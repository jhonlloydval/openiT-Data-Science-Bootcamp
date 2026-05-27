"""
pages/forecasting.py — AI Grade Forecasting

Uses Groq (via OpenAI-compatible client) with tool calling.
Tools: calculate_grade, compute_passing_probability,
       forecast_required_score, analyze_risk
"""

import json
import streamlit as st

from styles import page_header, COLORS
from utils import calc_subject_analytics, get_risk_info, calc_assessment_grade, fmt, pct
from probability_model import calc_pass_probability, explain_probability


# ── Tool Definitions (Anthropic-style, converted to OpenAI format for Groq) ───

TOOLS = [
    {
        "name": "calculate_grade",
        "description": "Calculates weighted average grade from scored items.",
        "input_schema": {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name":   {"type": "string"},
                            "score":  {"type": "number"},
                            "weight": {"type": "number"},
                        },
                    },
                }
            },
            "required": ["items"],
        },
    },
    {
        "name": "compute_passing_probability",
        "description": (
            "Weighted Distance Probability Model. "
            "earned_pts = sum(term_grade × term_weight) for completed terms."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "earned_pts":       {"type": "number"},
                "passing_grade":    {"type": "number"},
                "remaining_weight": {"type": "number", "description": "0.0 to 1.0"},
                "trend":            {"type": "number", "description": "Positive = improving"},
            },
            "required": ["earned_pts", "passing_grade", "remaining_weight"],
        },
    },
    {
        "name": "forecast_required_score",
        "description": "Minimum average score needed in remaining weight to hit a target grade.",
        "input_schema": {
            "type": "object",
            "properties": {
                "earned_pts":       {"type": "number"},
                "target_grade":     {"type": "number"},
                "remaining_weight": {"type": "number"},
            },
            "required": ["earned_pts", "target_grade", "remaining_weight"],
        },
    },
    {
        "name": "analyze_risk",
        "description": "Returns risk level and human-readable explanation for a subject.",
        "input_schema": {
            "type": "object",
            "properties": {
                "subject_name":        {"type": "string"},
                "passing_probability": {"type": "number"},
                "earned_pts":          {"type": "number"},
                "passing_grade":       {"type": "number"},
                "remaining_weight":    {"type": "number"},
            },
            "required": ["subject_name", "passing_probability", "remaining_weight"],
        },
    },
]


# ── Tool Execution ─────────────────────────────────────────────────────────────

def exec_tool(name: str, inp: dict) -> dict:
    try:
        if name == "calculate_grade":
            items = inp["items"]
            total_w = sum(i["weight"] for i in items)
            if total_w == 0:
                return {"error": "Total weight is zero."}
            grade = sum(i["score"] * i["weight"] for i in items) / total_w
            return {"grade": round(grade, 2)}

        elif name == "compute_passing_probability":
            prob = calc_pass_probability(
                earned_pts=inp["earned_pts"],
                passing_grade=inp["passing_grade"],
                remaining_weight=inp["remaining_weight"],
                trend=inp.get("trend", 0),
            )
            return {"probability": prob}

        elif name == "forecast_required_score":
            rw = inp["remaining_weight"]
            if rw <= 0:
                return {"required_score": None, "achievable": False, "note": "No remaining weight."}
            req = (inp["target_grade"] - inp["earned_pts"]) / rw
            return {
                "required_score": round(req, 1),
                "achievable": req <= 100,
                "note": (
                    "Target already achieved!" if req <= 0
                    else f"Need {req:.1f} average in remaining {rw*100:.0f}%." if req <= 100
                    else "Requires > 100 — may not be achievable."
                ),
            }

        elif name == "analyze_risk":
            ri = get_risk_info(inp["passing_probability"])
            explanation = explain_probability(
                earned_pts=inp.get("earned_pts", 0),
                passing_grade=inp.get("passing_grade", 75),
                remaining_weight=inp["remaining_weight"],
                probability=int(inp["passing_probability"]),
            )
            return {"risk_level": ri["level"], "explanation": explanation}

        return {"error": f"Unknown tool: {name}"}
    except Exception as e:
        return {"error": str(e)}


# ── AI Runner ──────────────────────────────────────────────────────────────────

def run_ai(user_message: str, subjects: list, api_key: str) -> str:
    try:
        from openai import OpenAI
    except ImportError:
        return "⚠️ `openai` package not installed. Run: pip install openai"

    client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

    # Build subject summary for context
    summary = []
    for s in subjects:
        a = calc_subject_analytics(s)
        summary.append({
            "subject":              s["name"],
            "passing_grade":        s["passing_grade"],
            "current_grade":        round(a["current_grade"], 1) if a["current_grade"] else None,
            "earned_pts":           round(a["earned_pts"], 2),
            "completed_weight_pct": round(a["completed_w"] * 100),
            "remaining_weight_pct": round(a["remaining_w"] * 100),
            "passing_probability":  a["probability"],
            "terms": [
                {
                    "name":        t["name"],
                    "weight_pct":  round(t["weight"] * 100),
                    "grade":       round(t["grade"], 1) if t["grade"] is not None else None,
                    "assessments": [
                        {
                            "name":           ass["name"],
                            "weight_pct":     round(ass["weight"] * 100),
                            "category_grade": round(calc_assessment_grade(ass), 1)
                                              if calc_assessment_grade(ass) is not None else None,
                            "items": [
                                {
                                    "name": item["name"],
                                    "score": item["score"],
                                    "total": item["total"],
                                    "percentage": round((item["score"] / item["total"]) * 100, 1)
                                                  if item["total"] > 0 else None,
                                }
                                for item in ass["items"]
                            ],
                        }
                        for ass in t["assessments"]
                    ],
                }
                for t in a["terms"]
            ],
        })

    # Convert tools to OpenAI-compatible format
    oai_tools = [
        {"type": "function",
         "function": {"name": t["name"], "description": t["description"], "parameters": t["input_schema"]}}
        for t in TOOLS
    ]

    system = (
        "You are Gradewise AI, an intelligent academic forecasting assistant for Filipino college students.\n"
        "Use the tools to compute real numbers before answering. Never guess or invent values.\n"
        "Be concise, warm, and specific. Reference actual subject names and numbers.\n"
        "End every response with a clear, actionable recommendation.\n"
        "Philippine context: Prelims 20%, Midterm 20%, Semi-Finals 25%, Finals 35% (default).\n"
        "earned_pts = sum(term_grade × term_weight). Do not confuse with current_grade."
    )

    messages = [
        {"role": "system", "content": system},
        {"role": "user",   "content": f"Academic data:\n{json.dumps(summary, indent=2)}\n\nQuestion: {user_message}"},
    ]

    for _ in range(8):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            messages=messages,
            tools=oai_tools,
            tool_choice="auto",
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            return msg.content or "Analysis complete."

        # Append assistant message with tool calls
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {"id": tc.id, "type": "function",
                 "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in msg.tool_calls
            ],
        })

        # Execute tools and append results
        for tc in msg.tool_calls:
            result = exec_tool(tc.function.name, json.loads(tc.function.arguments))
            messages.append({
                "role":         "tool",
                "tool_call_id": tc.id,
                "content":      json.dumps(result),
            })

    return "I couldn't complete the analysis."


# ── Quick Prompts ──────────────────────────────────────────────────────────────

QUICK_PROMPTS = [
    "What score do I need to pass all subjects?",
    "Which subject is most at risk and why?",
    "Predict my final grade if I maintain this performance.",
    "Give me a study priority plan.",
]


# ── Page Render ────────────────────────────────────────────────────────────────

def render():
    page_header("🔮 Forecasting", "AI-powered grade analysis using real calculations.")

    if not st.session_state.subjects:
        st.info("Add subjects in **Grade Entry** first.", icon="📚")
        return

    if not st.session_state.api_key:
        st.warning(
            "A Groq API key is required. Enter it in the sidebar under **API Key**.\n\n"
            "Get a free key at [console.groq.com](https://console.groq.com)",
            icon="🔑",
        )
        return

    # ── Chat history ───────────────────────────────────────────────────────────
    if not st.session_state.chat_history:
        st.markdown(
            f"""<div style='text-align:center;padding:48px 0 32px;color:{COLORS['muted']}'>
            <div style='font-size:36px;margin-bottom:10px'>🎓</div>
            <div style='font-size:15px;color:{COLORS['dim']}'>Ask Gradewise AI anything about your grades</div>
            <div style='font-size:12px;margin-top:4px'>Powered by real grade calculations and forecasting tools</div>
            </div>""",
            unsafe_allow_html=True,
        )

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user"><span>{msg["content"]}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="chat-ai"><div class="chat-ai-label">◈ Gradewise AI</div>'
                f'<div class="chat-ai-inner">{msg["content"]}</div></div>',
                unsafe_allow_html=True,
            )

    # ── Quick prompts (shown only at start) ───────────────────────────────────
    if len(st.session_state.chat_history) < 2:
        st.markdown(f"<p style='font-size:12px;color:{COLORS['muted']};margin-bottom:6px'>Quick questions:</p>", unsafe_allow_html=True)
        q_cols = st.columns(len(QUICK_PROMPTS))
        for col, prompt in zip(q_cols, QUICK_PROMPTS):
            if col.button(prompt, use_container_width=True, key=f"qp_{prompt[:15]}"):
                _send(prompt)
                st.rerun()

    st.markdown("")

    # ── Input row ──────────────────────────────────────────────────────────────
    i1, i2, i3 = st.columns([6, 1, 1])
    user_input = i1.text_input(
        "msg", placeholder="Ask about your grades, risks, or required scores…",
        label_visibility="collapsed", key="fc_input",
    )
    send  = i2.button("Ask →",  use_container_width=True, type="primary")
    clear = i3.button("Clear",  use_container_width=True)

    if clear:
        st.session_state.chat_history = []
        st.rerun()

    if send and user_input.strip():
        _send(user_input.strip())
        st.rerun()


def _send(message: str):
    st.session_state.chat_history.append({"role": "user", "content": message})
    with st.spinner("Thinking…"):
        try:
            reply = run_ai(message, st.session_state.subjects, st.session_state.api_key)
        except Exception as e:
            reply = f"⚠️ Error: {e}"
    st.session_state.chat_history.append({"role": "ai", "content": reply})
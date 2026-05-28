# ToolHaive AI

ToolHaive AI, displayed in the app as ToolHaive AI, is a local, privacy-first
AI workspace built for the openIT Data Science Bootcamp. It combines a polished
home page, a tools library, a general chat assistant named HAIVE, scoped AI
tools, a custom tool builder, and academic grade forecasting utilities into one
Streamlit application.

The project is designed as a capstone-style prototype: it demonstrates prompt
engineering, scoped assistants, local model integration, interface design, and
tool-based workflows without requiring a cloud backend.

## Table of Contents

- [Project Overview](#project-overview)
- [Core Features](#core-features)
- [Built-in Hives](#built-in-hives)
- [GradeWise and Forecasting](#gradewise-and-forecasting)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Running the App](#running-the-app)
- [Using Ollama](#using-ollama)
- [How the App Works](#how-the-app-works)
- [Custom Tool Builder](#custom-tool-builder)
- [Source Documents](#source-documents)
- [Page Routes](#page-routes)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Troubleshooting](#troubleshooting)
- [Development Notes](#development-notes)
- [Credits](#credits)
- [License](#license)

## Project Overview

ToolHaive AI is a modular AI assistant platform. Instead of giving users only
one generic chatbot, the app provides multiple focused assistants called
"Hives." Each Hive has a specific role, purpose, input format, and prompt
boundary.

The app includes:

- A branded landing page for ToolHaive AI
- A searchable tools library
- A general AI chat assistant called HAIVE
- 12 built-in specialized Hives
- A custom prompt-powered tool builder
- A self-contained GradeWise academic tracker
- A standalone Forecasting Hive
- About and Sources pages with project documentation
- Shared ToolHaive design system and navigation
- Local model calls through Ollama

## Core Features

### Local AI Workflow

All model calls are routed through `utils/ollama_client.py`, which connects to
Ollama at:

```text
http://localhost:11434/api/chat
```

The default model is:

```text
phi4-mini
```

The app also exposes `llama3.2` as an available model in HAIVE. Other model
options are displayed as coming soon.

### Scoped Assistants

Each specialized Hive uses a scoped system prompt. The shared prompt boundary is
stored in:

```text
ToolHaive/prompts/tool_scope.txt
```

This keeps each assistant focused on its intended purpose and prevents one tool
from behaving like a completely open-ended chatbot.

### Shared Brand System

The shared UI system lives in:

```text
ToolHaive/utils/ui.py
```

It defines:

- Navigation bar
- Home and tool page layouts
- Cards and buttons
- Tool headers
- Hexagon background patterns
- Tool body containers
- Output styling
- Responsive spacing rules
- ToolHaive colors and typography

### Tools Library

The tools library is rendered from a single source of truth:

```text
ToolHaive/utils/tools_data.py
```

That file controls built-in tool names, categories, descriptions, icons, cover
styles, turn type, and page routes.

### Custom Tool Support

Users can build and save custom prompt-powered assistants from the UI. Saved
custom tools are stored locally in:

```text
ToolHaive/data/custom_tools.json
```

The tools library merges built-in tools and saved custom tools at runtime.

## Built-in Hives

ToolHaive currently includes 12 built-in specialized Hives plus HAIVE general
chat.

| Hive | Category | Type | Purpose |
|---|---|---:|---|
| HAIVE | General | Multi-turn | Open-ended chat for drafting, studying, planning, and problem solving |
| Interview Coach Hive | Professional | Multi-turn | Mock interview practice with structured feedback |
| Doc Summarizer Hive | Academic | Single-turn | Summarizes pasted text into key points and action items |
| Doc Paraphraser Hive | Academic | Single-turn | Rewrites text in selected tones while preserving meaning |
| GradeWise Hive | Academic | Multi-turn | Tracks subjects, itemized scores, risk, and academic analytics |
| Forecasting Hive | Academic | Multi-turn | Forecasts required scores, targets, risk, and study priorities |
| Roleplay Creator Hive | Education | Multi-turn | Creates a configured AI persona for roleplay conversations |
| Wellness Companion Hive | Wellness | Multi-turn | Provides reflective journaling support for everyday wellbeing |
| Fact Checker Hive | Media Literacy | Single-turn | Reviews claims, article excerpts, and credibility signals |
| Career Roadmap Hive | Professional | Single-turn | Builds skill-gap and 30-60-90 day career plans |
| Grammar Checker Hive | Academic | Single-turn | Reviews grammar, clarity, punctuation, and writing quality |
| Essay Generator Hive | Academic | Single-turn | Generates structured essay or article drafts |
| Quiz and Flashcard Generator Hive | Education | Single-turn | Creates quizzes and flashcards from notes or source text |

Note: the app can show more than 12 tools in the library when custom tools are
saved locally.

## GradeWise and Forecasting

GradeWise replaces the old Grade Predictor placeholder. It is implemented as one
self-contained Streamlit page:

```text
ToolHaive/pages/4_Grade_Predictor.py
```

GradeWise includes:

- Subject management
- Passing grade configuration
- Default term weights
- Itemized score entry
- Assessment category grades
- Term grades
- Current weighted grade
- Required score forecast
- Passing probability estimate
- Risk level labels
- GWA equivalent display
- Demo subjects
- Dashboard view
- Forecasting chat
- Analytics charts
- Category radar chart
- Risk map

Default term weights:

| Term | Weight |
|---|---:|
| Prelims | 20% |
| Midterm | 20% |
| Semi-Finals | 25% |
| Finals | 35% |

Default assessment categories:

| Assessment | Weight |
|---|---:|
| Quiz | 30% |
| Attendance | 10% |
| Project | 30% |
| Exam | 30% |

The standalone Forecasting Hive is implemented here:

```text
ToolHaive/pages/13_Forecasting.py
```

It supports:

- Manual academic scenarios
- Current grade input
- Completed grade weight
- Passing grade
- Target grade
- Recent trend
- Required remaining average
- Passing probability estimate
- AI-generated action plans

When GradeWise session data exists, Forecasting Hive can use it as context.
Otherwise, it runs in manual scenario mode.

## Tech Stack

| Layer | Technology |
|---|---|
| App framework | Streamlit |
| Language | Python |
| Local LLM runtime | Ollama |
| HTTP client | Requests |
| Charts | Plotly |
| UI styling | Custom CSS injected through Streamlit |
| Data persistence | Local JSON for custom tools |
| Source documents | PDF, DOCX, HTML |

Recommended Python version:

```text
Python 3.10 or newer
```

The current development environment used Python 3.12.

## Project Structure

```text
openiT-Data-Science-Bootcamp/
|-- README.md
|-- ToolHaive/
|   |-- app.py
|   |-- data/
|   |   `-- custom_tools.json
|   |-- files/
|   |   |-- ToolHaive_Paper.docx
|   |   |-- ToolHaive_Paper.pdf
|   |   `-- ToolHaive_brand_guide.html
|   |-- pages/
|   |   |-- 0_Tools_Library.py
|   |   |-- 1_Interview_Coach.py
|   |   |-- 2_Document_Summarizer.py
|   |   |-- 3_Document_Paraphraser.py
|   |   |-- 4_Grade_Predictor.py
|   |   |-- 5_Roleplay_Creator.py
|   |   |-- 6_Wellness_Companion.py
|   |   |-- 7_Fact_Checker.py
|   |   |-- 8_Career_Roadmap.py
|   |   |-- 9_Custom_Tool_Runner.py
|   |   |-- 10_Grammar_Checker.py
|   |   |-- 11_Essay_Generator.py
|   |   |-- 12_Quiz_Flashcard_Generator.py
|   |   |-- 13_Forecasting.py
|   |   |-- about.py
|   |   |-- haive.py
|   |   `-- sources.py
|   |-- prompts/
|   |   `-- tool_scope.txt
|   `-- utils/
|       |-- __init__.py
|       |-- ollama_client.py
|       |-- tools_data.py
|       `-- ui.py
`-- Onground/
    `-- Bootcamp exercises, datasets, notebooks, and lesson files
```

## Setup and Installation

### 1. Clone or Open the Repository

```bash
cd /Users/jhonlloydval/GitHub/openiT-Data-Science-Bootcamp
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install streamlit requests plotly
```

Optional but useful:

```bash
pip install watchdog
```

`watchdog` is optional. Streamlit may recommend it for better local file-watch
performance.

## Running the App

From the repository root:

```bash
cd ToolHaive
python3 -m streamlit run app.py
```

Streamlit will print a local URL, usually:

```text
http://localhost:8501
```

If that port is already busy, choose another port:

```bash
python3 -m streamlit run app.py --server.port 8502
```

Then open:

```text
http://localhost:8502
```

## Using Ollama

The UI can load without Ollama, but AI responses require Ollama to be running.

### 1. Start Ollama

```bash
ollama serve
```

If Ollama is already running as a background service, this command may not be
needed.

### 2. Pull the Default Model

```bash
ollama pull phi4-mini
```

### 3. Pull the Secondary Available Model

```bash
ollama pull llama3.2
```

### 4. Confirm Models Are Installed

```bash
ollama list
```

The app sends chat requests to Ollama through:

```python
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "phi4-mini"
```

These values are defined in:

```text
ToolHaive/utils/ollama_client.py
```

## How the App Works

### Landing Page

File:

```text
ToolHaive/app.py
```

The landing page introduces the project, shows brand visuals, previews tools,
and links users into the Tools Library.

### Tools Library

File:

```text
ToolHaive/pages/0_Tools_Library.py
```

The Tools Library:

- Loads built-in tools from `utils/tools_data.py`
- Loads custom tools from `data/custom_tools.json`
- Provides search and category filters
- Shows a featured HAIVE card
- Renders each Hive as a launchable card

### Shared Tool Data

File:

```text
ToolHaive/utils/tools_data.py
```

This file is the single source of truth for built-in Hives. Each entry includes:

- `id`
- `name`
- `user`
- `desc`
- `cat`
- `cat_label`
- `turn`
- `cover`
- `page`
- `icon_svg`

### Shared UI

File:

```text
ToolHaive/utils/ui.py
```

This file contains reusable UI helpers:

- `inject_styles()`
- `render_navbar()`
- `render_tool_header()`
- `tool_body_container()`
- `render_html()`
- `render_output_box()`
- `render_tool_tip()`
- `render_output_header()`

It also contains the global CSS design system.

### Shared AI Client

File:

```text
ToolHaive/utils/ollama_client.py
```

This file handles:

- Ollama chat requests
- Default model configuration
- Available model metadata
- Prompt template loading
- Scoped system prompt construction
- Ollama health checks

### Prompt Boundary

File:

```text
ToolHaive/prompts/tool_scope.txt
```

Each tool-specific prompt is wrapped inside the shared scope template. This is
what keeps each Hive focused on its task.

## Custom Tool Builder

File:

```text
ToolHaive/pages/9_Custom_Tool_Runner.py
```

The Custom Tool Hive has two tabs:

1. Build Tool
2. Run Custom Tool

When creating a custom tool, the user can define:

- Tool name
- Description
- Target user
- Category
- System prompt
- Input placeholder
- Output format instruction

Saved custom tools are appended to:

```text
ToolHaive/data/custom_tools.json
```

They appear in the Tools Library after saving.

## Source Documents

The project includes local reference files in:

```text
ToolHaive/files/
```

Current source files:

| File | Purpose |
|---|---|
| `ToolHaive_Paper.pdf` | Project paper and system design reference |
| `ToolHaive_Paper.docx` | Editable version of the project paper |
| `ToolHaive_brand_guide.html` | Brand guide and visual design reference |

The Sources page explains how these files informed:

- Tool taxonomy
- Prompt boundaries
- Interface structure
- Brand system
- Navigation and layout decisions

## Page Routes

Common app routes:

| Page | Route |
|---|---|
| Home | `/` |
| Tools Library | `/Tools_Library` |
| HAIVE | `/haive` |
| Interview Coach Hive | `/Interview_Coach` |
| Document Summarizer Hive | `/Document_Summarizer` |
| Document Paraphraser Hive | `/Document_Paraphraser` |
| GradeWise Hive | `/Grade_Predictor` |
| Roleplay Creator Hive | `/Roleplay_Creator` |
| Wellness Companion Hive | `/Wellness_Companion` |
| Fact Checker Hive | `/Fact_Checker` |
| Career Roadmap Hive | `/Career_Roadmap` |
| Custom Tool Hive | `/Custom_Tool_Runner` |
| Grammar Checker Hive | `/Grammar_Checker` |
| Essay Generator Hive | `/Essay_Generator` |
| Quiz and Flashcard Generator Hive | `/Quiz_Flashcard_Generator` |
| Forecasting Hive | `/Forecasting` |
| About | `/about` |
| Sources | `/sources` |

## Limitations

ToolHaive is a capstone prototype, not a production AI platform.

Current limitations:

- Responses are not streamed token by token.
- Most tool state is stored in Streamlit session state.
- Chat history can reset on refresh.
- Custom tools are stored locally in JSON.
- There is no account system or cloud sync.
- The app does not browse the internet during normal tool use.
- Source files are not embedded into a retrieval system.
- Local model quality depends on the installed Ollama model.
- Some model options are visible in the UI but marked as coming soon.
- Grade forecasts are transparent estimates, not guaranteed outcomes.

## Future Improvements

Potential next steps:

- Add streaming responses for all AI tools
- Add persistent conversation history
- Add export and import for custom tools
- Add retrieval over `ToolHaive_Paper.pdf`
- Add semantic search for project sources
- Add a real settings page for model configuration
- Add cloud model connectors
- Add authentication if deployed beyond local use
- Add automated tests for grade calculations
- Add a requirements file for easier setup
- Add screenshots or a short demo video
- Add deployment instructions

## Troubleshooting

### Streamlit port is already in use

Use another port:

```bash
python3 -m streamlit run app.py --server.port 8502
```

### Ollama connection error

Start Ollama:

```bash
ollama serve
```

Then pull the default model:

```bash
ollama pull phi4-mini
```

### Model response is slow

Local models depend on your machine. Try:

- Closing other heavy applications
- Using a smaller model
- Asking shorter prompts
- Restarting Ollama

### A tool gives an out-of-scope response

Each Hive is intentionally scoped. Use HAIVE for open-ended questions, or use
the correct specialized Hive for the task.

### Custom tool does not appear

Check that it was saved to:

```text
ToolHaive/data/custom_tools.json
```

Then refresh the Tools Library page.

### GradeWise data disappeared

GradeWise uses Streamlit session state. If the browser refreshes or the server
restarts, session data can reset. Use the demo subjects to quickly preview the
workflow again.

## Development Notes

- Keep built-in tool metadata in `utils/tools_data.py`.
- Keep shared design changes in `utils/ui.py`.
- Keep Ollama configuration in `utils/ollama_client.py`.
- Keep tool-specific prompts inside each tool page.
- Keep shared tool boundaries in `prompts/tool_scope.txt`.
- Avoid hardcoding custom tools into the app. Save them to `data/custom_tools.json`.
- When adding a new built-in Hive, create a page in `ToolHaive/pages/` and add
  its metadata to `BUILTIN_TOOLS`.

## Credits

Project:

```text
ToolHaive AI / ToolHaive AI
```

Built for:

```text
openIT Data Science Bootcamp
```

Focus areas:

- Prompt engineering
- Local AI apps
- Streamlit development
- Scoped assistant design
- UI/UX prototyping
- Academic and productivity tools

## License

No license file is currently included in this repository. Add a license before
publishing, distributing, or reusing this project outside the bootcamp context.

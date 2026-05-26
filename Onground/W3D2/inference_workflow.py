"""
Section 7: Inference Workflow
Demonstrates encoder-only, decoder-only, and encoder-decoder inference patterns.
Also covers greedy, sampling, and beam search decoding.

Exercise 7A:
  Risk of using training target text during inference:
  This is called "teacher forcing leakage" — the model never learns to recover
  from its own mistakes. At inference, there is no ground-truth target to guide
  each step, so the model sees its own (potentially wrong) previous predictions
  instead. Errors compound step by step, causing the output to drift far from
  the intended target. The model appears accurate during training but performs
  much worse in real use.
"""

from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    AutoModelForCausalLM,
    T5Tokenizer, T5ForConditionalGeneration
)
import torch

# ── Inference prompts ──────────────────────────────────────────────────────────
encoder_prompt     = "The summary was concise and correct."
decoder_prompt     = "Write one sentence about cross-attention."
enc_dec_prompt     = "Transformers compare tokens with attention and use masks for generation."

# ── 1. Encoder-only: single forward pass → label ──────────────────────────────
print("="*60)
print("1. ENCODER-ONLY — Single forward pass")
print("="*60)

tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
model     = AutoModelForSequenceClassification.from_pretrained(
    'distilbert-base-uncased', num_labels=3
)
model.eval()

inputs  = tokenizer(encoder_prompt, return_tensors='pt', truncation=True, max_length=128)
with torch.no_grad():
    logits = model(**inputs).logits

label_map  = {0: 'positive', 1: 'negative', 2: 'neutral'}
prediction = label_map[torch.argmax(logits, dim=-1).item()]
print(f"Input:  {encoder_prompt}")
print(f"Output: {prediction}\n")

# ── 2. Decoder-only: autoregressive loop → text continuation ──────────────────
print("="*60)
print("2. DECODER-ONLY — Autoregressive loop")
print("="*60)

tokenizer = AutoTokenizer.from_pretrained('distilgpt2')
model     = AutoModelForCausalLM.from_pretrained('distilgpt2')
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model.eval()

input_ids = tokenizer.encode(decoder_prompt, return_tensors='pt')

# Greedy
with torch.no_grad():
    greedy_out = model.generate(input_ids, max_length=60, do_sample=False)
print(f"Prompt:      {decoder_prompt}")
print(f"Greedy:      {tokenizer.decode(greedy_out[0], skip_special_tokens=True)}\n")

# Sampling
with torch.no_grad():
    sample_out = model.generate(input_ids, max_length=60, do_sample=True, temperature=0.7)
print(f"Sampling:    {tokenizer.decode(sample_out[0], skip_special_tokens=True)}\n")

# Beam search
with torch.no_grad():
    beam_out = model.generate(input_ids, max_length=60, num_beams=4, early_stopping=True)
print(f"Beam search: {tokenizer.decode(beam_out[0], skip_special_tokens=True)}\n")

# ── 3. Encoder-decoder: encode once, decode step by step → summary ────────────
print("="*60)
print("3. ENCODER-DECODER — Encode once, decode step by step")
print("="*60)

tokenizer = T5Tokenizer.from_pretrained('t5-small')
model     = T5ForConditionalGeneration.from_pretrained('t5-small')
model.eval()

# T5 expects a task prefix
source    = "summarize: " + enc_dec_prompt
input_ids = tokenizer(source, return_tensors='pt', truncation=True, max_length=128)['input_ids']

with torch.no_grad():
    output_ids = model.generate(input_ids, max_length=64)

summary = tokenizer.decode(output_ids[0], skip_special_tokens=True)
print(f"Input:  {enc_dec_prompt}")
print(f"Output: {summary}\n")

print("Inference workflow complete!")

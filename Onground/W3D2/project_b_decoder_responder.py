"""
Project B: Decoder Prompt Responder
Goal: Generate one-sentence explanations from decoder_generation prompts.
Deliverable: Three prompts and their generated completions.

Experiment Log:
  Model:             distilgpt2
  Task rows used:    decoder_generation
  Tokenizer:         distilgpt2, max_length=128
  Epochs:            2
  Learning rate:     5e-5
  Metric:            Qualitative (fluency of completions)
"""

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load and split
df    = pd.read_csv('/Users/jhonlloydval/DataScience_BOOTCAMP/W3D2/transformers/transformer_workbook_dataset.csv')
train = df[(df['split'] == 'train') & (df['task_type'] == 'decoder_generation')]
test  = df[(df['split'] == 'test')  & (df['task_type'] == 'decoder_generation')]

print(f"Train: {len(train)} | Test: {len(test)}")

tokenizer = AutoTokenizer.from_pretrained('distilgpt2')
model     = AutoModelForCausalLM.from_pretrained('distilgpt2')
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=5e-5)

# Training: combine prompt + target_text so model learns the pattern
model.train()
for epoch in range(2):
    total_loss = 0
    for _, row in train.iterrows():
        text   = f"{row['input_text']} {row['target_text']}"
        inputs = tokenizer(text, return_tensors='pt',
                           truncation=True, max_length=128).to(device)
        out    = model(input_ids=inputs['input_ids'], labels=inputs['input_ids'])

        optimizer.zero_grad()
        out.loss.backward()
        optimizer.step()
        total_loss += out.loss.item()

    print(f"Epoch {epoch+1} | Loss: {total_loss/len(train):.4f}")

# Inference: provide only the prompt, let model continue
model.eval()
print("\nThree Prompts and Generated Completions:")
print("-" * 60)
for _, row in test.head(3).iterrows():
    input_ids = tokenizer.encode(str(row['input_text']), return_tensors='pt').to(device)
    with torch.no_grad():
        output = model.generate(input_ids, max_length=60, do_sample=True, temperature=0.7)
    completion = tokenizer.decode(output[0], skip_special_tokens=True)
    print(f"Prompt:     {row['input_text']}")
    print(f"Expected:   {row['target_text']}")
    print(f"Generated:  {completion}\n")

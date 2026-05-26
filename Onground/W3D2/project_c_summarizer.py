"""
Project C: Seq2seq Summarizer
Goal: Summarize transformer concept paragraphs.
Deliverable: Three source-target-output comparisons.

Experiment Log:
  Model:             t5-small
  Task rows used:    encoder_decoder_summarization
  Tokenizer:         t5-small, max_length=128 (source), 64 (target)
  Epochs:            2
  Learning rate:     3e-4
  Metric:            Word overlap (qualitative)
"""

import pandas as pd
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load and split
df    = pd.read_csv('/Users/jhonlloydval/DataScience_BOOTCAMP/W3D2/transformers/transformer_workbook_dataset.csv')
train = df[(df['split'] == 'train') & (df['task_type'] == 'encoder_decoder_summarization')]
test  = df[(df['split'] == 'test')  & (df['task_type'] == 'encoder_decoder_summarization')]

print(f"Train: {len(train)} | Test: {len(test)}")

tokenizer = T5Tokenizer.from_pretrained('t5-small')
model     = T5ForConditionalGeneration.from_pretrained('t5-small')
device    = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=3e-4)

# Training with teacher forcing (labels= handles it internally)
model.train()
for epoch in range(2):
    total_loss = 0
    for _, row in train.iterrows():
        source = tokenizer("summarize: " + str(row['input_text']),
                           return_tensors='pt', truncation=True, max_length=128).to(device)
        target = tokenizer(str(row['target_text']),
                           return_tensors='pt', truncation=True, max_length=64).to(device)

        out = model(input_ids=source['input_ids'],
                    attention_mask=source['attention_mask'],
                    labels=target['input_ids'])

        optimizer.zero_grad()
        out.loss.backward()
        optimizer.step()
        total_loss += out.loss.item()

    print(f"Epoch {epoch+1} | Loss: {total_loss/len(train):.4f}")

# Inference: encode once, decode step by step
model.eval()
print("\nThree Source-Target-Output Comparisons:")
print("-" * 60)
for _, row in test.head(3).iterrows():
    source = tokenizer("summarize: " + str(row['input_text']),
                       return_tensors='pt', truncation=True, max_length=128).to(device)
    with torch.no_grad():
        output_ids = model.generate(source['input_ids'], max_length=64)
    output = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    # Qualitative word overlap score
    target_words = set(str(row['target_text']).lower().split())
    output_words = set(output.lower().split())
    overlap      = len(target_words & output_words) / max(len(target_words), 1)

    print(f"Source:   {row['input_text'][:100]}...")
    print(f"Target:   {row['target_text']}")
    print(f"Output:   {output}")
    print(f"Overlap:  {overlap:.0%}\n")

"""
Project D: Seq2seq Pseudo-code Translator
Goal: Map instructions to pseudo-code using encoder_decoder_translation rows.
Deliverable: Exact-match score and error analysis.

Experiment Log:
  Model:             t5-small
  Task rows used:    encoder_decoder_translation
  Tokenizer:         t5-small, max_length=64 (source), 32 (target)
  Epochs:            3
  Learning rate:     3e-4
  Metric:            Exact match (prediction == target after stripping whitespace)
"""

import pandas as pd
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load and split
df    = pd.read_csv('/Users/jhonlloydval/DataScience_BOOTCAMP/W3D2/transformers/transformer_workbook_dataset.csv')
train = df[(df['split'] == 'train') & (df['task_type'] == 'encoder_decoder_translation')]
test  = df[(df['split'] == 'test')  & (df['task_type'] == 'encoder_decoder_translation')]

# Fallback: use validation as test if test split is empty
if len(test) == 0:
    test = df[(df['split'] == 'validation') & (df['task_type'] == 'encoder_decoder_translation')]

print(f"Train: {len(train)} | Test: {len(test)}")
print(f"Example input:  {train.iloc[0]['input_text']}")
print(f"Example target: {train.iloc[0]['target_text']}\n")

tokenizer = T5Tokenizer.from_pretrained('t5-small')
model     = T5ForConditionalGeneration.from_pretrained('t5-small')
device    = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=3e-4)

# Training
model.train()
for epoch in range(3):
    total_loss = 0
    for _, row in train.iterrows():
        source = tokenizer(str(row['input_text']),
                           return_tensors='pt', truncation=True, max_length=64).to(device)
        target = tokenizer(str(row['target_text']),
                           return_tensors='pt', truncation=True, max_length=32).to(device)

        out = model(input_ids=source['input_ids'],
                    attention_mask=source['attention_mask'],
                    labels=target['input_ids'])

        optimizer.zero_grad()
        out.loss.backward()
        optimizer.step()
        total_loss += out.loss.item()

    print(f"Epoch {epoch+1} | Loss: {total_loss/len(train):.4f}")

# Inference and evaluation
model.eval()
exact_matches = 0
errors        = []

print("\nPredictions:")
print("-" * 60)
for _, row in test.iterrows():
    source = tokenizer(str(row['input_text']),
                       return_tensors='pt', truncation=True, max_length=64).to(device)
    with torch.no_grad():
        output_ids = model.generate(source['input_ids'], max_length=32)
    prediction = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    target     = str(row['target_text']).strip()
    match      = prediction.strip() == target

    if match:
        exact_matches += 1
    else:
        errors.append({'input': row['input_text'], 'target': target, 'prediction': prediction})

    print(f"Input:      {row['input_text']}")
    print(f"Target:     {target}")
    print(f"Predicted:  {prediction}")
    print(f"Match:      {match}\n")

# Exact-match score
exact_match_score = exact_matches / max(len(test), 1)
print(f"Exact Match Score: {exact_matches}/{len(test)} = {exact_match_score:.0%}")

# Error analysis
if errors:
    print("\nError Analysis:")
    print("-" * 60)
    for err in errors:
        print(f"Input:      {err['input']}")
        print(f"Target:     {err['target']}")
        print(f"Predicted:  {err['prediction']}")
        # Show which words were wrong
        t_words = err['target'].split()
        p_words = err['prediction'].split()
        missed  = [w for w in t_words if w not in p_words]
        extra   = [w for w in p_words if w not in t_words]
        print(f"Missing:    {missed}")
        print(f"Extra:      {extra}\n")
else:
    print("\nNo errors — all predictions matched exactly!")

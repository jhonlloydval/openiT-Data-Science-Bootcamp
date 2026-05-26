"""
Mini Lab: Sequence-to-Sequence (Encoder-Decoder)
Uses a pre-trained T5 model for summarization and pseudo-code tasks.
"""

import pandas as pd
from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch

# Step 1: Load rows where task_type starts with encoder_decoder
print("Step 1: Loading data...")
df = pd.read_csv('/Users/jhonlloydval/DataScience_BOOTCAMP/W3D2/transformers/transformer_workbook_dataset.csv')
encoder_decoder_df = df[df['task_type'].str.startswith('encoder_decoder')]
print(f"Loaded {len(encoder_decoder_df)} rows")
print(f"Task types found: {encoder_decoder_df['task_type'].unique()}\n")

# Step 2: Use input_text as encoder source, target_text as decoder target
train_df = encoder_decoder_df[encoder_decoder_df['split'] == 'train'].head(20)
test_df  = encoder_decoder_df[encoder_decoder_df['split'] == 'test'].head(5)

print(f"Train rows: {len(train_df)}, Test rows: {len(test_df)}")
print(f"Example input : {train_df.iloc[0]['input_text']}")
print(f"Example target: {train_df.iloc[0]['target_text']}\n")

# Load small T5 model
print("Loading T5 model...")
tokenizer = T5Tokenizer.from_pretrained('t5-small')
model     = T5ForConditionalGeneration.from_pretrained('t5-small')
device    = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Step 3: Train with teacher forcing
# T5ForConditionalGeneration does teacher forcing internally when labels are provided
print("\nStep 3: Fine-tuning with teacher forcing...")
optimizer = torch.optim.Adam(model.parameters(), lr=3e-4)
model.train()

for epoch in range(2):
    total_loss = 0
    for _, row in train_df.iterrows():
        # Tokenize source (encoder input)
        source = tokenizer(
            row['input_text'], return_tensors='pt',
            truncation=True, max_length=128
        ).to(device)

        # Tokenize target (decoder target / labels)
        target = tokenizer(
            row['target_text'], return_tensors='pt',
            truncation=True, max_length=64
        ).to(device)

        # Forward pass — teacher forcing is handled internally
        outputs = model(
            input_ids=source['input_ids'],
            attention_mask=source['attention_mask'],
            labels=target['input_ids']
        )

        loss = outputs.loss
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()

    print(f"  Epoch {epoch+1} | Avg Loss: {total_loss / len(train_df):.4f}")

model.eval()

# Step 4: At inference, encode source once and decode step by step
print("\nStep 4: Inference — encode source, decode target step by step")
print("=" * 70)

results = []
for _, row in test_df.iterrows():
    source = tokenizer(
        row['input_text'], return_tensors='pt',
        truncation=True, max_length=128
    ).to(device)

    # Encode once, then auto-regressively decode
    with torch.no_grad():
        output_ids = model.generate(
            input_ids=source['input_ids'],
            attention_mask=source['attention_mask'],
            max_length=64
        )

    prediction = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    results.append({
        'task_type':  row['task_type'],
        'input':      row['input_text'],
        'target':     row['target_text'],
        'prediction': prediction
    })

# Step 5: Evaluate
print("\nStep 5: Evaluation")
print("=" * 70)

for r in results:
    print(f"\nTask:       {r['task_type']}")
    print(f"Input:      {r['input'][:100]}...")
    print(f"Target:     {r['target']}")
    print(f"Prediction: {r['prediction']}")

    if 'pseudo' in r['task_type']:
        # Exact match for pseudo-code rows
        match = r['target'].strip() == r['prediction'].strip()
        print(f"Exact Match: {match}")
    else:
        # Qualitative check for summaries
        target_words = set(r['target'].lower().split())
        pred_words   = set(r['prediction'].lower().split())
        overlap      = len(target_words & pred_words) / max(len(target_words), 1)
        print(f"Word Overlap (qualitative): {overlap:.0%}")

    print("-" * 70)

print("\nMini lab complete!")


# ──────────────────────────────────────────────────────────────────────────────
# Exercise 5A: Mark each task as encoder-only, decoder-only, or encoder-decoder
# ──────────────────────────────────────────────────────────────────────────────
print("""
Exercise 5A Answers:
  Spam classification   → Encoder-only      (classify a fixed input, no generation needed)
  Article summarization → Encoder-Decoder   (read full article, generate shorter output)
  Story continuation    → Decoder-only      (generate new tokens from a prompt)
  Translation           → Encoder-Decoder   (read source language, generate target language)
  Retrieval embedding   → Encoder-only      (produce a fixed vector representing the input)
""")

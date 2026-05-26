"""
Baseline Training Checklist + Exercise 6A
"""

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ── Load and split data ────────────────────────────────────────────────────────
df = pd.read_csv('/Users/jhonlloydval/DataScience_BOOTCAMP/W3D2/transformers/transformer_workbook_dataset.csv')

train = df[df['split'] == 'train']
valid = df[df['split'] == 'validation']
test  = df[df['split'] == 'test']

enc     = train[train['task_type'] == 'encoder_classification']
seq2seq = train[train['task_type'].str.startswith('encoder_decoder')]
dec     = train[train['task_type'] == 'decoder_generation']

print(f"Train: {len(train)} | Valid: {len(valid)} | Test: {len(test)}")
print(f"Encoder classification: {len(enc)} | Seq2Seq: {len(seq2seq)} | Decoder gen: {len(dec)}\n")

# ── Exercise 6A: Validation rule ───────────────────────────────────────────────
print("Exercise 6A: Checking data integrity...")

def validate_rows(df):
    classification_rows = df[df['task_type'] == 'encoder_classification']
    generation_rows     = df[df['task_type'].str.startswith('encoder_decoder') |
                             (df['task_type'] == 'decoder_generation')]

    # Check: every classification row must have a non-empty label
    bad_labels = classification_rows[classification_rows['label'].isna() |
                                     (classification_rows['label'].astype(str).str.strip() == '')]

    # Check: every generation row must have a non-empty target_text
    bad_targets = generation_rows[generation_rows['target_text'].isna() |
                                  (generation_rows['target_text'].astype(str).str.strip() == '')]

    print(f"  Classification rows missing label:       {len(bad_labels)}")
    print(f"  Generation rows missing target_text:     {len(bad_targets)}")

    if len(bad_labels) == 0 and len(bad_targets) == 0:
        print("  All rows passed validation!\n")
    else:
        print("  Warning: Some rows failed validation. Fix before training.\n")

validate_rows(train)

# ── Checklist item 1: Overfit a tiny subset first ─────────────────────────────
print("Checklist 1: Overfitting a tiny subset to catch data issues...")
tiny = enc.head(5)
print(f"  Using {len(tiny)} rows for overfit test\n")

# ── Checklist item 2: Labels/targets not empty (already done in Exercise 6A) ──
print("Checklist 2: Labels and targets verified above via validate_rows()\n")

# ── Checklist item 3: Train/valid/test are already separate ───────────────────
print(f"Checklist 3: Splits are separate — train={len(train)}, valid={len(valid)}, test={len(test)}\n")

# ── Checklist items 4 & 5: Train, track loss, save model ──────────────────────
print("Checklist 4 & 5: Training with loss tracking and model saving...\n")

label_map = {'positive': 0, 'negative': 1, 'neutral': 2}

tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
model     = AutoModelForSequenceClassification.from_pretrained(
    'distilbert-base-uncased', num_labels=len(label_map)
)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

optimizer = torch.optim.Adam(model.parameters(), lr=2e-5)

# Training loop on tiny subset first (overfit check)
model.train()
for epoch in range(3):
    total_loss = 0
    for _, row in tiny.iterrows():
        inputs = tokenizer(
            str(row['input_text']),
            return_tensors='pt', truncation=True, max_length=128
        ).to(device)

        label = torch.tensor([label_map.get(str(row['label']), 0)]).to(device)
        outputs = model(**inputs, labels=label)

        optimizer.zero_grad()
        outputs.loss.backward()
        optimizer.step()
        total_loss += outputs.loss.item()

    # Track training loss
    avg_loss = total_loss / len(tiny)
    print(f"  Epoch {epoch+1} | Train Loss: {avg_loss:.4f}")

# Validation performance
model.eval()
correct = 0
val_enc = valid[valid['task_type'] == 'encoder_classification'].head(10)
for _, row in val_enc.iterrows():
    inputs = tokenizer(
        str(row['input_text']),
        return_tensors='pt', truncation=True, max_length=128
    ).to(device)
    with torch.no_grad():
        logits = model(**inputs).logits
    pred = torch.argmax(logits, dim=-1).item()
    true = label_map.get(str(row['label']), 0)
    if pred == true:
        correct += 1

val_acc = correct / max(len(val_enc), 1)
print(f"\n  Validation Accuracy: {val_acc:.0%}")

# Save tokenizer, model weights, and label mapping together
import json, os
save_dir = '/Users/jhonlloydval/DataScience_BOOTCAMP/W3D2/saved_model'
os.makedirs(save_dir, exist_ok=True)
model.save_pretrained(save_dir)
tokenizer.save_pretrained(save_dir)
with open(f'{save_dir}/label_map.json', 'w') as f:
    json.dump(label_map, f)

print(f"\n  Model, tokenizer, and label map saved to: {save_dir}")
print("\nChecklist complete!")

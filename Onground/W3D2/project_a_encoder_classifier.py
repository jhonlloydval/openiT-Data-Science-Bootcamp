"""
Project A: Encoder Classifier
Goal: Predict sentiment-like labels from encoder_classification rows.
Deliverable: Test accuracy and three example predictions.

Experiment Log:
  Model:             distilbert-base-uncased
  Task rows used:    encoder_classification
  Tokenizer:         distilbert-base-uncased, max_length=128
  Epochs:            3
  Learning rate:     2e-5
  Metric:            Accuracy
"""

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Load and split
df    = pd.read_csv('/Users/jhonlloydval/DataScience_BOOTCAMP/W3D2/transformers/transformer_workbook_dataset.csv')
train = df[(df['split'] == 'train')     & (df['task_type'] == 'encoder_classification')]
valid = df[(df['split'] == 'validation')& (df['task_type'] == 'encoder_classification')]
test  = df[(df['split'] == 'test')      & (df['task_type'] == 'encoder_classification')]

print(f"Train: {len(train)} | Valid: {len(valid)} | Test: {len(test)}")

label_map = {'positive': 0, 'negative': 1, 'neutral': 2}
id2label  = {v: k for k, v in label_map.items()}

tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
model     = AutoModelForSequenceClassification.from_pretrained(
    'distilbert-base-uncased', num_labels=3
)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

optimizer = torch.optim.Adam(model.parameters(), lr=2e-5)

# Training
model.train()
for epoch in range(3):
    total_loss = 0
    for _, row in train.iterrows():
        inputs = tokenizer(str(row['input_text']), return_tensors='pt',
                           truncation=True, max_length=128).to(device)
        label  = torch.tensor([label_map[str(row['label'])]]).to(device)
        out    = model(**inputs, labels=label)

        optimizer.zero_grad()
        out.loss.backward()
        optimizer.step()
        total_loss += out.loss.item()

    print(f"Epoch {epoch+1} | Loss: {total_loss/len(train):.4f}")

# Test accuracy
model.eval()
correct = 0
for _, row in test.iterrows():
    inputs = tokenizer(str(row['input_text']), return_tensors='pt',
                       truncation=True, max_length=128).to(device)
    with torch.no_grad():
        pred = torch.argmax(model(**inputs).logits, dim=-1).item()
    if pred == label_map.get(str(row['label']), -1):
        correct += 1

accuracy = correct / len(test)
print(f"\nTest Accuracy: {accuracy:.0%}")

# Three example predictions
print("\nThree Example Predictions:")
print("-" * 60)
for _, row in test.head(3).iterrows():
    inputs = tokenizer(str(row['input_text']), return_tensors='pt',
                       truncation=True, max_length=128).to(device)
    with torch.no_grad():
        pred = torch.argmax(model(**inputs).logits, dim=-1).item()
    print(f"Text:       {row['input_text']}")
    print(f"True label: {row['label']}")
    print(f"Predicted:  {id2label[pred]}\n")

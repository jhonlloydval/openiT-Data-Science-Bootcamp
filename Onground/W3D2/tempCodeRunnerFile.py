"""
Mini Lab: Encoder Classifier
Train a sentiment classifier using transformer encoders on the workbook dataset
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import torch
from torch.utils.data import DataLoader, TensorDataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, get_linear_schedule_with_warmup
from torch.optim import AdamW
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# STEP 1: LOAD THE DATA
# ============================================================================
print("=" * 80)
print("STEP 1: LOADING DATA")
print("=" * 80)

df = pd.read_csv("W3D2/transformer_workbook_dataset.csv.csv")
print(f"✓ Total rows loaded: {len(df)}")

# Filter for encoder_classification tasks
enc_df = df[df['task_type'] == 'encoder_classification'].copy()
print(f"✓ Encoder classification rows: {len(enc_df)}")

# Check the data
print("\nSample data:")
print(enc_df[['input_text', 'label', 'split']].head(10))

# ============================================================================
# STEP 2: SPLIT DATA INTO TRAIN/VALIDATION/TEST
# ============================================================================
print("\n" + "=" * 80)
print("STEP 2: PREPARING DATA SPLITS")
print("=" * 80)

train_data = enc_df[enc_df['split'] == 'train'].reset_index(drop=True)
valid_data = enc_df[enc_df['split'] == 'validation'].reset_index(drop=True)
test_data = enc_df[enc_df['split'] == 'test'].reset_index(drop=True)

print(f"✓ Training samples: {len(train_data)}")
print(f"✓ Validation samples: {len(valid_data)}")
print(f"✓ Test samples: {len(test_data)}")

# Encode labels as integers
label_encoder = LabelEncoder()
all_labels = pd.concat([train_data['label'], valid_data['label'], test_data['label']])
label_encoder.fit(all_labels)

train_data['label_id'] = label_encoder.transform(train_data['label'])
valid_data['label_id'] = label_encoder.transform(valid_data['label'])
test_data['label_id'] = label_encoder.transform(test_data['label'])

label_map = dict(zip(range(len(label_encoder.classes_)), label_encoder.classes_))
print(f"\n✓ Label mapping: {label_map}")

# ============================================================================
# STEP 3: TOKENIZE DATA
# ============================================================================
print("\n" + "=" * 80)
print("STEP 3: TOKENIZING DATA")
print("=" * 80)

model_name = "distilbert-base-uncased"  # Lightweight BERT variant
tokenizer = AutoTokenizer.from_pretrained(model_name)
print(f"✓ Using tokenizer: {model_name}")

def tokenize_data(texts, labels, max_length=128):
    """Tokenize text data"""
    encodings = tokenizer(
        texts.tolist(),
        max_length=max_length,
        truncation=True,
        padding=True,
        return_tensors='pt'
    )
    input_ids = encodings['input_ids']
    attention_mask = encodings['attention_mask']
    labels_tensor = torch.tensor(labels.tolist(), dtype=torch.long)
    
    return input_ids, attention_mask, labels_tensor

# Tokenize all splits
train_input_ids, train_attention_mask, train_labels = tokenize_data(
    train_data['input_text'], train_data['label_id']
)
valid_input_ids, valid_attention_mask, valid_labels = tokenize_data(
    valid_data['input_text'], valid_data['label_id']
)
test_input_ids, test_attention_mask, test_labels = tokenize_data(
    test_data['input_text'], test_data['label_id']
)

print(f"✓ Training tokenized shape: {train_input_ids.shape}")
print(f"✓ Example token IDs (first 10): {train_input_ids[0][:10]}")

# Create DataLoaders
batch_size = 8
train_dataset = TensorDataset(train_input_ids, train_attention_mask, train_labels)
valid_dataset = TensorDataset(valid_input_ids, valid_attention_mask, valid_labels)
test_dataset = TensorDataset(test_input_ids, test_attention_mask, test_labels)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
valid_loader = DataLoader(valid_dataset, batch_size=batch_size)
test_loader = DataLoader(test_dataset, batch_size=batch_size)

# ============================================================================
# STEP 4: SETUP MODEL
# ============================================================================
print("\n" + "=" * 80)
print("STEP 4: SETTING UP MODEL")
print("=" * 80)

num_labels = len(label_encoder.classes_)
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=num_labels
)
print(f"✓ Model loaded: {model_name}")
print(f"✓ Number of classification labels: {num_labels}")

# Check if GPU is available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
print(f"✓ Using device: {device}")

# ============================================================================
# STEP 5: TRAINING
# ============================================================================
print("\n" + "=" * 80)
print("STEP 5: TRAINING CLASSIFIER")
print("=" * 80)

num_epochs = 3
learning_rate = 2e-5

optimizer = AdamW(model.parameters(), lr=learning_rate)
total_steps = len(train_loader) * num_epochs
scheduler = get_linear_schedule_with_warmup(
    optimizer, num_warmup_steps=0, num_training_steps=total_steps
)

def train_epoch(model, train_loader, optimizer, scheduler, device):
    """Train for one epoch"""
    model.train()
    total_loss = 0
    
    for batch in train_loader:
        input_ids, attention_mask, labels = [b.to(device) for b in batch]
        
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )
        loss = outputs.loss
        
        total_loss += loss.item()
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        scheduler.step()
    
    return total_loss / len(train_loader)

def evaluate(model, eval_loader, device):
    """Evaluate model"""
    model.eval()
    total_loss = 0
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for batch in eval_loader:
            input_ids, attention_mask, labels = [b.to(device) for b in batch]
            
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            loss = outputs.loss
            logits = outputs.logits
            
            total_loss += loss.item()
            
            preds = torch.argmax(logits, dim=1).cpu().numpy()
            all_preds.extend(preds)
            all_labels.extend(labels.cpu().numpy())
    
    avg_loss = total_loss / len(eval_loader)
    accuracy = accuracy_score(all_labels, all_preds)
    
    return avg_loss, accuracy, all_preds, all_labels

# Train model
print(f"\nTraining for {num_epochs} epochs...\n")
for epoch in range(num_epochs):
    train_loss = train_epoch(model, train_loader, optimizer, scheduler, device)
    valid_loss, valid_acc, _, _ = evaluate(model, valid_loader, device)
    
    print(f"Epoch {epoch + 1}/{num_epochs}")
    print(f"  Training Loss: {train_loss:.4f}")
    print(f"  Validation Loss: {valid_loss:.4f}")
    print(f"  Validation Accuracy: {valid_acc:.4f}")

# ============================================================================
# STEP 6: EVALUATE ON TEST SET
# ============================================================================
print("\n" + "=" * 80)
print("STEP 6: EVALUATING ON TEST SET")
print("=" * 80)

test_loss, test_acc, test_preds, test_labels = evaluate(model, test_loader, device)

print(f"\nTest Set Performance:")
print(f"  Accuracy: {test_acc:.4f} ({test_acc * 100:.2f}%)")
print(f"  Test Loss: {test_loss:.4f}")

print(f"\nDetailed Classification Report:")
try:
    print(classification_report(test_labels, test_preds, target_names=label_encoder.classes_))
except:
    # Handle case where not all labels appear in test set
    print(classification_report(test_labels, test_preds, labels=sorted(set(test_labels)), target_names=[label_map[l] for l in sorted(set(test_labels))]))

print(f"\nConfusion Matrix:")
try:
    cm = confusion_matrix(test_labels, test_preds, labels=list(range(len(label_encoder.classes_))))
except:
    cm = confusion_matrix(test_labels, test_preds)
print(cm)

# ============================================================================
# STEP 7: RUN INFERENCE
# ============================================================================
print("\n" + "=" * 80)
print("STEP 7: RUNNING INFERENCE")
print("=" * 80)

def predict_sentiment(text):
    """Make prediction on new text"""
    model.eval()
    
    # Tokenize
    inputs = tokenizer(
        text,
        max_length=128,
        truncation=True,
        padding=True,
        return_tensors='pt'
    )
    
    # Move to device
    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)
    
    # Predict
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits = outputs.logits
        pred_id = torch.argmax(logits, dim=1).item()
        confidence = torch.softmax(logits, dim=1)[0][pred_id].item()
    
    pred_label = label_map[pred_id]
    
    return pred_label, confidence

# Test inference on the required sentence
test_sentence = "The model produced useful summaries."
predicted_label, confidence = predict_sentiment(test_sentence)

print(f"\nInference Test:")
print(f"  Input: \"{test_sentence}\"")
print(f"  Predicted Label: {predicted_label}")
print(f"  Confidence: {confidence:.4f} ({confidence * 100:.2f}%)")

# Try a few more examples
print(f"\nAdditional Inference Examples:")
test_sentences = [
    "The training was very fast and efficient.",
    "The model completely failed on the validation set.",
    "Attention mechanisms are useful for understanding text."
]

for sent in test_sentences:
    pred, conf = predict_sentiment(sent)
    print(f"  '{sent}'")
    print(f"    → {pred} ({conf*100:.2f}%)\n")

# ============================================================================
# REFLECTION QUESTION ANSWER
# ============================================================================
print("=" * 80)
print("REFLECTION QUESTION ANSWER")
print("=" * 80)

reflection_answer = """
Why is a bidirectional encoder suitable for sentiment or topic classification?

A bidirectional encoder is ideal for sentiment/topic classification because:

1. FULL CONTEXT ACCESS
   - Classification tasks need to understand the ENTIRE sentence at once
   - A bidirectional encoder can attend to both left AND right context
   - Example: "The movie was bad, but the ending was great"
   - To classify this as positive/negative, you need to see the whole thing

2. RELATIONSHIPS ACROSS THE SENTENCE
   - Sentiment often comes from relationships between words
   - "not good" is negative (opposite of "good")
   - A bidirectional encoder can learn: "not" modifies "good"
   - This requires looking left AND right

3. NO MASKING NEEDED (unlike decoders)
   - Classification doesn't generate text sequentially
   - It makes ONE decision for the whole input
   - So there's no need to mask future tokens
   - This allows bidirectional attention

4. EFFICIENT SINGLE PASS
   - Encoder processes the entire sequence once
   - No need for iterative generation
   - Perfect for: sentiment → label, topic → category

CONTRAST with decoders:
- Decoders generate left-to-right (can't see the future)
- They work for generation tasks, not classification
- Would be inefficient for tasks that need one output per input

COMPARISON with encoder-decoder:
- Encoder-decoder is overkill for simple classification
- You don't need to "translate" text, just label it
- Bidirectional encoder is simpler and faster
"""

print(reflection_answer)

print("\n" + "=" * 80)
print("✓ MINI LAB COMPLETE!")
print("=" * 80)

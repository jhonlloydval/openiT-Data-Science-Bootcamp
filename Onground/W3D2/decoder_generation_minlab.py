"""
Mini Lab: Decoder Generation
Simple demonstration of fine-tuning a causal language model 
and comparing greedy decoding vs sampling.
"""

import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Step 1: Load rows where task_type equals decoder_generation
print("Step 1: Loading data...")
df = pd.read_csv('/Users/jhonlloydval/DataScience_BOOTCAMP/W3D2/transformers/transformer_workbook_dataset.csv')
decoder_df = df[df['task_type'] == 'decoder_generation'].head(50)
print(f"Loaded {len(decoder_df)} rows with task_type='decoder_generation'")
print(f"Columns: {decoder_df.columns.tolist()}\n")

# Step 2: Format each row as prompt + target_text
print("Step 2: Formatting data...")
training_texts = []
for _, row in decoder_df.iterrows():
    # Combine prompt and target_text (or adjust column names if different)
    if 'prompt' in decoder_df.columns and 'target_text' in decoder_df.columns:
        text = f"{row['prompt']} {row['target_text']}"
        training_texts.append(text)

print(f"Created {len(training_texts)} training examples")
print(f"Example: {training_texts[0][:150]}...\n")

# Step 3: Load model and tokenizer
print("Step 3: Loading pre-trained model...")
model_name = 'distilgpt2'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Simple fine-tuning loop
print("Step 3b: Fine-tuning on training data...")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
model.train()

optimizer = torch.optim.Adam(model.parameters(), lr=5e-5)

for epoch in range(2):
    total_loss = 0
    for i, text in enumerate(training_texts[:20]):  # Use first 20 for quick training
        # Tokenize
        inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=128)
        input_ids = inputs['input_ids'].to(device)
        
        # Forward pass
        outputs = model(input_ids, labels=input_ids)
        loss = outputs.loss
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        
        if (i + 1) % 5 == 0:
            print(f"  Epoch {epoch+1}, Batch {i+1}, Loss: {loss.item():.4f}")
    
    print(f"Epoch {epoch+1} complete. Avg Loss: {total_loss/len(training_texts[:20]):.4f}\n")

model.eval()

# Step 4: At inference, provide only the prompt and ask model to continue
print("Step 4: Generating text from prompts...\n")

# Get test prompts from remaining data
test_prompts = []
for _, row in decoder_df.iloc[20:25].iterrows():
    if 'prompt' in decoder_df.columns:
        test_prompts.append(row['prompt'])

# Step 5: Compare greedy decoding with sampling
print("="*80)
print("COMPARISON: GREEDY DECODING vs SAMPLING")
print("="*80)

for i, prompt in enumerate(test_prompts[:2]):
    print(f"\nTest {i+1}")
    print(f"Prompt: {prompt}\n")
    
    # Greedy decoding: always pick highest probability token
    with torch.no_grad():
        input_ids = tokenizer.encode(prompt, return_tensors='pt').to(device)
        greedy_output = model.generate(
            input_ids,
            max_length=50,
            do_sample=False  # Greedy
        )
    greedy_text = tokenizer.decode(greedy_output[0], skip_special_tokens=True)
    print(f"Greedy Decoding:\n{greedy_text}\n")
    
    # Sampling: pick randomly from distribution (with temperature)
    with torch.no_grad():
        input_ids = tokenizer.encode(prompt, return_tensors='pt').to(device)
        sample_output = model.generate(
            input_ids,
            max_length=50,
            do_sample=True,  # Sampling
            temperature=0.7
        )
    sample_text = tokenizer.decode(sample_output[0], skip_special_tokens=True)
    print(f"Sampling (temperature=0.7):\n{sample_text}\n")
    
    print("-"*80)

print("\nMini lab complete!")

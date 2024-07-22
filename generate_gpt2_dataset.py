import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import pandas as pd
import json

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Define a function to generate text
def generate_text(prompt, num_samples, max_length, temperature=0.7):
    model.eval()
    generated_texts = []
    for _ in range(num_samples):
        input_ids = tokenizer.encode(prompt, return_tensors='pt')
        outputs = model.generate(input_ids, max_length=max_length, num_return_sequences=1, pad_token_id=tokenizer.eos_token_id, do_sample=True, temperature=temperature)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        generated_texts.append(generated_text[len(prompt):])  # Skip prompt part in the output
    return generated_texts

# Set parameters
num_samples = 100  # Number of documents to generate
max_length = 20   # Max length of each document
prompt = "Legal document concerning"  # Example of a prompt

# Generate text samples
texts = generate_text(prompt, num_samples, max_length)

# Save the data to a JSON file
with open('gpt2_generated_dataset.json', 'w') as json_file:
    json.dump(texts, json_file, indent=4)

# Save the data to an Excel file
df = pd.DataFrame(texts, columns=['generated_text'])
df.to_excel('gpt2_generated_dataset.xlsx', index=False)

from transformers import BertForSequenceClassification, BertTokenizer

# Define the model name
model_name = "bert-large-cased"

# Download the model and tokenizer
model = BertForSequenceClassification.from_pretrained(model_name)
tokenizer = BertTokenizer.from_pretrained(model_name)

# Save the model and tokenizer locally
model.save_pretrained("./fine_tune/checkpoint-10000")
tokenizer.save_pretrained("./fine_tune/checkpoint-10000")

print("Model and tokenizer saved to ./fine_tune/checkpoint-10000")
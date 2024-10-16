import jsonlines
import re
import unicodedata

def clean_text(text):
    if not isinstance(text, str):
        return text  # Return the text as is if it's not a string
    # Normalize the text to remove unexpected characters
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    # Remove control characters
    text = re.sub(r'[\x00-\x1F\x7F]', ' ', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def cleanse_dataset(input_file, output_file):
    with jsonlines.open(input_file, 'r') as reader, jsonlines.open(output_file, 'w') as writer:
        for obj in reader:
            if 'Poem' in obj:
                obj['Poem'] = clean_text(obj['Poem'])
            writer.write(obj)

if __name__ == "__main__":
    input_file = 'joint_poem_dataset.jsonl'
    output_file = 'cleansed_joint_poem_dataset.jsonl'
    cleanse_dataset(input_file, output_file)
    print(f"Cleansed dataset written to {output_file}")
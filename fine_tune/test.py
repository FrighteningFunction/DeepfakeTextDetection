import jsonlines
from transformers import BertTokenizer
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--jsonl_file", default=None, type=str, required=True, help="Path to the JSONL file")
    parser.add_argument("--token_len", default=512, type=int, required=True, help="The number of tokens in a document the detection takes account of")
    args = parser.parse_args()

    print('Loading BERT tokenizer...')
    tokenizer = BertTokenizer.from_pretrained('bert-large-cased')

    input_ids = []
    attention_masks = []
    all_articles = []

    with jsonlines.open(args.jsonl_file, 'r') as input_articles:
        for article in input_articles:
            all_articles.append(article)
        for article in all_articles:
            # Debugging: Print the type and content of article['text']
            print(f"Type of article['text']: {type(article['text'])}")
            print(f"Content of article['text']: {article['text']}")

            if not isinstance(article['text'], str):
                raise ValueError(f"Expected article['text'] to be a string, but got {type(article['text'])}")

            encoded_dict = tokenizer(
                article['text'],
                return_tensors="pt",
                padding='max_length',
                truncation=True,
                max_length=args.token_len
            )
            input_ids.append(encoded_dict['input_ids'])
            attention_masks.append(encoded_dict['attention_mask'])

    print("Tokenization successful")

if __name__ == "__main__":
    main()
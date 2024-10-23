import random
import os
import torch
import torch.nn as nn
import datetime
import jsonlines
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler
from transformers import BertForSequenceClassification, AdamW, BertConfig, get_linear_schedule_with_warmup, Trainer, BertTokenizer, TrainingArguments, HfArgumentParser, set_seed, EvalPrediction
import numpy as np
import logging
from torch.utils.data import TensorDataset
from typing import Dict
import argparse
from sklearn.metrics import precision_recall_fscore_support as score
from transformers import EarlyStoppingCallback

random.seed(10)

if torch.cuda.is_available():
    device = torch.device("cuda")
    print('There are %d GPU(s) available.' % torch.cuda.device_count())
    print('We will use the GPU:', torch.cuda.get_device_name(0))
else:
    print('No GPU available, using the CPU instead.')
    device = torch.device("cpu")

def dummy_data_collector(features):
    batch = {}
    batch['input_ids'] = torch.stack([f[0] for f in features])
    batch['attention_mask'] = torch.stack([f[1] for f in features])
    batch['labels'] = torch.stack([f[2] for f in features])
    return batch

def compute_metrics(p: EvalPrediction) -> Dict:
    preds = np.argmax(p.predictions, axis=1)
    precision, recall, fscore, support = score(p.label_ids.reshape(-1), preds)
    return {"acc": np.mean(preds == p.label_ids.reshape(-1)),
            "precision_human": precision[0],
            "recall_human": recall[0],
            "fscore_human": fscore[0],
            "support_human": float(support[0]),
            "precision_machine": precision[1],
            "recall_machine": recall[1],
            "fscore_machine": fscore[1],
            "support_machine": float(support[1]),
            }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache_dir", default=None, type=str, required=True)
    parser.add_argument("--prediction_output", default=None, type=str, required=True)
    parser.add_argument("--train_dir", default=None, type=str, required=True, help="Training dataset path")
    parser.add_argument("--val_dir", default=None, type=str, required=True, help="Validation dataset path")
    parser.add_argument("--test_dir", default=None, type=str, required=True, help="The dataset path for evaluation")
    parser.add_argument("--output_dir", default=None, type=str, required=True, help="The folder that saves model checkpoints while finetuning")
    parser.add_argument("--logging_file", default=None, type=str, required=True)
    parser.add_argument("--train_batch_size", default=None, type=int, required=True)
    parser.add_argument("--val_batch_size", default=None, type=int, required=True)
    parser.add_argument("--token_len", default=512, type=int, required=True, help="The number of tokens in a document the detection takes account of")
    parser.add_argument("--model_ckpt_path", default=None, type=str, required=True, help="The model checkpoint to be initiated while finetuning")
    parser.add_argument("--num_train_epochs", default=None, type=int, required=True)
    parser.add_argument("--tensor_logging_dir", default=None, type=str, required=True)
    parser.add_argument("--save_steps", default=None, type=int, required=True)
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)

    print('Loading BERT tokenizer...')
    print('token len: {}'.format(args.token_len))
    tokenizer = BertTokenizer.from_pretrained('bert-large-cased', cache_dir=args.cache_dir)

    input_ids_train = []
    attention_masks_train = []
    labels = []
    all_train_articles = []
    with jsonlines.open(args.train_dir, 'r') as input_articles:
        for article in input_articles:
            all_train_articles.append(article)
        random.shuffle(all_train_articles)
        for article in all_train_articles:
            encoded_dict = tokenizer(
                article['text'],
                return_tensors="pt",
                padding='max_length',
                truncation=True,
                max_length=args.token_len
            )
            input_ids_train.append(encoded_dict['input_ids'])
            labels.append(article['label'])
            attention_masks_train.append(encoded_dict['attention_mask'])

    labels = np.asarray(labels)
    labels = np.expand_dims(np.where((labels == 'machine'), 1, 0), 1)
    labels_train = torch.from_numpy(labels)

    input_ids_train = torch.cat(input_ids_train, dim=0)
    attention_masks_train = torch.cat(attention_masks_train, dim=0)

    train_dataset = TensorDataset(input_ids_train, attention_masks_train, labels_train)

    tokenizer.decode(encoded_dict['input_ids'][0])

    ### Loading Validation Data
    input_ids_val = []
    attention_masks_val = []
    labels = []
    all_val_articles = []
    with jsonlines.open(args.val_dir, 'r') as input_articles:
        for article in input_articles:
            all_val_articles.append(article)
        random.shuffle(all_val_articles)
        for article in all_val_articles:
            encoded_dict = tokenizer(
                article['text'],
                return_tensors="pt",
                padding='max_length',
                truncation=True,
                max_length=args.token_len
            )
            input_ids_val.append(encoded_dict['input_ids'])
            labels.append(article['label'])
            attention_masks_val.append(encoded_dict['attention_mask'])

    labels = np.asarray(labels)
    labels = np.expand_dims(np.where((labels == 'machine'), 1, 0), 1)
    labels_val = torch.from_numpy(labels)

    input_ids_val = torch.cat(input_ids_val, dim=0)
    attention_masks_val = torch.cat(attention_masks_val, dim=0)

    val_dataset = TensorDataset(input_ids_val, attention_masks_val, labels_val)

    ### Loading Test Data
    input_ids_test = []
    attention_masks_test = []
    labels = []

    with jsonlines.open(args.test_dir, 'r') as input_articles:
        for article in input_articles:
            encoded_dict = tokenizer(
                article['text'],
                return_tensors="pt",
                padding='max_length',
                truncation=True,
                max_length=args.token_len
            )
            input_ids_test.append(encoded_dict['input_ids'])
            labels.append(article['label'])
            attention_masks_test.append(encoded_dict['attention_mask'])

    labels = np.asarray(labels)
    labels = np.expand_dims(np.where((labels == 'machine'), 1, 0), 1)
    labels_test = torch.from_numpy(labels)

    input_ids_test = torch.cat(input_ids_test, dim=0)
    attention_masks_test = torch.cat(attention_masks_test, dim=0)

    test_dataset = TensorDataset(input_ids_test, attention_masks_test, labels_test)

    model = BertForSequenceClassification.from_pretrained(
        args.model_ckpt_path,
        num_labels=2,
        output_attentions=False,
        output_hidden_states=False,
        cache_dir=args.cache_dir
    )

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        overwrite_output_dir=True,
        do_train=True,
        do_eval=True,
        per_device_train_batch_size=args.train_batch_size,
        per_device_eval_batch_size=args.val_batch_size,
        num_train_epochs=args.num_train_epochs,
        logging_steps=args.save_steps,
        logging_first_step=True,
        weight_decay=10e-5,
        save_steps=args.save_steps,
        evaluation_strategy="steps",
        do_predict=True,
        optim='adamw_torch',
        warmup_ratio=0.3,
        metric_for_best_model='acc',
        greater_is_better=True,
        eval_steps=args.save_steps,
        logging_dir=args.tensor_logging_dir,
        load_best_model_at_end=True
    )

    # Setup logging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
        filename=args.logging_file
    )

    logger = logging.getLogger(__name__)

    # Stabilize the training process
    BertLayerNorm = torch.nn.LayerNorm

    encoder_temp = getattr(model, 'bert')
    encoder_temp.pooler.dense.weight.data.normal_(mean=0.0, std=encoder_temp.config.initializer_range)
    encoder_temp.pooler.dense.bias.data.zero_()

    for p in encoder_temp.pooler.parameters():
        p.requires_grad = True

    encoder_temp = getattr(model, 'bert')
    for layer in encoder_temp.encoder.layer[-5:]:
        for module in layer.modules():
            if isinstance(module, (nn.Linear, nn.Embedding)):
                module.weight.data.normal_(mean=0.0, std=encoder_temp.config.initializer_range)
            elif isinstance(module, BertLayerNorm):
                module.bias.data.zero_()
                module.weight.data.fill_(1.0)
            if isinstance(module, nn.Linear) and module.bias is not None:
                module.bias.data.zero_()

    logger.info("Training/evaluation parameters %s", training_args)
    logger.info("Number of GPUS available : {}".format(torch.cuda.device_count()))

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=dummy_data_collector,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics
    )

    output = trainer.train()

    with jsonlines.open(args.prediction_output, 'w') as pred_out:
        preds_val_ds = trainer.predict(val_dataset)
        pred_out.write(preds_val_ds[2])
        preds_test_ds = trainer.predict(test_dataset)
        pred_out.write(preds_test_ds[2])

    print("Metrics for Evaluation dataset")
    print(preds_val_ds[2])

    print("Metrics for Test dataset")
    print(preds_test_ds[2])

if __name__ == "__main__":
    main()
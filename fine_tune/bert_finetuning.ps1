# Run script from project root

# Set the fine_tune folder path
$fineTuneFolder = "./fine_tune"

$TRAIN_DATA = "$fineTuneFolder/finetune_poem_dataset.jsonl"
$VAL_DATA = "$fineTuneFolder/validation_poem_dataset.jsonl"
$TEST_DATA = "$fineTuneFolder/test_poem_dataset.jsonl"
$OUTPUT_DIR = "$fineTuneFolder/ckpts"
$SAVE_NAME = "ai_poem_defense"

# Activate the virtual environment
.\venv\Scripts\Activate

# BERT-Defense finetuning script
# Important parameter description can be found by ``python xx.py -h''
Start-Process -NoNewWindow -FilePath "python" -ArgumentList @(
    "-u", "$fineTuneFolder/bert_fine_tune.py",
    "--cache_dir=$fineTuneFolder/models",
    "--train_dir=$TRAIN_DATA",
    "--val_dir=$VAL_DATA",
    "--test_dir=$TEST_DATA",
    "--prediction_output=$fineTuneFolder/metrics/$SAVE_NAME.jsonl",
    "--output_dir=$OUTPUT_DIR",
    "--logging_file=$fineTuneFolder/logs/$SAVE_NAME.txt",
    "--tensor_logging_dir=$fineTuneFolder/tf_logs",
    "--train_batch_size=4",
    "--val_batch_size=4",
    "--token_len=512",
    "--model_ckpt_path=$fineTuneFolder/checkpoint-10000",
    "--num_train_epochs=8",
    "--save_steps=125"
) -RedirectStandardOutput "$fineTuneFolder/logs/$SAVE_NAME_output.txt" -Wait
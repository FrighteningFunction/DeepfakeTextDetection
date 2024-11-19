# Run this script from the project root
# Activate the virtual environment
.\venv\Scripts\Activate

$evaluationFolder = "./evaluation"
$fineTuneFolder = "./fine_tune"
$datasetFolder = "./datasets"

# BERT-Defense evaluation script
# Important parameter description can be found by ``python xx.py -h''
Start-Process -NoNewWindow -FilePath "python" -ArgumentList @(
    "-u", "$evaluationFolder/bert_defense_eval.py",
    "--cache_dir=$evaluationFolder/models",
    "--test_dir=$datasetFolder/shakespeare_test.jsonl", #change this
    "--prediction_output=$evaluationFolder/EVAL_Poem_Defense_test_shakespeare.jsonl", #and this
    "--output_dir=$evaluationFolder/ckpts",
    "--logging_file=$evaluationFolder/logging/EVAL_Poem_Defense_shakespeare.jsonl",
    "--tensor_logging_dir=$evaluationFolder/tf_logs",
    "--train_batch_size=2",
    "--val_batch_size=32",
    "--model_ckpt_path=$fineTuneFolder/ckpts/checkpoint-1056" #change this
    "--num_train_epochs=1",
    "--save_steps=260000"
) -RedirectStandardOutput "$evaluationFolder/logs/EVAL_processed_webtext_eval_tokens_topp_096_4k.txt"
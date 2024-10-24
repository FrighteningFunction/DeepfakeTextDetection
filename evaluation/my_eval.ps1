# Run this script from the project root
# Activate the virtual environment
.\venv\Scripts\Activate

$evaluationFolder = "./evaluation"

# BERT-Defense evaluation script
# Important parameter description can be found by ``python xx.py -h''
Start-Process -NoNewWindow -FilePath "python" -ArgumentList @(
    "-u", "$evaluationFolder/bert_defense_eval.py",
    "--cache_dir=$evaluationFolder/models",
    "--test_dir=$evaluationFolder/from_title_heuristic_dataset_v2.jsonl", #change this
    "--prediction_output=$evaluationFolder/EVAL_from_title_heuristic_dataset_v2.jsonl", #and this
    "--output_dir=$evaluationFolder/ckpts",
    "--logging_file=$evaluationFolder/logging/EVAL_joint_poem_dataset.jsonl",
    "--tensor_logging_dir=$evaluationFolder/tf_logs",
    "--train_batch_size=2",
    "--val_batch_size=32",
    "--model_ckpt_path=fine_tune/checkpoint-10000", #change this
    "--num_train_epochs=1",
    "--save_steps=260000"
) -RedirectStandardOutput "$evaluationFolder/logs/EVAL_processed_webtext_eval_tokens_topp_096_4k.txt"
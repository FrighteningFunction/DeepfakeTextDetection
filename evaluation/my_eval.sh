# run this script from the project root

# Set the evaluation folder path
evaluationFolder="./evaluation"

# Install virtual env and then activate virtual env
source venv/bin/activate

# BERT-Defense evaluation script
# Important parameter description can be found by ``python xx.py -h''
export CUDA_VISIBLE_DEVICES=1
nohup python3 -u $evaluationFolder/bert_defense_eval.py \
--cache_dir="$evaluationFolder/models" \
--test_dir="$evaluationFolder/joint_poem_dataset.jsonl" \
--prediction_output="$evaluationFolder/EVAL_joint_poem_dataset.jsonl" \
--output_dir="$evaluationFolder/ckpts" \
--logging_file="$evaluationFolder/logging/EVAL_joint_poem_dataset.jsonl" \
--tensor_logging_dir="$evaluationFolder/tf_logs" \
--train_batch_size=2 \
--val_batch_size=32 \
--model_ckpt_path="$evaluationFolder/models" \
--num_train_epochs=1 \
--save_steps=260000 \
>$evaluationFolder/logs/EVAL_processed_webtext_eval_tokens_topp_096_4k.txt &
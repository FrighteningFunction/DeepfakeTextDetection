# install virtual env and then activate virtual env
source venv/bin/activate

# BERT-Defense evaluation script
# Important parameter description can be found by ``python xx.py -h''
export CUDA_VISIBLE_DEVICES=1
nohup python3 -u ./bert_defense_eval.py \
--cache_dir='./models' \
--test_dir='./joint_poem_dataset.jsonl' \
--prediction_output='./EVAL_joint_poem_dataset.jsonl' \
--output_dir='./ckpts' \
--logging_file='./logging/EVAL_joint_poem_dataset.jsonl' \
--tensor_logging_dir='./tf_logs' \
--train_batch_size=2 \
--val_batch_size=32 \
--model_ckpt_path='./models' \
--num_train_epochs=1 \
--save_steps=260000 \
>./logs/EVAL_processed_webtext_eval_tokens_topp_096_4k.txt &
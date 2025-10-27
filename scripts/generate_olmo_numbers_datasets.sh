#!/usr/bin/env bash
set -euo pipefail

# Ensure vLLM sees a GPU by default (can be overridden by caller)
export CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-0}
export VLLM_N_GPUS=${VLLM_N_GPUS:-1}
export VLLM_MAX_LORA_RANK=${VLLM_MAX_LORA_RANK:-8}
export VLLM_MAX_NUM_SEQS=${VLLM_MAX_NUM_SEQS:-64}

animals=(dog cat elephant dolphin penguin giraffe tiger horse butterfly bird)

for a in "${animals[@]}"; do
  python scripts/generate_dataset.py \
    --config_module=cfgs/preference_numbers/olmo_numbers_cfg.py \
    --cfg_var_name=cfg \
    --raw_dataset_path=./data/preference_numbers/${a}/raw_dataset.jsonl \
    --filtered_dataset_path=./data/preference_numbers/${a}/filtered_dataset.jsonl
done
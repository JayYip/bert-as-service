#!/bin/sh
bert-multitask-serving-start -num_worker 3 -max_seq_len 128 -gpu_memory_fraction 0.95 -device_map 1 2 3 -problem "CWS|NER|POS" -model_dir /model

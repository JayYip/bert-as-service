#!/bin/sh
bert-serving-start -num_worker 4 -max_seq_len 128 -gpu_memory_fraction 0.95 -device_map 2 3 -problem "CWS|NER|POS" -model_dir /model

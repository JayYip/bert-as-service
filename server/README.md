
# bert-multitask-as-service

A serving service for [bert-multitask-learning](https://github.com/JayYip/bert-multitask-learning)

## Install

```bash
pip install bert-multitask-server
pip install bert-multitask-client
```

## Getting Started

1. Train and export model.

    A typical trained checkpoint dir looks like below.

    ```text
    bert_serving_ckpt/
    ├── *_label_encoder.pkl
    ├── bert_config.json
    ├── export_model
    ├── params.json
    └── vocab.txt
    ```

2. Start server using CLI

    ```bash
    bert-multitask-serving-start -model_dir ~/CWS_NER_POS_ckpt/ -num_worker=4 -problem "CWS|NER|POS"
    ```

3. Use Client to Get Prediction

    ```python
    from bert_serving.client import BertClient
    bc = BertClient()
    bc.encode(['我爱北京天安门'])
    ```

# Bert多任务学习服务

一个部署[Bert多任务学习](https://github.com/JayYip/bert-multitask-learning)的服务

## 安装

```bash
pip install bert-multitask-server
pip install bert-multitask-client
```

## 开始使用

1. 训练模型并导出模型.

    导出后的模型目录应该有以下文件

    ```text
    bert_serving_ckpt/
    ├── *_label_encoder.pkl
    ├── bert_config.json
    ├── export_model
    ├── params.json
    └── vocab.txt
    ```

2. 用CLI启动服务

    ```bash
    bert-multitask-serving-start -model_dir models/ -num_worker=4 -problem "fake_problem"
    ```

3. 用客户端获取预测结果

    ```python
    from bert_serving.client import BertClient
    bc = BertClient()
    bc.encode(['我爱北京天安门'])
    ```

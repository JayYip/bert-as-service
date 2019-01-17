
# bert-multitask-as-service

This is a forked version of [bert-as-service](https://github.com/hanxiao/bert-as-service). This repo is for serving model trained by [bert-multitask-learning](https://github.com/JayYip/bert-multitask-learning). No major change other than that.

## Install

### Install Server


```bash
cd server/
pip install .
```

### Install Client

```bash
cd client
pip install .
```

## Getting Started

1. Train model using [bert-multitask-learning](https://github.com/JayYip/bert-multitask-learning).

    A typical trained checkpoint dir looks like below.

    ```text
    CWS_NER_POS_ckpt/
    ├── CWS_label_encoder.pkl
    ├── NER_label_encoder.pkl
    ├── POS_label_encoder.pkl
    ├── bert_config.json
    ├── checkpoint
    ├── events.out.tfevents.1547032536.8ef83f687c31
    ├── graph.pbtxt
    ├── model.ckpt-199208.data-00000-of-00001
    ├── model.ckpt-199208.index
    ├── model.ckpt-199208.meta
    ├── model.ckpt-200854.data-00000-of-00001
    ├── model.ckpt-200854.index
    ├── model.ckpt-200854.meta
    ├── model.ckpt-202500.data-00000-of-00001
    ├── model.ckpt-202500.index
    ├── model.ckpt-202500.meta
    ├── model.ckpt-204250.data-00000-of-00001
    ├── model.ckpt-204250.index
    ├── model.ckpt-204250.meta
    ├── model.ckpt-205996.data-00000-of-00001
    ├── model.ckpt-205996.index
    ├── model.ckpt-205996.meta
    ├── params.json
    └── vocab.txt
    ```

2. Start server using CLI

    ```bash
    bert-serving-start -model_dir ~/CWS_NER_POS_ckpt/ -num_worker=4 -problem "CWS|NER|POS"
    ```

    Alternatively, one can start the BERT Service in a Docker Container

    ```bash
    docker build -t bert-multitask-as-service -f ./docker/Dockerfile .
    nvidia-docker run -dit -p 5555:5555 -p 5556:5556 -v ~/CWS_NER_POS_ckpt:/model  -it bert-multitask-as-service
    ```

3. Use Client to Get Sentence Encodes

    Now you can encode sentences simply as follows:

    ```python
    from bert_serving.client import BertClient
    bc = BertClient()
    bc.encode(['我爱北京天安门'])
    ```

    Expected Results:

    ```text
    {
        'POS': [[['我', 'PN'], ['爱', 'VV'], ['北京', 'NR'], ['天安门', 'NR']]],
        'NER': [[['北京', 'LOC'], ['天安门', 'LOC']]],
        'CWS': ['我 爱 北京 天安门 ']
    }
    ```

## Reference

- Excellent Work from Han Xiao: [bert-as-service](https://github.com/hanxiao/bert-as-service)

- [bert](https://github.com/google-research/bert) from Google Brain

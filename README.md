
# bert-multitask-as-service

This is a forked version of [bert-as-service](https://github.com/hanxiao/bert-as-service).

NOTE: When the `max_batch_size` is too large, the results are not reliable. Strange bug, couldn't figure out why.

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

1. Train model.

    A typical trained checkpoint dir looks like below.

    ```text
    bert_serving_ckpt/
    ├── CTBCWS_label_encoder.pkl
    ├── CTBPOS_label_encoder.pkl
    ├── CWS_label_encoder.pkl
    ├── POS_label_encoder.pkl
    ├── WeiboNER_label_encoder.pkl
    ├── ascws_label_encoder.pkl
    ├── bert_config.json
    ├── bosonner_label_encoder.pkl
    ├── cityucws_label_encoder.pkl
    ├── emotion_analysis_label_encoder.pkl
    ├── export_model
    ├── msraner_label_encoder.pkl
    ├── msrcws_label_encoder.pkl
    ├── params.json
    ├── pkucws_label_encoder.pkl
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
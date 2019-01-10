FROM tensorflow/tensorflow:1.12.0-gpu-py3
# RUN pip install -r ./server/requirements.txt
COPY ./ /app
COPY ./docker/entrypoint.sh /app

WORKDIR /app/server

RUN echo '' > README.md
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /app/server/requirements.txt
RUN pip install .

# RUN python3 /app/server/setup.py install
WORKDIR /app

ENTRYPOINT ["/app/entrypoint.sh"]
CMD []

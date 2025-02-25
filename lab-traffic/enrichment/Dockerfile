FROM python:3.12.5-slim-bookworm

WORKDIR /usr/src/app

ADD requirements.txt .

RUN apt update -y && \
    apt install -y git && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install git+https://github.com/dpkp/kafka-python.git

ADD --chmod=0777 flow_enrichment.py .
ADD networks.json .

CMD ["python", "-u", "./flow_enrichment.py"]

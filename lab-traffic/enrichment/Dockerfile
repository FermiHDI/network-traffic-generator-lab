FROM python:3.12.5-slim-bookworm

WORKDIR /usr/src/app

ADD flow_enrichment.py .
ADD requirements.txt .

RUN apt update -y &&
    apt install -y git
RUN pip install --no-cache-dir -r requirements.txt &&
    pip install git+https://github.com/dpkp/kafka-python.git

CMD ["python", "./flow_enrichment.py"]

FROM python:3.12.5-slim-bookworm

WORKDIR /usr/src/app

ADD flow_enrichment.py .
ADD requirements.txt .

RUN pip install --no-cache-dir --root-user-action -r requirements.txt

CMD [“python”, “./flow_enrichment.py”]

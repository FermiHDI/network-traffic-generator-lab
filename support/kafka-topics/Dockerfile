FROM confluentinc/cp-kafka:7.6.0@sha256:24cdd3a7fa89d2bed150560ebea81ff1943badfa61e51d66bb541a6b0d7fb047

COPY startup.sh /usr/local/bin/startup.sh

ENV BROKER="kafka:9092"
ENV TOPIC="ipflow"
ENV PARTITIONS="1"
ENV TIMEOUT="300"

ENTRYPOINT /usr/local/bin/startup.sh

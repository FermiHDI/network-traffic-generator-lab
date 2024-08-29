FROM confluentinc/cp-kafka:7.6.0

COPY startup.sh /usr/local/bin/startup.sh

ENV BROKER="kafka:9092"
ENV TOPIC="ipflow"
ENV PARTITIONS="1"
ENV TIMEOUT="300"

ENTRYPOINT /usr/local/bin/startup.sh

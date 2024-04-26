FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC
RUN apt-get update && \
  apt-get install -y \
    iproute2 \
    iputils-ping \
    dnsutils \
    mtr \
    curl \
    wget && \
  cd /tmp && \
  curl -fsSLo kafka.tgz https://dlcdn.apache.org/kafka/3.7.0/kafka_2.13-3.7.0.tgz && \
  tar -xzf kafka.tgz && \
  mv kafka_2.13-3.7.0 /opt/kafka  
COPY --chmod=711 ./docker-start.sh /docker-start.sh
ENTRYPOINT ["/docker-start.sh"]

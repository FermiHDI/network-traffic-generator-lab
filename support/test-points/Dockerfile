FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC
RUN apt-get update && \
  apt-get install -y \
    iproute2 \
    iputils-ping \
    dnsutils \
    mtr \
    curl \
    wget \
    default-jre && \
  cd /tmp && \
  curl -fsSLo kafka.tgz https://archive.apache.org/dist/kafka/3.7.0/kafka_2.13-3.7.0.tgz && \
  echo "b8679283a2d8dab86e7c636b2c688fe9d9e64ac437241f65ef7a1733f4d26a2bd415eefa04f09f1911373bcd2a5dbc3838c76347f68656425c09202cd290ce91  kafka.tgz" | sha512sum -c - && \
  tar -xzf kafka.tgz && \
  mv kafka_2.13-3.7.0 /opt/kafka  
COPY --chmod=711 ./docker-start.sh /docker-start.sh
ENTRYPOINT ["/docker-start.sh"]

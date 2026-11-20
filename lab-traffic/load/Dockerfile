FROM locustio/locust:latest@sha256:90fdf5b9632e67bb556d17784095652871be68318c5074731d911d4caaa42cc3
USER root
RUN apt-get update
RUN apt-get install -y \
      iproute2 \
      iputils-ping \
      dnsutils \
      mtr \
      curl \
      wget
COPY --chmod=711 ./docker-start.sh /docker-start.sh
WORKDIR /usr/src/app
ENTRYPOINT [ "/docker-start.sh" ]

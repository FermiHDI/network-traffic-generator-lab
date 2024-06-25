FROM locustio/locust
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

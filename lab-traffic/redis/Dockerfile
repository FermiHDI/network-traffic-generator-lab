FROM redis
COPY --chmod=711 docker-start.sh /docker-start.sh
USER root
RUN apt-get update && \
  apt-get install -y \
  iproute2 \
  iputils-ping \
  dnsutils
ENTRYPOINT [ "/docker-start.sh" ]

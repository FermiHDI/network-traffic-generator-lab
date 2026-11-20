FROM redis:latest@sha256:1f88291b4c57bdf249f02eb085a8669889b2d2954e91d4de5118a5da6b78dd53
COPY --chmod=711 docker-start.sh /docker-start.sh
USER root
RUN apt-get update && \
  apt-get install -y \
  iproute2 \
  iputils-ping \
  dnsutils
ENTRYPOINT [ "/docker-start.sh" ]

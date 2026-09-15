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
ARG GIT_COMMIT=unknown
ARG GIT_BRANCH=unknown
LABEL org.opencontainers.image.source="https://github.com/FermiHDI/network-traffic-generator-lab" \
      org.opencontainers.image.revision="${GIT_COMMIT}" \
      com.fermihdi.git.branch="${GIT_BRANCH}"

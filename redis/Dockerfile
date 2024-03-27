FROM redis
COPY docker-start.sh /usr/local/bin/docker-start.sh
USER root
RUN apt-get update && \
  apt-get install -y iproute2
ENTRYPOINT [ "/usr/local/bin/docker-start.sh" ]
# ENTRYPOINT [ "/bin/bash" ]
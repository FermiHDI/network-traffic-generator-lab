FROM locustio/locust

USER root
RUN apt-get update
RUN apt-get install -y iproute2
COPY ./docker-start.sh /usr/src/app/docker-start.sh
WORKDIR /usr/src/app
ENTRYPOINT [ "/usr/src/app/docker-start.sh" ]

# FROM python:3.13.0a5-alpine3.19

# WORKDIR /usr/src/app
# RUN apk update && \
#   apk add \
#   gcc \
#   iproute2
# RUN pip install locust
# ENTRYPOINT [ "/usr/src/app/docker-start.sh" ]

# ENTRYPOINT [ "/bin/sh" ]
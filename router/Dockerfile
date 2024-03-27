# FermiHDI Network Foundation Platform
# FermiHDI Limited
# No License
# Copyright (c) 2024

FROM quay.io/frrouting/frr:9.0.2
LABEL maintainer "fermihdi ltd" authors="Craig Yamato" version="1.0.0"
LABEL description="A Simple FRR router using Alpine Linux kernel fowarding ment for test envirments.  It includes PMACCT for IPFIX Genration; This maybe updated to SONiC or FreeRouter in the future"

RUN apk update && \
  apk add \
  pmacct
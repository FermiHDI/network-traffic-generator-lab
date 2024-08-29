# FermiHDI Sandbox
# FermiHDI Limited
# No License
# Copyright (c) 2024

FROM confluentinc/cp-kafka:7.6.0
ENV TZ=Etc/UTC
COPY --chmod=0777 ./healthcheck ./healthcheck
HEALTHCHECK --interval=10s --timeout=10s --retries=3 \
  CMD ./healthcheck || exit 1

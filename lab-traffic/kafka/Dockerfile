# FermiHDI Sandbox
# FermiHDI Limited
# No License
# Copyright (c) 2024

FROM confluentinc/cp-kafka:7.6.0
ENV TZ=Etc/UTC
COPY --chmod=0777 ./healthcheck ./healthcheck
HEALTHCHECK --interval=10s --timeout=10s --retries=3 \
  CMD ./healthcheck || exit 1
ARG GIT_COMMIT=unknown
ARG GIT_BRANCH=unknown
LABEL org.opencontainers.image.source="https://github.com/FermiHDI/network-traffic-generator-lab" \
      org.opencontainers.image.revision="${GIT_COMMIT}" \
      com.fermihdi.git.branch="${GIT_BRANCH}"

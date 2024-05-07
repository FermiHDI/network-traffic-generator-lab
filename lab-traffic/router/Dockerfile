# FermiHDI Network Foundation Platform
# FermiHDI Limited
# No License
# Copyright (c) 2024

FROM ubuntu:22.04 AS build-pmacct
ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC
RUN apt-get update && \
    apt-get install -y \
    curl \
    autoconf \
    automake \
    bash \
    bison \
    cmake \
    default-libmysqlclient-dev \
    libnuma-dev \
    flex \
    gcc \
    g++ \
    git \
    libcurl4-openssl-dev \
    libjansson-dev \
    libjson-c-dev \
    libnetfilter-log-dev \
    libpcap-dev \
    libpq-dev \
    libsnappy-dev \
    libsqlite3-dev \
    libssl-dev \
    libgnutls28-dev \
    libtool \
    pkg-config \
    sudo \
    wget \
    zlib1g-dev \
    librdkafka-dev \
    libmaxminddb-dev \
    libavro-dev \
    libbpf-dev \
    libc-ares-dev && \
  cd /tmp && \
  /bin/sh -c "$(curl -fsSL https://github.com/network-analytics/mdt-dialout-collector/raw/main/install.sh)" -- -l -v current && \
  cd /tmp && \
  git clone -b 4.6-stable https://github.com/ntop/nDPI.git && \
  git clone -b 1.7.9 --depth 1 https://github.com/pmacct/pmacct.git && \
  cd /tmp/nDPI && \
  ./autogen.sh && \
  ./configure --prefix=/usr/local/ && \
  make -j${nproc} && \
  make install && \
  ldconfig && \
  cd /tmp/pmacct && \
  ./autogen.sh && \
  ./configure \
    --enable-l2 \
    --enable-kafka \
    --enable-geoipv2 \
    --enable-avro \
    --enable-ndpi \
    --enable-grpc-collector \
    --enable-ebpf \
    --enable-nflog \
    --enable-bgp-bins \
    --enable-bmp-bins \
    --enable-st-bins \
    --enable-jansson && \
  make -j${nproc} && \
  make install

FROM ubuntu:22.04 AS build-frr                                                                                          
ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC
RUN apt-get update && \
  apt-get install -y \
  git \
  autoconf \
  automake \
  cmake \
  libtool \
  make \
  libreadline-dev \
  texinfo \
  pkg-config \
  libpam0g-dev \
  libjson-c-dev \
  bison flex \
  libc-ares-dev \
  python3-dev \
  python3-sphinx \
  python3-pip \
  install-info \
  build-essential \
  libsnmp-dev \
  perl \
  libcap-dev \
  libelf-dev \
  libunwind-dev \
  libprotobuf-dev \
  libprotoc-dev \
  libgrpc++-dev \
  protobuf-compiler \
  protobuf-compiler-grpc \
  protobuf-c-compiler \
  libprotobuf-c-dev \
  libpcre2-dev \
  libsqlite3-dev \
  libzmq3-dev && \
  pip install -U pytest && \
  cd /tmp && \
  git clone https://github.com/CESNET/libyang.git && \
  cd libyang && \
  git checkout v2.1.128 && \
  mkdir build && \
  cd /tmp/libyang/build && \
  cmake -D CMAKE_INSTALL_PREFIX:PATH=/usr \
    -D CMAKE_BUILD_TYPE:String="Release" .. && \
  make -j${nproc} && \
  make install && \
  cd /tmp && \
  git clone https://github.com/rtrlib/rtrlib.git && \
  cd /tmp/rtrlib && \
  git checkout v0.8.0 && \
  cmake -D CMAKE_BUILD_TYPE=Release . && \
  make -j${nproc} && \
  make install && \
  cd /tmp && \
  groupadd -r -g 92 frr && \
  groupadd -r -g 85 frrvty && \
  adduser --system --ingroup frr --home /var/run/frr/ \
    --gecos "FRR suite" --shell /sbin/nologin frr && \
  usermod -a -G frrvty frr && \
  cd /tmp && \
  git clone -b stable/10.0 https://github.com/frrouting/frr.git frr && \
  cd /tmp/frr && \
  ./bootstrap.sh && \
  ./configure \
    --prefix=/usr \
    --includedir=\${prefix}/include \
    --bindir=\${prefix}/bin \
    --sbindir=\${prefix}/lib/frr \
    --libdir=\${prefix}/lib/frr \
    --libexecdir=\${prefix}/lib/frr \
    --sysconfdir=/etc \
    --localstatedir=/var \
    --with-moduledir=\${prefix}/lib/frr/modules \
    --enable-configfile-mask=0640 \
    --enable-logfile-mask=0640 \
    --enable-snmp=agentx \
    --enable-multipath=64 \
    --enable-user=frr \
    --enable-group=frr \
    --enable-vty-group=frrvty \
    --with-pkg-git-version \
    --with-pkg-extra-version=-FermiHDIFRRv1.0.0 \
    --disable-ripd \
    --disable-ripngd \
    --disable-ospfd \
    --disable-ospf6d \
    --disable-ldpd \
    --disable-nhrpd \
    --disable-eigrpd \
    --disable-babeld \
    --disable-isisd \
    --disable-pimd \
    --disable-pim6d \
    --disable-vrrpd \
    --enable-config-rollbacks \
    --enable-zeromq \
    --enable-rpki && \
  mkdir /etc/frr && \
  chown frr:frr /etc/frr && \
  mkdir -p /usr/lib/frr/modules && \
  chown frr:frr /usr/lib/frr/modules && \
  mkdir -p /etc/frr/scripts && \
  chown frr:frr /etc/frr/scripts && \
  cd /tmp/frr && \
  make -j${nproc} && \
  make install

FROM ubuntu:22.04 AS router
ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC
RUN apt-get update && \
  apt-get install -y \
    iputils-ping \
    iproute2 \
    dnsutils \
    mtr \
    curl \
    wget \
    tcpdump \
    nano \
    libreadline-dev \
    libpam0g-dev \
    libjson-c-dev \
    libc-ares-dev \
    python3-dev \
    python3-pip \
    libsnmp-dev \
    perl \
    libcap-dev \
    libelf-dev \
    libunwind-dev \
    libprotobuf-dev \
    libprotoc-dev \
    libgrpc++-dev \
    protobuf-compiler \
    protobuf-compiler-grpc \
    protobuf-c-compiler \
    libprotobuf-c-dev \
    libpcre2-dev \
    libsqlite3-dev \
    libzmq3-dev \
    default-libmysqlclient-dev \
    libnuma-dev \
    libcurl4-openssl-dev \
    libjansson-dev \
    libnetfilter-log-dev \
    libpcap-dev \
    libpq-dev \
    libsnappy-dev \
    libssl-dev \
    libgnutls28-dev \
    zlib1g-dev \
    librdkafka-dev \
    libmaxminddb-dev \
    libavro-dev \
    libbpf-dev && \
  groupadd -r -g 92 frr && \
  groupadd -r -g 85 frrvty && \
  adduser --system --ingroup frr --home /var/run/frr/ \
    --gecos "FRR suite" --shell /sbin/nologin frr && \
  usermod -a -G frrvty frr
COPY --from=build-pmacct "/usr/local/bin/pmacct" "/usr/local/bin/ndpiReader" "/usr/local/bin/"
COPY --from=build-pmacct "/usr/local/sbin/" "/usr/local/sbin/"
COPY --from=build-pmacct "/usr/local/lib/" "/usr/local/lib"
COPY --from=build-frr "/usr/share/yang/modules/" "/usr/share/yang/modules/"
COPY --from=build-frr "/usr/lib/x86_64-linux-gnu/libyang.s*" "/usr/lib/x86_64-linux-gnu/"
COPY --from=build-frr "/usr/include/libyang/" "/usr/include/libyang/"
COPY --from=build-frr "/usr/lib/x86_64-linux-gnu/pkgconfig/libyang.pc" "/usr/lib/x86_64-linux-gnu/pkgconfig/"
COPY --from=build-frr "/usr/bin/yanglint" "/usr/bin/yangre" "/usr/bin/yanglint"
COPY --from=build-frr "/usr/bin/yangre" "/usr/bin/yangre"
COPY --from=build-frr "/var/run/frr" "/var/run/frr"
COPY --from=build-frr "/etc/frr" "/etc/frr"
COPY --from=build-frr "/usr/lib/frr/" "/usr/lib/frr/"
COPY --from=build-frr "/usr/local/lib/" "/usr/local/lib"
COPY --from=build-frr "/tmp/frr/tools/frrcommon.sh" "/usr/lib/frr/"
COPY --from=build-frr "/usr/bin/vtysh" "/usr/bin/vtysh"
COPY --chmod=711 "./docker-start.sh" "/docker-start.sh"
COPY "./daemons.conf" "/etc/frr/daemons"
COPY "./router-a.conf" "/etc/frr/frr.conf"
COPY "./pmacctd.conf" "/etc/pmacct/pmacctd.conf"
COPY "./pmacctd.interfaces.map" "/etc/pmacct/pmacctd.interfaces.map"
COPY "./networks_file" "/etc/pmacct/networks_file"
COPY "./GeoLite2-City.mmdb" "/etc/geoip.db"
RUN echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf && \
  rm /lib/x86_64-linux-gnu/libyang.so.2 && \
  ln -s /lib/x86_64-linux-gnu/libyang.2.41.0 /lib/x86_64-linux-gnu/libyang.so.2 && \
  echo "net.ipv6.conf.all.forwarding=1" >> /etc/sysctl.conf && \
  ldconfig && \
  sysctl -p && \
  chmod +x /usr/lib/frr/frrcommon.sh && \
  chmod +x /lib/lsb/init-functions && \
  ldconfig -n /usr/lib/frr/modules
HEALTHCHECK CMD vtysh -c "show watchfrr" || exit 1
ENTRYPOINT ["/docker-start.sh"]

FROM ubuntu:22.04 AS pmacct
ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC
RUN apt-get update && \
  apt-get install -y \
    iputils-ping \
    iproute2 \
    dnsutils \
    mtr \
    curl \
    wget \
    tcpdump \
    nano \
    default-jre \
    libjson-c-dev \
    libsqlite3-dev \
    libnuma-dev \
    libcurl4-openssl-dev \
    libjansson-dev \
    libnetfilter-log-dev \
    libpcap-dev \
    libpq-dev \
    libsnappy-dev \
    libssl-dev \
    libgnutls28-dev \
    zlib1g-dev \
    librdkafka-dev \
    libmaxminddb-dev \
    libavro-dev \
    libbpf-dev
COPY --from=build-pmacct "/usr/local/bin/pmacct" "/usr/local/bin/ndpiReader" "/usr/local/bin/"
COPY --from=build-pmacct "/usr/local/sbin/" "/usr/local/sbin/"
COPY --from=build-pmacct "/usr/local/lib/" "/usr/local/lib"
COPY --chmod=711 "./docker-start-nfacctd.sh" "/docker-start.sh"
COPY "./nfacctd.conf" "/etc/pmacct/nfacctd.conf"
COPY "./networks_file" "/etc/pmacct/networks_file"
COPY "./GeoLite2-City.mmdb" "/etc/geoip.db"
RUN ldconfig
ENTRYPOINT ["/docker-start.sh"]

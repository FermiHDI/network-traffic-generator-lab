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
RUN apt-get update && \
  apt-get install -y \
    iputils-ping \
    iproute2 \
    dnsutils \
    mtr \
    curl \
    wget \
    tcpdump \
    nano

# FROM gcr.io/distroless/base-debian12 AS pmacct
FROM ubuntu:22.04 AS pmacct
ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC PATH=${PATH}:/usr/local/lib LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/lib:/usr/lib/x86_64-linux-gnu
COPY --from=build-pmacct "/usr/bin/ping" "/usr/bin/curl" "/usr/bin/"
COPY --from=build-pmacct "/usr/sbin/ip" "/usr/sbin/"
COPY --from=build-pmacct "/lib64/ld-linux-x86-64.so*" "/lib64/"
COPY --from=build-pmacct "/lib/x86_64-linux-gnu/libmaxminddb.so*" \
  "/lib/x86_64-linux-gnu/libavro.so*" \
  "/lib/x86_64-linux-gnu/libbpf.so*" \
  "/lib/x86_64-linux-gnu/libc.so*" \
  "/lib/x86_64-linux-gnu/libcap.so*" \
  "/lib/x86_64-linux-gnu/libcrypto.so*" \
  "/lib/x86_64-linux-gnu/libdbus-1.so*" \
  "/lib/x86_64-linux-gnu/libelf.so*" \
  "/lib/x86_64-linux-gnu/libgcc_s.so*" \
  "/lib/x86_64-linux-gnu/libgcrypt.so*" \
  "/lib/x86_64-linux-gnu/libgpg-error.so*" \
  "/lib/x86_64-linux-gnu/libjansson.so*" \
  "/lib/x86_64-linux-gnu/liblz4.so*" \
  "/lib/x86_64-linux-gnu/liblzma.so*" \
  "/lib/x86_64-linux-gnu/libm.so*" \
  "/lib/x86_64-linux-gnu/libmnl.so*" \
  "/lib/x86_64-linux-gnu/libnetfilter_log.so*" \
  "/lib/x86_64-linux-gnu/libnfnetlink.so*" \
  "/lib/x86_64-linux-gnu/libpcap.so*" \
  "/lib/x86_64-linux-gnu/librdkafka.so*" \
  "/lib/x86_64-linux-gnu/libsasl2.so*" \
  "/lib/x86_64-linux-gnu/libsnappy.so*" \
  "/lib/x86_64-linux-gnu/libssl.so*" \
  "/lib/x86_64-linux-gnu/libstdc++.so*" \
  "/lib/x86_64-linux-gnu/libsystemd.so*" \
  "/lib/x86_64-linux-gnu/libz.so*" \
  "/lib/x86_64-linux-gnu/libzstd.so*" \
  "/lib/x86_64-linux-gnu/"
COPY --from=build-pmacct "/usr/local/bin/pmacct" "/usr/local/bin/"
COPY --from=build-pmacct "/usr/local/sbin/" "/usr/local/sbin/"
COPY --from=build-pmacct "/usr/local/lib/" "/usr/local/lib"
COPY "./*.conf" "/etc/pmacct/"
COPY "./networks_file" "/etc/pmacct/"
COPY "./GeoLite2-City.mmdb" "/etc/GeoLite2-City.mmdb"
ENTRYPOINT ["/usr/local/sbin/nfacctd", "-f", "/etc/pmacct/nfacctd.conf"]

FROM ubuntu:22.04 AS build-frr                                                                                          
ENV DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC
ENV S6_OVERLAY_VERSION=3.1.4.1
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
    --enable-user=nobody \
    --enable-group=nogroup \
    --enable-vty-group=nogroup \
    --with-pkg-git-version \
    --with-pkg-extra-version=-FermiHDI-FRRv1.0.0 \
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
  make install && \
  echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf && \
  rm /lib/x86_64-linux-gnu/libyang.so.2 && \
  ln -s /lib/x86_64-linux-gnu/libyang.2.41.0 /lib/x86_64-linux-gnu/libyang.so.2 && \
  echo "net.ipv6.conf.all.forwarding=1" >> /etc/sysctl.conf && \
  ldconfig && \
  sysctl -p && \
  chmod +x /usr/lib/frr/frrcommon.sh && \
  chmod +x /lib/lsb/init-functions && \
  ldconfig -n /usr/lib/frr/modules
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-symlinks-noarch.tar.xz /tmp
RUN mkdir /tmp/rootfs && \
  tar -Jxpf /tmp/s6-overlay-noarch.tar.xz -C /tmp/rootfs && \
  tar -Jxpf /tmp/s6-overlay-x86_64.tar.xz -C /tmp/rootfs && \
  tar -Jxpf /tmp/s6-overlay-symlinks-noarch.tar.xz -C /tmp/rootfs

# FROM gcr.io/distroless/base-debian12 AS router
FROM ubuntu:22.04 AS router
ENV TZ=Etc/UTC PATH=${PATH}:/usr/local/lib:/command LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/lib:/usr/lib/x86_64-linux-gnu
COPY --from=build-pmacct "/usr/bin/ping" "/usr/bin/curl" "/usr/bin/"
COPY --from=build-pmacct "/usr/sbin/ip" "/usr/sbin/"
COPY --from=build-pmacct "/lib64/ld-linux-x86-64.so*" "/lib64/"
COPY --from=build-pmacct "/lib/x86_64-linux-gnu/libmaxminddb.so*" \
  "/lib/x86_64-linux-gnu/libavro.so*" \
  "/lib/x86_64-linux-gnu/libbpf.so*" \
  "/lib/x86_64-linux-gnu/libc.so*" \
  "/lib/x86_64-linux-gnu/libcap.so*" \
  "/lib/x86_64-linux-gnu/libcrypto.so*" \
  "/lib/x86_64-linux-gnu/libdbus-1.so*" \
  "/lib/x86_64-linux-gnu/libelf.so*" \
  "/lib/x86_64-linux-gnu/libgcc_s.so*" \
  "/lib/x86_64-linux-gnu/libgcrypt.so*" \
  "/lib/x86_64-linux-gnu/libgpg-error.so*" \
  "/lib/x86_64-linux-gnu/libjansson.so*" \
  "/lib/x86_64-linux-gnu/liblz4.so*" \
  "/lib/x86_64-linux-gnu/liblzma.so*" \
  "/lib/x86_64-linux-gnu/libm.so*" \
  "/lib/x86_64-linux-gnu/libmnl.so*" \
  "/lib/x86_64-linux-gnu/libnetfilter_log.so*" \
  "/lib/x86_64-linux-gnu/libnfnetlink.so*" \
  "/lib/x86_64-linux-gnu/libpcap.so*" \
  "/lib/x86_64-linux-gnu/librdkafka.so*" \
  "/lib/x86_64-linux-gnu/libsasl2.so*" \
  "/lib/x86_64-linux-gnu/libsnappy.so*" \
  "/lib/x86_64-linux-gnu/libssl.so*" \
  "/lib/x86_64-linux-gnu/libstdc++.so*" \
  "/lib/x86_64-linux-gnu/libsystemd.so*" \
  "/lib/x86_64-linux-gnu/libz.so*" \
  "/lib/x86_64-linux-gnu/libzstd.so*" \
  "/lib/x86_64-linux-gnu/"
COPY --from=build-pmacct "/usr/local/bin/pmacct" "/usr/local/bin/"
COPY --from=build-pmacct "/usr/local/sbin/" "/usr/local/sbin/"
COPY --from=build-pmacct "/usr/local/lib/" "/usr/local/lib"
COPY "./*acct.conf" "/etc/pmacct/"
COPY "./networks_file" "/etc/pmacct/"
COPY "./GeoLite2-City.mmdb" "/etc/GeoLite2-City.mmdb"
COPY --from=build-frr --chmod=755 "/tmp/rootfs/" "/"
COPY --from=build-frr "/lib/x86_64-linux-gnu/libbsd.so*" \
  "/lib/x86_64-linux-gnu/libcares.so*" \
  "/lib/x86_64-linux-gnu/libcom_err.so*" \
  "/lib/x86_64-linux-gnu/libcrypt.so*" \
  "/lib/x86_64-linux-gnu/libgssapi_krb5.so*" \
  "/lib/x86_64-linux-gnu/libjson-c.so*" \
  "/lib/x86_64-linux-gnu/libk5crypto.so*" \
  "/lib/x86_64-linux-gnu/libkeyutils.so*" \
  "/lib/x86_64-linux-gnu/libkrb5.so*" \
  "/lib/x86_64-linux-gnu/libkrb5support.so*" \
  "/lib/x86_64-linux-gnu/libmd.so*" \
  "/lib/x86_64-linux-gnu/libnetsnmp.so*" \
  "/lib/x86_64-linux-gnu/libnetsnmpagent.so*" \
  "/lib/x86_64-linux-gnu/libnorm.so*" \
  "/lib/x86_64-linux-gnu/libnsl.so*" \
  "/lib/x86_64-linux-gnu/libpcre2-8.so*" \
  "/lib/x86_64-linux-gnu/libperl.so*" \
  "/lib/x86_64-linux-gnu/libpgm-5.3.so*" \
  "/lib/x86_64-linux-gnu/libprotobuf-c.so*" \
  "/lib/x86_64-linux-gnu/libpthread.so*" \
  "/lib/x86_64-linux-gnu/libreadline.so*" \
  "/lib/x86_64-linux-gnu/libresolv.so*" \
  "/lib/x86_64-linux-gnu/libsodium.so*" \
  "/lib/x86_64-linux-gnu/libsqlite3.so*" \
  "/lib/x86_64-linux-gnu/libtirpc.so*" \
  "/lib/x86_64-linux-gnu/libunwind.so*" \
  "/lib/x86_64-linux-gnu/libwrap.so*" \
  "/lib/x86_64-linux-gnu/libyang.so*" \
  "/lib/x86_64-linux-gnu/libzmq.so*" \
  "/lib/x86_64-linux-gnu/"
COPY --from=build-frr "/usr/lib/frr/libfrr.so*" \
  "/usr/lib/frr/libmgmt_be_nb.so*" \
  "/usr/lib/frr/"
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
COPY "./daemons.conf" "/etc/frr/daemons"
COPY "./frr.conf" "/etc/frr/frr.conf"
COPY "./pmacctd.conf" "./pmacctd.interfaces.map" "/etc/pmacct/"
COPY "./networks_file" "/etc/pmacct/"
COPY "./GeoLite2-City.mmdb" "/etc/GeoLite2-City.mmdb"
COPY --chmod=755 "./s6-rc.d/" "/etc/s6-overlay/s6-rc.d/"
RUN touch /etc/frr/vtysh.conf && \
    mkdir -p /var/run/frr && \
    chown -R nobody:nogroup /etc/frr /var/run/frr && \
    mkdir -p /var/run/s6/container_environment && \
    echo $LD_LIBRARY_PATH > /var/run/s6/container_environment/LD_LIBRARY_PATH
HEALTHCHECK CMD vtysh -c "show watchfrr" || exit 1
ENTRYPOINT ["/init", "/usr/lib/frr/watchfrr", "zebra", "mgmtd", "staticd"]
CMD ["bgpd"]

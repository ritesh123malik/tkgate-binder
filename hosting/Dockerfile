# Build only the curated context produced by prepare-context.py.
ARG KASM_BASE=kasmweb/core-ubuntu-jammy:1.17.0
FROM ubuntu:22.04 AS build
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    build-essential autoconf automake libtool libtool-bin bison flex \
    tcl8.6-dev tk8.6-dev libx11-dev python3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /build/tkgate
COPY source/ ./
# Debian/Ubuntu keep the real Tcl/Tk configuration in multiarch directories.
RUN mkdir -p /opt/tcltk-config/lib /opt/tcltk-config/include \
    && ln -s /usr/lib/$(dpkg-architecture -qDEB_HOST_MULTIARCH)/tcl8.6/tclConfig.sh /opt/tcltk-config/lib/tclConfig.sh \
    && ln -s /usr/lib/$(dpkg-architecture -qDEB_HOST_MULTIARCH)/tk8.6/tkConfig.sh /opt/tcltk-config/lib/tkConfig.sh \
    && mkdir -p m4 && sh autogen.sh \
    && CFLAGS='-O2 -std=gnu99 -fcommon' ./configure --prefix=/opt/tkgate --with-tcltk=/opt/tcltk-config \
    && make -j2 && make install \
    && python3 macos/test.py --prefix /opt/tkgate \
    && cc -O0 -g -fsanitize=address,undefined -fno-sanitize-recover=all -Isrc/common \
       test/common/ycmalloc_pool.c src/common/ycmalloc.c -o /tmp/pool-test \
    && /tmp/pool-test \
    && cc -O0 -g -Isrc/common test/common/hash_pointer.c src/common/hash.c -o /tmp/hash-test \
    && /tmp/hash-test

FROM ${KASM_BASE}
USER root
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    tcl8.6 tk8.6 xfonts-base fonts-dejavu-core ghostscript thunar \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /opt/tkgate /opt/tkgate
COPY source.tar.gz /usr/share/doc/tkgate/source.tar.gz
COPY source/COPYING /usr/share/doc/tkgate/COPYING
COPY source/hosting/custom_startup.sh /dockerstartup/custom_startup.sh
COPY source/hosting/tkgate.desktop /usr/share/applications/tkgate.desktop
COPY source/hosting/SESSION-README.txt /home/kasm-default-profile/Desktop/READ-ME.txt
RUN install -m 755 /usr/share/applications/tkgate.desktop /home/kasm-default-profile/Desktop/tkgate.desktop \
    && chmod 755 /dockerstartup/custom_startup.sh \
    && /dockerstartup/set_user_permission.sh /home/kasm-default-profile \
    && mkdir -p /home/kasm-user && chown 1000:0 /home/kasm-user
ENV PATH="/opt/tkgate/bin:${PATH}" TKGATE_HOME=/opt/tkgate/share/tkgate
WORKDIR /home/kasm-user
USER 1000

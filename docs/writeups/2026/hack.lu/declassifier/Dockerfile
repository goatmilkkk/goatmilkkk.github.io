FROM debian:trixie-20260925-slim@sha256:a99cfc517144bc59b1978475ec53b46ecabec7e43635402ee5b77cc54cd1b20a

# for reproducible build:
# https://github.com/reproducible-containers/repro-sources-list.sh
ENV DEBIAN_FRONTEND=noninteractive
RUN \
  --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  --mount=type=bind,source=./repro-sources-list.sh,target=/usr/local/bin/repro-sources-list.sh \
  repro-sources-list.sh && \
  apt-get update && \
  apt-get install -y socat && \
  : "Clean up for improving reproducibility (optional)" && \
  rm -rf /var/log/* /var/cache/ldconfig/aux-cache

RUN useradd -m -d /chal ctf && \
    chown -R root:root /chal && \
    chmod +rx /chal
WORKDIR /chal

COPY entrypoint.sh /
COPY declass .

EXPOSE 1024
CMD ["/entrypoint.sh"]

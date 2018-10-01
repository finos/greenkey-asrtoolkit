FROM alpine:latest
LABEL maintainer="Matthew Goldey <mgoldey@greenkeytech.com>"
LABEL organization="Green Key Technologies <transcription@greenkeytech.com>"

# APK INSTALLS
RUN apk update && \
  apk --no-cache add \
    py3-pip \
    python3 \
    python3-dev\
    sox \
    wget && \
  rm -rf /var/cache/apk/*

COPY . /

RUN pip3 install -e .

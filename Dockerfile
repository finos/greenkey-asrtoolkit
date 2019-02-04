FROM alpine:latest
LABEL maintainer="Matthew Goldey <mgoldey@greenkeytech.com>"
LABEL organization="Green Key Technologies <transcription@greenkeytech.com>"

# APK INSTALLS
RUN apk update && \
  apk --no-cache add \
    build-base \
    gcc \
    g++ \
    libc-dev \
    libstdc++ \
    linux-headers \
    make \
    py3-pip \
    python3 \
    python3-dev\
    sox \
    wget && \
  rm -rf /var/cache/apk/*

COPY . /

RUN pip3 install -e . && \
  pip3 install requests

RUN wget https://storage.googleapis.com/gkt-external/sample_audio_files.tar.gz && tar -xvzf sample_audio_files.tar.gz


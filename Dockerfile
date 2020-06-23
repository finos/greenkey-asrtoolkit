FROM debian:buster-slim
LABEL maintainer="Matthew Goldey <mgoldey@greenkeytech.com>" \
      organization="Green Key Technologies <transcription@greenkeytech.com>"

# APT INSTALLS
RUN apt update && \
    apt install -y python3-dev libsox-fmt-mp3 wget curl build-essential sox && \
    apt-get clean autoclean && \
    apt-get autoremove -y && \
    rm -rf /usr/share/doc /var/lib/apt/lists/* && \
    curl https://bootstrap.pypa.io/get-pip.py | python3 && \
    wget https://storage.googleapis.com/gkt-external/sample_audio_files.tar.gz && tar -xvzf sample_audio_files.tar.gz

WORKDIR /asrtoolkit
COPY . /asrtoolkit

RUN \
  python3 -m pip install .[dev] && \
  python3 -m pip install "requests>=2.18.4"

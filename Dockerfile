FROM debian:buster-slim
LABEL maintainer="Matthew Goldey <mgoldey@greenkeytech.com>"
LABEL organization="Green Key Technologies <transcription@greenkeytech.com>"

# APK INSTALLS
RUN apt update && \
    apt install -y python3-dev libsox-fmt-mp3 wget curl && \
    apt-get clean autoclean && \
    apt-get autoremove -y && \
    rm -rf /usr/share/doc /var/lib/apt/lists/*


RUN curl https://bootstrap.pypa.io/get-pip.py | python3
COPY . /

RUN \
  python3 -m pip install -e .[dev] && \
  python3 -m pip install "requests>=2.18.4"

RUN wget https://storage.googleapis.com/gkt-external/sample_audio_files.tar.gz && tar -xvzf sample_audio_files.tar.gz


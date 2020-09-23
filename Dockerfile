FROM python:3.7-slim

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

ENV TOOLING_WEBSERVER_VERSION="0.10.0"
ENV TOOLING_WEBSERVER_URL="https://github.com/exercism/tooling-webserver/releases/download/${TOOLING_WEBSERVER_VERSION}/tooling_webserver"

RUN apt-get update \
 && apt-get install curl \
 && curl -L -o /usr/local/bin/tooling_webserver "$TOOLING_WEBSERVER_URL" \
 && chmod +x /usr/local/bin/tooling_webserver \
 && apt-get remove curl \
 && rm -rf /var/lib/apt/lists/*

COPY . /opt/test-runner

WORKDIR /opt/test-runner

ENTRYPOINT [ "sh", "bin/run.sh" ]

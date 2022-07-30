FROM python:3.10-slim

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN apt-get update \
 && apt-get autoremove -y \
 && rm -rf /var/lib/apt/lists/*

COPY . /opt/test-runner

WORKDIR /opt/test-runner

ENTRYPOINT [ "/opt/test-runner/bin/run.sh" ]

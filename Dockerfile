FROM python:3.7-alpine

RUN pip install pytest

WORKDIR /opt/test-runner

COPY ./bin/* ./bin/
COPY ./runner/* ./runner/

ENTRYPOINT [ "sh", "/opt/test-runner/bin/run.sh" ]

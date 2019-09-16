FROM python:3.7-alpine

WORKDIR /opt/test-runner

COPY ./run.sh ./bin/

ENTRYPOINT [ "sh", "/opt/test-runner/bin/run.sh" ]

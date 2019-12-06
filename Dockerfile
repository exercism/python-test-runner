FROM python:3.7-alpine

RUN pip install pytest

WORKDIR /opt/test-runner

COPY ./run.sh ./bin/
COPY ./process_results.py ./

# Necessary to apply to tests run in bound directory /solution/
COPY ./conftest.py /

ENTRYPOINT [ "sh", "/opt/test-runner/bin/run.sh" ]

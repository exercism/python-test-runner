FROM python:3.13-alpine3.23

COPY requirements.txt /requirements.txt

RUN apk update && apk upgrade\
 && apk --no-cache add bash\
 && apk cache clean


RUN --mount=type=cache,target=/root/.cache/pip\
 PYTHONDONTWRITEBYTECODE=1\
 pip install --no-compile  --no-cache\
 -r /requirements.txt

COPY . /opt/test-runner

# Compile every installed package, and the runner itself, to bytecode now.
# The packages are installed with --no-compile, so without this step every run
# compiled pytest and its dependencies from source before running any tests.
RUN python3 -m compileall -q /usr/local/lib/python3.13/site-packages /opt/test-runner/runner /opt/test-runner/bin

# Run pytest once on a dummy test so it caches its assertion-rewritten copies
# of the installed plugins (such as pytest-subtests), which compileall can't make.
RUN mkdir /tmp/warm && echo "def test_x(): assert True" > /tmp/warm/test_warm.py \
 && python3 -m pytest --collect-only -q -p no:cacheprovider /tmp/warm && rm -rf /tmp/warm

WORKDIR /opt/test-runner

ENTRYPOINT ["sh", "/opt/test-runner/bin/run.sh" ]

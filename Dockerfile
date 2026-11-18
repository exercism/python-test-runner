FROM python:3.13-alpine3.23

COPY requirements.txt /requirements.txt

RUN apk update && apk upgrade\
 && apk --no-cache add bash\
 && apk cache clean


# Don't write bytecode when Python runs, and don't buffer output.
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# Pip compiles each package to bytecode as it installs it, so every run
# starts pytest and its dependencies from compiled files instead of compiling
# them from source first.
RUN --mount=type=cache,target=/root/.cache/pip pip install -r /requirements.txt

COPY . /opt/test-runner

# Compile the runner to bytecode now, so runs don't compile it. The
# checked-hash files stay valid however the file times change.
RUN python3 -m compileall -q --invalidation-mode=checked-hash /opt/test-runner/runner /opt/test-runner/bin

# Run pytest once on a dummy test so it caches its assertion-rewritten copies
# of the installed plugins (such as pytest-subtests), which compileall can't make.
# This step unsets PYTHONDONTWRITEBYTECODE, because pytest needs it unset to
# write those files.
RUN mkdir /tmp/warm && echo "def test_x(): assert True" > /tmp/warm/test_warm.py \
 && PYTHONDONTWRITEBYTECODE= python3 -m pytest --collect-only -q -p no:cacheprovider /tmp/warm && rm -rf /tmp/warm

WORKDIR /opt/test-runner

ENTRYPOINT ["sh", "/opt/test-runner/bin/run.sh" ]

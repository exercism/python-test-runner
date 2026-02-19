FROM python:3.13.5-alpine3.22

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN apk update && apk upgrade\
 && apk --no-cache add curl bash\
 && apk cache clean

COPY . /opt/test-runner

WORKDIR /opt/test-runner

ENTRYPOINT ["sh", "/opt/test-runner/bin/run.sh" ]
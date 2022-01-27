FROM        ubuntu:20.04 AS builder

RUN         apt-get update && apt-get install -y build-essential gnupg python3 python3-setuptools python3-pip
COPY        ./requirements.txt /app/requirements.txt
WORKDIR     /app

COPY        [^docker]* /app/


FROM        alpine:3.15.0

RUN         apk --no-cache add python3 py3-pip
COPY        --from=builder /app /app

WORKDIR     /app
RUN         pip3 install -r requirements.txt


ENTRYPOINT  ["python3"]
CMD         ["app.py"]
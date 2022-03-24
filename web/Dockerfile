FROM python:3.8.5-alpine

COPY . /app
WORKDIR /app

RUN python3 -m venv /opt/venv

RUN apk add mariadb mariadb-dev python3-dev libffi-dev openssl-dev
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

RUN /opt/venv/bin/pip3 install --upgrade pip &&  \
    /opt/venv/bin/pip3 install -r requirements.txt && \
    chmod +x entrypoint.sh

CMD ["/app/entrypoint.sh"]
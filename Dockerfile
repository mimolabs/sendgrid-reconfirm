FROM python:3-alpine

RUN apk update && apk upgrade && \
    apk add gcc python python-dev py-pip \
    && rm -rf /var/cache/apk/*

ADD reqs.txt /opt/reconfirm/requirements.txt
RUN pip install -r /opt/reconfirm/requirements.txt \
    && rm -rf ~/.pip/cache

ADD . /opt/reconfirm/

EXPOSE 8080

WORKDIR /opt/reconfirm

CMD gunicorn -b 0.0.0.0:8000 --workers 2 --max-requests 1000 wsgi

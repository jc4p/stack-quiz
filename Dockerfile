FROM janeczku/alpine-kubernetes:3.2

RUN apk --update add \
    python \
    py-pip \ 
    uwsgi-python

ADD . /opt/quiz/
WORKDIR /opt/quiz/

RUN apk --update add --virtual builddeps \
    python-dev \
    build-base \
    libmemcached-dev \
    zlib-dev \
    musl-dev \
  && pip install --upgrade pip \
  && pip install -r requirements.txt \
  && apk del builddeps \
  && rm -rf /var/cache/apk/*

EXPOSE 8000
CMD ["/usr/bin/gunicorn","-b","0.0.0.0:8000", "quiz.wsgi"]



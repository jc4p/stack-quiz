FROM python:2.7
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install libmemcached-dev
RUN mkdir /opt/quiz/
ADD . /opt/quiz/
WORKDIR /opt/quiz/
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["/usr/local/bin/gunicorn","-b '0.0.0.0:8000'", "quiz.wsgi"]



FROM python:3.6.9

WORKDIR /src

ADD . /src

RUN pip install -r requirements.txt

CMD [ "uwsgi", "app.ini" ]

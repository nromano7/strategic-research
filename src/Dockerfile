FROM python:3.6-alpine

RUN adduser -D admin

WORKDIR /home/app

ENV FLASK_APP application.py
ENV ELASTICSEARCH_URL http://elasticsearch:9200

COPY requirements.txt requirements.txt
COPY dashapp dashapp
COPY elastic elastic
COPY flaskapp flaskapp
COPY webscrapper webscrapper
COPY application.py ./
COPY boot.sh ./
COPY .data .data

RUN chmod +x boot.sh
RUN apk add --update --no-cache g++ gcc libxslt-dev
RUN pip install --upgrade pip
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

# RUN python3 -m elastic.index

RUN chown -R admin:admin ./
USER admin

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
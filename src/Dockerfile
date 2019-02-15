# FROM joyzoursky/python-chromedriver:3.6-alpine3.7
FROM python:3.6-alpine

ENV FLASK_APP application.py
ENV ELASTICSEARCH_URL http://host.docker.internal:9200
ENV DATAPATH ./.data
ENV FLASKHOST '0.0.0.0'
# ENV CHROMEDRIVER_DIR /home/app/webscrapper/chromedriver/chromedriver.exe
# ENV PATH $CHROMEDRIVER_DIR:$PATH

RUN adduser -D admin
RUN apk update
RUN apk add chromium chromium-chromedriver
RUN apk add --update --no-cache g++ gcc libxslt-dev
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /home/app
COPY dashapp dashapp
COPY elastic elastic
COPY flaskapp flaskapp
COPY webscrapper webscrapper
COPY application.py ./
COPY .data .data

EXPOSE 5000
ENTRYPOINT ["python"]

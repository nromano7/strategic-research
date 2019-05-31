@echo on
docker pull nromano7/srs:data
docker pull nromano7/srs:app

docker run -v /usr/share/elasticsearch/data --entrypoint "bin/sh" ^
--name srs-data-container nromano7/srs:data

TIMEOUT 10
docker start srs-elasticsearch
IF /I "%ERRORLEVEL%" NEQ "0" ( 
    docker run --name srs-elasticsearch -d -p 9200:9200 -p 9300:9300 ^
    -e "discovery.type=single-node" --volumes-from srs-data-container ^
    docker.elastic.co/elasticsearch/elasticsearch:6.3.2
)

TIMEOUT 10
docker run -d --name srs-app --rm -p 5000:5000 ^
--link srs-elasticsearch:elasticsearch ^
--env ELASTICSEARCH_URL=http://elasticsearch:9200 ^
-d nromano7/srs:app run.py

pause

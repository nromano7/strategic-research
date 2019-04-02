@echo on
docker start elasticsearch
IF /I "%ERRORLEVEL%" NEQ "0" ( 
docker volume create --name esdata
docker run --name elasticsearch -d -p 9200:9200 -p 9300:9300 ^
-e "discovery.type=single-node" -v esdata:/usr/share/elasticsearch/data ^
docker.elastic.co/elasticsearch/elasticsearch:6.3.2
)
docker pull nromano7/srs:latest
docker run --name srs-app --rm -p 5000:5000 ^
--link elasticsearch:elasticsearch ^
--env ELASTICSEARCH_URL=http://elasticsearch:9200 ^
-d nromano7/srs:latest run.py
pause
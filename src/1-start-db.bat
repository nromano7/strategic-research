@echo on
docker start elasticsearch
IF /I "%ERRORLEVEL%" NEQ "0" ( 
docker volume create --name esdata
docker run --name elasticsearch -d -p 9200:9200 -p 9300:9300 ^
-e "discovery.type=single-node" -v esdata:/usr/share/elasticsearch/data ^
docker.elastic.co/elasticsearch/elasticsearch:6.3.2
)
ECHO Elasticsearch is running.
pause

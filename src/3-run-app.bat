@echo on
docker pull nromano7/srs:latest
docker run --name srs-app --rm -p 5000:5000 ^
--link elasticsearch:elasticsearch ^
--env ELASTICSEARCH_URL=http://elasticsearch:9200 ^
-d nromano7/srs:latest application.py
pause
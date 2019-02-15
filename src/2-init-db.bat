@echo on

docker run --name srs-dbinit --rm nromano7/srs:latest -m elastic.index

pause
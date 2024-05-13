#!/bin/bash
docker stop $(docker ps -a -q)
docker rm $(docker ps -aq)
docker rmi -f $(docker images -aq)
docker compose build --no-cache ossqa-web
docker-compose up ossqa-web
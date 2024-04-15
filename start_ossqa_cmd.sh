#!/bin/bash
git pull
docker stop $(docker ps -a -q)
docker rm $(docker ps -aq)
docker rmi -f $(docker images -aq)
docker compose build --no-cache ossqa-cmd
docker-compose up ossqa-cmd
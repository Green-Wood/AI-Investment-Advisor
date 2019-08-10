#!/usr/bin/env bash

docker-compose down
docker-compose  up --build -d --remove-orphans
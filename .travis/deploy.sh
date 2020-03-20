#!/bin/bash
docker build -t haavardnk/krakenes .   
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker push haavardnk/krakenes
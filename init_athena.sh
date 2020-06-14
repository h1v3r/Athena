#!/bin/sh

#Build directories for Elastic
mkdir -p ../Athena_Data/elastic-data/nodes/0/indices
chmod -R 775 ../Athena_Data/elastic-data/nodes/0
chmod -R 777 ./elastic-env

#Set max virtual memory for Elastic
sysctl -w vm.max_map_count=262144


#Docker
systemctl start docker
docker-compose up -d

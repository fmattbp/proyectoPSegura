#!/bin/bash

for var in $(ccrypt -d -c settings.env.cpt); do
    export "$var"
done

#for var in $(cat settings.env); do
#    export "$var"
#done

docker-compose --compatibility up -d
#docker-compose up 

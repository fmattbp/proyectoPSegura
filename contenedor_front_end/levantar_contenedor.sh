#!/bin/bash

var_env=""

for var in $(ccrypt -d -c settings.env.cpt); do
    var_env="$var_env -e $var"
done

comando=$(echo docker run  --rm -p 8888:8000 -v \"$PWD/progra_segura\":/code "$var_env" front_end_segura)

bash -c "$comando"

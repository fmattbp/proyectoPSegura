#!/bin/bash

su -c "ttyd -o -S -C ca.crt -K ca.key -c $USER:$PASS bash" limitado

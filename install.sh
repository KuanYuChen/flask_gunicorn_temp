#!/bin/sh
echo "Install"

sudo cp fgtapp.service /etc/systemd/system/
sudo cp fgtapp.nginx /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/fgtapp.nginx  /etc/nginx/sites-enabled/






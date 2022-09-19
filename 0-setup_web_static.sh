#!/usr/bin/env bash
# task 0

apt-get update
apt-get -y install nginx

mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

echo "Testing.. OK!" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data/

printf %s "server {
    listen 80;
    listen [::]:80;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html;

    location /hbnb_static {
        alias /data/web_static/current;
        index  index.html;
    }

    location /redirect_me {
                return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
    }

    error_page 404 /5-design_a_beautiful_404_page.html;

}" > /etc/nginx/sites-available/default

service nginx restart

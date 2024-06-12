server {
    server_name onstock.in www.onstock.in;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /stock;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/onstock.in/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/onstock.in/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot


}
server {
    if ($host = www.onstock.in) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    if ($host = onstock.in) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    listen 80;
    server_name onstock.in www.onstock.in;
    return 404; # managed by Certbot




}
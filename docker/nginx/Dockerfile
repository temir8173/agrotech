FROM nginx:stable-alpine
COPY default.conf /etc/nginx
COPY default.conf /etc/nginx/conf.d
EXPOSE 80
server {
    listen 80 default_server;
    server_name _;
    location / {
        proxy_pass http://web:8000;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
    location /static/ {
        alias /app/static/;
    }
    location /media/ {
        alias /app/static/;
    }
}
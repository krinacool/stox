ExecStart=/bin/bash -c '/usr/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock stock.wsgi:application & /usr/local/bin/daphne -b 0>



[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/stock
ExecStart=/bin/bash -c '/usr/bin/gunicorn stock.wsgi:application --bind unix:/run/gunicorn.sock & /usr/local/bin/daphne -b 0.0.0.0 -p 8001 stock.asgi:application'

[Install]
WantedBy=multi-user.target
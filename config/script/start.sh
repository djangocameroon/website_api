#!/bin/bash

/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord-web.conf &

/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord-celery.conf &

wait

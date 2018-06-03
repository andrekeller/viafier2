#!/bin/bash
set -e

if [[ $1 = 'viafier2' ]]; then
    MAX_ATTEMPTS=10
    ATTEMPT=1
    until /srv/viafier2/manage.py migrate || [[ $ATTEMPT -eq $MAX_ATTEMPTS ]]
    do
        ATTEMPT=$((ATTEMPT + 1))
        sleep 1
    done

    /srv/viafier2/manage.py collectstatic --noinput
    exec /usr/bin/uwsgi \
         --chdir /srv/viafier2 \
         --die-on-term \
         --need-app \
         --env DJANGO_SETTINGS_MODULE=viafier2.settings \
         --enable-threads \
         --master \
         --processes 2 \
         --socket :8000 \
         --wsgi-file viafier2/wsgi.py
else
    exec "$@"
fi

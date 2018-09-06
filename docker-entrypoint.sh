#!/bin/bash
set -e

if [[ $1 = 'viafier2' ]]; then
    MAX_ATTEMPTS=10
    ATTEMPT=1
    until /app/viafier2/manage.py migrate || [[ $ATTEMPT -eq $MAX_ATTEMPTS ]]
    do
        ATTEMPT=$((ATTEMPT + 1))
        sleep 1
    done

    /app/viafier2/manage.py collectstatic --noinput
    exec /usr/bin/uwsgi \
        --add-header "X-Viafier-Backend: ${HOSTNAME}" \
        --chdir /app/viafier2 \
        --die-on-term \
        --enable-threads \
        --env DJANGO_SETTINGS_MODULE=viafier2.settings \
        --master \
        --need-app \
        --processes 2 \
        --socket :8000 \
        --strict \
        --thunder-lock \
        --wsgi-file viafier2/wsgi.py
else
    exec "$@"
fi

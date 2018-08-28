FROM alpine:3.8

RUN mkdir /app
COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
COPY docker-entrypoint.sh /app/docker-entrypoint.sh

RUN apk --no-cache add dumb-init python3 pcre mailcap libpq libxml2 \
                       libxslt libressl libjpeg-turbo bash gettext git && \
    apk --no-cache add --virtual build-deps \
                       python3-dev build-base postgresql-dev libxml2-dev \
                       libxslt-dev linux-headers libressl-dev \
                       libjpeg-turbo-dev pcre-dev && \
    pip3 install pipenv && \
    cd /app && pipenv sync && \
    apk del build-deps

COPY viafier2 /app/viafier2
RUN cd /app && pipenv run viafier2/manage.py compilemessages -l de

USER nobody

EXPOSE 8000
ENTRYPOINT ["dumb-init", "/app/docker-entrypoint.sh"]
CMD ["viafier2"]

FROM alpine:3.7

COPY viafier2 /srv/viafier2
COPY requirements.txt /srv/viafier2/requirements.txt
COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN apk --no-cache add dumb-init python3 pcre mailcap libpq libxml2 \
                       libxslt libressl libjpeg-turbo bash gettext && \
    apk --no-cache add --virtual build-deps \
                       python3-dev build-base postgresql-dev libxml2-dev \
                       libxslt-dev linux-headers libressl-dev \
                       libjpeg-turbo-dev pcre-dev && \
    python3 -m ensurepip --default-pip && \
    pip3 install -U pip && \
    pip3 install -r /srv/viafier2/requirements.txt && \
    apk del build-deps

RUN /srv/viafier2/manage.py compilemessages

USER nobody
EXPOSE 8000

ENTRYPOINT ["dumb-init", "/docker-entrypoint.sh"]
CMD ["viafier2"]

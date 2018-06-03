FROM alpine:3.7

RUN mkdir /app
COPY requirements.txt /app/requirements.txt
COPY docker-entrypoint.sh /app/docker-entrypoint.sh

RUN apk --no-cache add dumb-init python3 pcre mailcap libpq libxml2 \
                       libxslt libressl libjpeg-turbo bash gettext && \
    apk --no-cache add --virtual build-deps \
                       python3-dev build-base postgresql-dev libxml2-dev \
                       libxslt-dev linux-headers libressl-dev \
                       libjpeg-turbo-dev pcre-dev && \
    python3 -m ensurepip --default-pip && \
    pip3 install -U pip && \
    pip3 install -r /app/requirements.txt && \
    apk del build-deps

COPY viafier2 /app/viafier2
RUN /app/viafier2/manage.py compilemessages -l de

USER nobody

EXPOSE 8000
ENTRYPOINT ["dumb-init", "/app/docker-entrypoint.sh"]
CMD ["viafier2"]

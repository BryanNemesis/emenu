FROM python:3.9-alpine
ENV PYTHONBUFFERED=1
ENV DEBUG=0
WORKDIR /home/app
COPY requirements.txt .
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
COPY . /home/app/
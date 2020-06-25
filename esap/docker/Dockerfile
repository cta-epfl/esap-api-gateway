FROM python:3.6.7-slim
RUN apt-get update && apt-get install --no-install-recommends -y bash nano mc
# RUN apk update && apk add gcc bash nano mc linux-headers musl-dev alpine-sdk openssl-dev libffi-dev

RUN mkdir /src
WORKDIR /src
COPY ../. /src/

RUN pip install --upgrade pip  "cython==0.29.14"
RUN pip install cryptography
RUN pip install -r requirements/prod.txt
RUN exec python manage.py collectstatic --settings=esap.settings.statics --no-input
CMD exec gunicorn esap.wsgi_docker:application --bind 0.0.0.0:8000 --workers 3

# build the image like this:
# docker build -t esap_api:latest .

# run the container from 'shared', like this:
# docker run -d --name esap_api --mount type=bind,source=/data/shared,target=/shared -p 8005:8000 --restart always esap_api:latest

# log into the container
# docker exec -it esap_api sh

FROM python:3.6.7-alpine
ENV PYTHONUNBUFFERED 1
RUN apk update && apk add bash && apk add nano
RUN mkdir /code
WORKDIR /code
FROM python:3.6.7-alpine
ENV PYTHONUNBUFFERED 1
RUN apk update && apk add bash && apk add nano && apk add mc
RUN mkdir /src
WORKDIR /src
COPY . /src/
RUN pip install -r requirements/prod.txt
RUN exec python manage.py collectstatic --settings=adex.settings.docker_dop457
CMD exec gunicorn adex.wsgi_docker_dop457:application --bind 0.0.0.0:8000 --workers 3

# build the image like this:
# docker build -t adex_api:latest .

# run the container from 'shared', like this:
# docker run -d --name adex_api --mount type=bind,source=/home/pi/shared,target=/shared -p 8004:8000 --restart always adex_api:latest

# log into the container
# docker exec -it adex_api sh
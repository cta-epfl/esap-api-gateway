FROM python:3.6.7-alpine
ENV PYTHONUNBUFFERED 1
RUN apk update && apk add gcc bash nano mc linux-headers musl-dev
RUN mkdir /src
WORKDIR /src
COPY . /src/
RUN pip install --upgrade pip  "cython==0.29.14" && pip install -r requirements/prod.txt
RUN exec python manage.py collectstatic --settings=esap.settings.docker_dop457 --no-input
CMD exec gunicorn esap.wsgi_docker_dop457:application --bind 0.0.0.0:8000 --workers 3

# build the image like this:
# docker build -t esap_api:latest .

# run the container from 'shared', like this:
# docker run -d --name esap_api --mount type=bind,source=/data/shared,target=/shared -p 8005:8000 --restart always esap_api:latest

# log into the container
# docker exec -it esap_api sh
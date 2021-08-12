FROM python:3.6.7-slim
RUN apt-get update && apt-get install --no-install-recommends -y bash nano mc

RUN mkdir /src
WORKDIR /src
COPY . /src/

RUN pip install --upgrade pip  "cython==0.29.14"
RUN pip install cryptography
RUN pip install -r requirements/prod.txt
RUN python manage.py collectstatic --settings=esap.settings.statics --no-input

RUN python manage.py migrate ida --database=ida --settings=esap.settings.dev --no-input
RUN python manage.py loaddata --database=ida --settings=esap.settings.dev esap/esap_ida_config.yaml

CMD exec gunicorn esap.wsgi_docker:application --bind 0.0.0.0:8000 --workers 3



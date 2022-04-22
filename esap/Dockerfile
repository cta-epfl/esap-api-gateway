FROM python:3.10-slim
RUN apt-get update && apt-get install --no-install-recommends -y bash nano mc libmagic1 git

RUN mkdir /src
WORKDIR /src
COPY . /src/

RUN pip install --upgrade pip
RUN pip install -r requirements/prod.txt
RUN python manage.py collectstatic --settings=esap.settings.statics --no-input

# create databases and import default configuration fixtures

# empty databases
RUN python manage.py migrate accounts --database=accounts --settings=esap.settings.dev --no-input
RUN python manage.py migrate rucio --database=rucio --settings=esap.settings.dev --no-input

# databases containing configuration settings
RUN python manage.py migrate ida --database=ida --settings=esap.settings.dev --no-input
RUN python manage.py loaddata --database=ida --settings=esap.settings.dev esap/esap_ida_config.yaml
RUN python manage.py migrate --settings=esap.settings.dev
RUN python manage.py loaddata --database=default --settings=esap.settings.dev esap/esap_config.yaml

CMD exec gunicorn esap.wsgi_docker:application --bind 0.0.0.0:8000 --workers 3



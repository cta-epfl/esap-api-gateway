python manage.py collectstatic --settings=esap.settings.statics --no-input

# create databases and import default configuration fixtures

# empty databases
python manage.py migrate accounts --database=accounts --settings=esap.settings.dev --no-input
python manage.py migrate rucio --database=rucio --settings=esap.settings.dev --no-input

# databases containing configuration settings
python manage.py migrate ida --database=ida --settings=esap.settings.dev --no-input
python manage.py loaddata --database=ida --settings=esap.settings.dev esap/esap_ida_config.yaml
python manage.py migrate --settings=esap.settings.dev
python manage.py loaddata --database=default --settings=esap.settings.dev esap/esap_config.yaml

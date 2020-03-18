import sys
from django.conf import settings

import importlib
sys.path.append(settings.CONFIGURATION_DIR)

my_config = importlib.import_module(settings.CONFIGURATION_FILE)

#my_config = __import__('dev')
#from esap.esap.configuration import esap_dev as my_config

# return expanded configuration
def get_configuration_from_settings():
    result = {}
    result['logo'] = my_config.logo
    result['title'] = my_config.title

    return result

# return expanded configuration
def get_configuration_from_database(configuration):
    result = {}
    result['logo'] = configuration.logo
    result['schema_datasets'] = configuration.schema_datasets
    return result
import os, sys
from django.conf import settings

import importlib

try:
    sys.path.append(settings.CONFIGURATION_DIR)
    my_config = importlib.import_module(settings.CONFIGURATION_FILE)
except:
    # no configuration definition found in settings.py, use the default configuration
    esap_default_config = os.path.join((os.path.join(settings.BASE_DIR, 'configuration'),'esap_default'))
    my_config = importlib.import_module(esap_default_config)


# return expanded configuration
def get_configuration():
    result = {}
    try:
        result['logo'] = my_config.logo
    except:
        pass

    try:
        result['title'] = my_config.title
    except:
        pass

    try:
        result['navbar'] = my_config.navbar
    except:
        pass

    try:
        result['query_schema'] = my_config.query_schema
    except:
        pass

    return result

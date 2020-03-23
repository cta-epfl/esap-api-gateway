import os, sys
from django.conf import settings

import importlib

try:
    sys.path.append(settings.CONFIGURATION_DIR)
    my_config = importlib.import_module(settings.CONFIGURATION_FILE)
except:
    # no configuration found, continue without configuration settings for the frontend.
    # (the frontend will have to use its defaults)
    pass

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

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


def get_datasets_enabled():
    return my_config.datasets_enabled

def get_datasets_disabled():
    return my_config.datasets_disabled

# return expanded configuration
def get_configuration():
    result = {}
    result['version'] = settings.VERSION

    try:
        result['frontend_basename'] = my_config.frontend_basename
    except:
        pass

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

    try:
        result['datasets_enabled'] = my_config.datasets_enabled
    except:
        pass

    try:
        result['datasets_disabled'] = my_config.datasets_disabled
    except:
        pass

    return result

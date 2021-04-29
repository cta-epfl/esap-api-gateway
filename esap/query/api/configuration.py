import os, sys
from django.conf import settings

import logging, importlib
logger = logging.getLogger(__name__)

try:
    sys.path.append(settings.CONFIGURATION_DIR)
    my_config = importlib.import_module(settings.CONFIGURATION_FILE)
except:
    # no configuration found, continue without configuration my_config = importlib.import_module(settings.CONFIGURATION_FILE)settings for the frontend.
    # (the frontend will have to use its defaults)
    pass


def get_datasets_enabled():
    return my_config.datasets_enabled

def get_datasets_disabled():
    return my_config.datasets_disabled

# return expanded configuration
def get_configuration(name=None, session=None):
    result = {}
    result['version'] = settings.VERSION

    # default the configuration from settings.CONFIGURATION_FILE is used,
    # but it can be overridden with the 'name' parameter like this
    # /esap-api/query/configuration?name=adex

    try:
        if name!=None:
            my_config = importlib.import_module(name,'configuration')
        else:
            my_config = importlib.import_module(settings.CONFIGURATION_FILE)

        # More sophisticated config files can embed the config in a class called Config
        try:
            my_config = my_config.Config(session)
        except AttributeError as e:
            pass

    except Exception as error:
        return {"configuration error in ": name+ ".py : " + str(error)}

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
        result['ui_schema'] = my_config.ui_schema
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

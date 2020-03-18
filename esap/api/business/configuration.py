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

    return result

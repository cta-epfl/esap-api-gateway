from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'query'
# experiment to start a samp client on startup... (warning, blocking)
#    def ready(self):
#        try:
#            print('importing samp')
#            from .api.services import samp
#            #samp()
#        except:
#            pass
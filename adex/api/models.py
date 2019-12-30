from django.db import models


"""
DataSource
"""
class DataSource(models.Model):

    name = models.CharField(max_length=40, default="unknown")
    instrument = models.CharField(max_length=30, default="unknown") # WSRT, Apertif, LOFAR
    description = models.CharField(max_length=1000, default="unknown")
    thumbnail = models.CharField(max_length=200, default="https://alta.astron.nl/alta-static/unknown.jpg")

    # the representation of the value in the REST API
    def __str__(self):
        return str(self.name) + ' (' + str(self.instrument) + ')'

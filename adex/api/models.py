from django.db import models


"""
DataSource
"""
class DataSource(models.Model):

    uri = models.CharField(max_length=40, null=False)    # unique identifier for this datasource
    instrument = models.CharField(max_length=30)         # like: WSRT, Apertif, LOFAR
    datatype = models.CharField(max_length=30)           # like: visibility, image, cube
    processing_level = models.CharField(max_length=30)   # like: raw, calibrated, processed

    name = models.CharField(max_length=40)               # label in GUI
    thumbnail_primary = models.URLField(default="https://alta.astron.nl/alta-static/unknown.jpg")
    thumbnail_secondary = models.URLField()

    archive_name = models.CharField(max_length=40)       # like: LOFAR LTA, ALTA, WSRT (MoM), VO
    archive_url = models.URLField()

    short_description = models.CharField(max_length=40)
    description = models.TextField(null=True)
    documentation_url = models.URLField(null=True)

    retrieval_description = models.TextField(null=True)
    scientific_description = models.TextField(null=True)


    # the representation of the value in the REST API
    def __str__(self):
        return str(self.name) + ' (' + str(self.instrument) + ')'

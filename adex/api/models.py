from django.db import models

"""
AdexBaseObject contains the shared fields
"""

class AdexBaseObject(models.Model):
    uri = models.CharField(max_length=40, null=False)  # unique identifier for this datasource
    name = models.CharField(max_length=40)             # label in GUI
    short_description = models.CharField(max_length=40)
    long_description = models.TextField(null=True)
    retrieval_description = models.TextField(null=True)

    thumbnail = models.URLField(default="https://alta.astron.nl/alta-static/unknown.jpg")
    documentation_url = models.URLField(null=True)

    def __str__(self):
        return str(self.uri)


"""
Archive
"""
class Archive(AdexBaseObject):

    instrument = models.CharField(max_length=30)
    catalog_name = models.CharField(max_length=30)
    catalog_url = models.URLField(null=True)

    def __str__(self):
        return str(self.uri)


"""
DataSet
"""
class DataSet(AdexBaseObject):
    datatype = models.CharField(max_length=30)  # like: visibility, image, cube
    processing_level = models.CharField(max_length=30)  # like: raw, calibrated, processed

    # note: the field is called 'data_archive' because 'archive' clashes in the database with the field adexbaseobject.archive.
    data_archive = models.ForeignKey(Archive, related_name='datasets', on_delete=models.CASCADE, null=True, blank=True)

    # the representation of the value in the REST API
    def __str__(self):
        return str(self.uri)




from django.db import models

"""
EsapBaseObject contains the shared fields
"""

class EsapBaseObject(models.Model):
    # type = models.CharField(max_length=15, null=False) # Archive, Catalog, CatalogService
    uri = models.CharField(max_length=40, null=False)  # unique identifier for this datasource
    name = models.CharField(max_length=40)             # label in GUI
    short_description = models.CharField(max_length=40)
    long_description = models.TextField(null=True, blank=True)
    retrieval_description = models.TextField(null=True, blank=True)

    thumbnail = models.URLField(default="https://alta.astron.nl/alta-static/unknown.jpg")
    documentation_url = models.URLField(null=True)

    institute = models.CharField(max_length=40)

    def __str__(self):
        return str(self.uri)

    @property
    def type_derived(self):
        my_type = "EsapBaseObject"

        if isinstance(self,Archive):
            my_type = "Archive"
        elif isinstance(self, Catalog):
            my_type = "Catalog"
        elif isinstance(self, CatalogService):
            my_type = "CatalogService"
        elif isinstance(self, DataSet):
            my_type = "Dataset"
        return my_type

"""
Catalog
"""
class Catalog(EsapBaseObject):
    url = models.URLField(null=True)

    # the representation of the value in the REST API
    def __str__(self):
        return str(self.uri)

"""
CatalogService
"""
class CatalogService(EsapBaseObject):

    # fields
    url = models.URLField(null=True)
    access_parameters = models.TextField(null=True)

    # relationships
    service_catalog = models.ForeignKey(Catalog, related_name='services', on_delete=models.CASCADE, null=True, blank=True)

    # the representation of the value in the REST API
    def __str__(self):
        return str(self.uri)


"""
Archive
"""
class Archive(EsapBaseObject):

    # fields
    instrument = models.CharField(max_length=30)
    # catalog_name = models.CharField(max_length=30)
    # catalog_url = models.URLField(null=True)

    # relationships
    # note: the field is called 'archive_catalog' because 'catalog' clashes in the database with the field esapbaseobject.catalog.
    archive_catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def catalog_name_derived(self):
        return self.archive_catalog.name

    @property
    def catalog_url_derived(self):
        return self.archive_catalog.url

    def __str__(self):
        return str(self.uri)


"""
DataSet
"""
class DataSet(EsapBaseObject):

    datatype = models.CharField(max_length=30)  # like: visibility, image, cube
    processing_level = models.CharField(max_length=30)  # like: raw, calibrated, processed

    # note: the field is called 'data_archive' because 'archive' clashes in the database with the field esapbaseobject.archive.
    data_archive = models.ForeignKey(Archive, related_name='datasets', on_delete=models.CASCADE, null=True, blank=True)

    @property
    def catalog_name_derived(self):
        return self.data_archive.catalog_name_derived

    @property
    def archive_name_derived(self):
        return self.data_archive.name

    @property
    def archive_uri_derived(self):
        return self.data_archive.uri

    # the representation of the value in the REST API
    def __str__(self):
        return str(self.uri)


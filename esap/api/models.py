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
    documentation_url = models.URLField(null=True, blank=True)

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
        #elif isinstance(self, CatalogService):
        #    my_type = "CatalogService"
        elif isinstance(self, DataSet):
            my_type = "Dataset"
        return my_type


"""
Every catalog service uses different parameters to access similar information
"""

class ParameterMapping(models.Model):

    # fields
    uri = models.CharField(max_length=15, null=False) # vo, alta, ...

    # this is a json object containing all parameter mappings for this uri
    parameters = models.TextField(null=True, blank=True)

    # the representation of the value in the REST API
    def __str__(self):
        return str(self.uri) + ' = ' + str(self.parameters)


"""
Catalog
"""
class Catalog(EsapBaseObject):
    ADQL = 'adql'
    HTTP = 'http'
    PROTOCOL = [
        (ADQL, ADQL),
        (HTTP, HTTP),
    ]

    J2000 = 'J2000'
    ICRS = 'ICRS'
    EQUINOX = [
        (J2000, J2000),
        (ICRS, ICRS),
    ]


    # query_base determines which algorithm is used to create and run queries.
    esap_service = models.CharField(default='vo',max_length=15) # vo, alta, vso

    equinox = models.CharField(default=ICRS, max_length=10, choices=EQUINOX) # J2000, ICRS
    protocol = models.CharField(max_length=15, choices=PROTOCOL)  # adql, http

    # the url for the user (this brings the user to an external web page)
    user_url = models.URLField(null=True)

    # the url that the query has to access
    url = models.URLField(null=True)
    parameters = models.ForeignKey(ParameterMapping, related_name='catalogs', on_delete=models.CASCADE, null=True, blank=True)

    # relationships
    # datasets = models.ForeignKey(DataSet, related_name = 'catalogs', on_delete=models.CASCADE, null=True, blank=True)

     # the representation of the value in the REST API
    def __str__(self):
        return str(self.uri)


"""
Archive
"""
class Archive(EsapBaseObject):

    # fields
    instrument = models.CharField(max_length=30)

    def __str__(self):
        return str(self.uri)


"""
DataSet
"""
class DataSet(EsapBaseObject):
    LIST = 'list'
    TILES = 'tiles'
    OUTPUT_FORMAT = [
        (LIST, LIST),
        (TILES, TILES),
    ]

    datatype = models.CharField(max_length=30)  # like: visibility, image, cube
    processing_level = models.CharField(max_length=30)  # like: raw, calibrated, processed

    # relationships
    dataset_catalog = models.ForeignKey(Catalog, related_name = 'datasets', on_delete=models.CASCADE, null=True, blank=True)

    # note: the field is called 'data_archive' because 'archive' clashes in the database with the field esapbaseobject.archive.
    dataset_archive = models.ForeignKey(Archive, related_name='datasets', on_delete=models.CASCADE, null=True, blank=True)

    # datasets could use the same catalog, but accessing different tables...
    resource_name =  models.CharField(max_length=30, null=True, blank=True)  # like: ivoa.obscore, activities, observations

    # ... and returning different results based on the SELECT statement
    select_fields =  models.CharField(default="*", max_length=100, null=True, blank=True)  # like: raw, calibrated, processed

    # Identify some (non mandatory) fields in the remote dataset that hold values to used by a frontend to render the output
    title_field  = models.CharField(max_length=30, null=True, blank=True) # a field for a title of the dataproduct
    thumbnail_field = models.CharField(max_length=30, null=True, blank=True)              # a url to a preview thumbnail
    url_field = models.CharField(max_length=30, null=True, blank=True)                    # the url to the data itself

    # Extra info for a frontend about how to render the output
    output_format = models.CharField(default=LIST, max_length=10, choices=OUTPUT_FORMAT) # list,tiles

    # The connector refers to the business logic in the services directory that handles the query to the specific catalog
    service_connector = models.CharField(max_length=80, null=True, blank=True) # vo.tap_service_connector, alta.observations_connector, ...


    @property
    def catalog_name_derived(self):
        return self.dataset_catalog.name

    @property
    def catalog_uri_derived(self):
        return self.dataset_catalog.uri

    @property
    def catalog_url_derived(self):
        return self.dataset_catalog.url

    @property
    def catalog_user_url_derived(self):
        return self.dataset_catalog.user_url


    @property
    def archive_name_derived(self):
        return self.dataset_archive.name

    @property
    def archive_uri_derived(self):
        return self.dataset_archive.uri


    # the representation of the value in the REST API
    def __str__(self):
        return str(self.uri)

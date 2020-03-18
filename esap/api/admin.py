from django.contrib import admin
from .models import EsapBaseObject, Archive, DataSet, Catalog, ParameterMapping, Configuration

admin.site.register(EsapBaseObject)
admin.site.register(Archive)
admin.site.register(DataSet)
admin.site.register(Catalog)
#admin.site.register(CatalogService)
admin.site.register(ParameterMapping)
admin.site.register(Configuration)
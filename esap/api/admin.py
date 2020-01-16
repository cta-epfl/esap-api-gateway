from django.contrib import admin
from .models import AdexBaseObject, Archive, DataSet

admin.site.register(AdexBaseObject)
admin.site.register(Archive)
admin.site.register(DataSet)
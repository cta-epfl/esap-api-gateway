from django.db import models
from django.db.models import Q
import django_filters


class Batch(models.Model):
    uri = models.CharField(max_length=40, null=False)
    status = models.CharField(max_length=40, null=False)
    
    


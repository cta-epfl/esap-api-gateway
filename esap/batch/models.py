from django.db import models
from django.db.models import Q
import django_filters


class Batch(models.Model):
    uri = models.CharField(max_length=40, null=False)
    status = models.CharField(max_length=40, null=False)
    
    
"""
Facility
"""
class Facility(models.Model):

    # fields
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=240)
    url = models.CharField(max_length=240)
    facilitytype = models.CharField(max_length=240)


    def __str__(self):
        return str(self.name)
   

"""
Workflow
"""
class Workflow(models.Model):

    # fields
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=240)
    url = models.CharField(max_length=240)
    ref = models.CharField(max_length=240, default="HEAD")
    filepath = models.CharField(max_length=240, blank=True)
    workflowtype = models.CharField(max_length=240)
    
    def __str__(self):
        return str(self.name)


"""
ShoppingCart
"""
class ShoppingCart(models.Model):

    # fields
    user = models.PositiveIntegerField()
    workflow = models.ForeignKey(Workflow,  models.CASCADE)
    facility = models.ForeignKey(Facility, models.CASCADE) 
    dataset = models.PositiveIntegerField()
    datatype = models.CharField(max_length=240) 

    def __str__(self):
        return str(self.name)



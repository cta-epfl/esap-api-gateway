from django.db import models
from django.db.models import Q
import django_filters


class Ida(models.Model):
    uri = models.CharField(max_length=40, null=False)
    status = models.CharField(max_length=40, null=False)


class Facility(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=240)
    url = models.CharField(max_length=240)
    facilitytype = models.CharField(max_length=240)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ["facilitytype", "name"]


class Workflow(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=240)
    url = models.CharField(max_length=240)
    ref = models.CharField(max_length=240, default="HEAD", null=True)
    filepath = models.CharField(max_length=240, blank=True, null=True)
    workflowtype = models.CharField(max_length=240)
    keywords = models.CharField(max_length=240, null=True)
    author = models.CharField(max_length=240, null=True)
    runtimePlatform = models.CharField(max_length=240, null=True)

    def __str__(self):
        return str(self.name)


class ShoppingCart(models.Model):
    user = models.PositiveIntegerField()
    workflow = models.ForeignKey(Workflow, models.CASCADE)
    facility = models.ForeignKey(Facility, models.CASCADE)
    dataset = models.PositiveIntegerField()
    datatype = models.CharField(max_length=240)

    def __str__(self):
        return str(self.name)

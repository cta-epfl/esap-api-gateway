from django.db import models

class Staging(models.Model):
    uri = models.CharField(max_length=40, null=False)
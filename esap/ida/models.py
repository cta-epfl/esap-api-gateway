from django.db import models

class Ida(models.Model):
    uri = models.CharField(max_length=40, null=False)

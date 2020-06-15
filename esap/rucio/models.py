from django.db import models
from django.contrib.auth.models import User

class Staging(models.Model):
    task = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User, related_name="staging", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.task
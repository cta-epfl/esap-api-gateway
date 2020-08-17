from django.db import models
from django.contrib.auth.models import User

class Rucio(models.Model):
    task = models.CharField(max_length=255)
    # owner = models.ForeignKey(User, related_name="rucio", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.task
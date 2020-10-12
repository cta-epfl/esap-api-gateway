from django.db import models

class Ida(models.Model):
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

    def __str__(self):
        return str(self.name)
    
    @property
    def type_derived(self):
        my_type = "Facility"

        if isinstance(self,JupyterHubFacility):
            my_type = "JupyterHub"
        else:
            my_type = "Other"
        return my_type

"""
Workflow
"""
class Workflow(models.Model):

    # fields
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=240)
    url = models.CharField(max_length=240)
    workflowtype = models.CharField(max_length=240)
    
    def __str__(self):
        return str(self.name)



"""
JupyterHubFacility
"""
class JupyterHubFacility(Facility):

    # fields
    version = models.CharField(max_length=30)
    
    def __str__(self):
        return str(self.name)


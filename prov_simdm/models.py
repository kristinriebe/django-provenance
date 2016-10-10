from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible
class Party(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    label = models.CharField(max_length=128, null=True) # human readable label, firstname + lastname
    type = models.CharField(max_length=128, null=True, choices=AGENT_TYPE_CHOICES) # types of entities: single entity, dataset
    description = models.CharField(max_length=1024, blank=True, null=True)
    affiliation = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.label

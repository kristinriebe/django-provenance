from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible
class Party(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=128, null=True) # human readable label, firstname + lastname
    #email = models.CharField(max_length=1024, blank=True, null=True)
    #address = models.CharField(max_length=1024, blank=True, null=True)
    #telephone = models.CharField(max_length=1024, blank=True, null=True)
    def __str__(self):
        return self.label

class Experiment(models.Model):
    id = models.CharField(primary_key=True, max_length=128)  # new from prov
    executionTime = models.DateTimeField(null=True) # == voprov:endTime
    protocol = models.ForeignKey("Protocol", null=True, on_delete=models.SET_NULL) # == voprov:activitydescription
    name = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.name

class Protocol(models.Model):
    id = models.CharField(primary_key=True, max_length=128)  # new from prov
    name = models.CharField(max_length=128, blank=True, null=True) # = name of the code, not included in SimDM
    code = models.CharField(max_length=128, blank=True, null=True) # must be a URI, for downloading the code!!
    version = models.CharField(max_length=32, blank=True, null=True)
    def __str__(self):
        return self.name

class AppliedAlgorithm(models.Model):
    id = models.CharField(primary_key=True, max_length=128)  # new from prov
    algorithm = models.ForeignKey("Algorithm", null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.id

class Algorithm(models.Model):
    id = models.CharField(primary_key=True, max_length=128)  # new from prov
    # This class is used in collections with AppliedAlgorithm for Experiment
    # and used directly (again as collection, contains-relationship) with protocol.
    # For modelling the relation, we therefore add here a reference to the "one"-side of the many-to-one-relationship with protocol
    name = models.CharField(max_length=1024, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    label = models.CharField(max_length=1024, blank=True, null=True) # should actually be one of the SKOS-vocabularies, = skoscocept
    protocol = models.ForeignKey("Protocol", null=True, on_delete=models.SET_NULL)  # should actually not be null!! composition-relationship!
    code = models.CharField(max_length=128, blank=True, null=True) # additional attribute; added because I don't want it in Protocol

    def __str__(self):
        return self.name

class InputParameter(models.Model):
    id = models.CharField(primary_key=True, max_length=128)  # new from prov
    # This is refered to as "parameter" from Protocol
    label = models.CharField(max_length=1024, blank=True, null=True) # SKOS label

class ParameterSetting(models.Model):
    id = models.CharField(primary_key=True, max_length=128)  # new from prov
    # since parameters values could be of any type, but we cannot easily model this, 
    # a compromise was made: numericValue is set if the value is double, integer, ...; stringValue is used for other cases
    stringValue = models.CharField(max_length=128, blank=True, null=True)
    numericValue = models.CharField(max_length=128, blank=True, null=True)
    # The numericValue should in fact be a "quantity"! But I don't have this datatype defined here. It would consist of a value (type real) and a unit
    label = models.ForeignKey("InputParameter")



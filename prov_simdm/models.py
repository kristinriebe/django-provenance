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
        return self.id

    def get_viewattributes(self):
        attributes = [
            'id',
            'name',
        ]
        return attributes


class Experiment(models.Model):
    id = models.CharField(primary_key=True, max_length=128)  # new from prov
    executionTime = models.DateTimeField(null=True) # == voprov:endTime
    protocol = models.ForeignKey("Protocol", null=True, on_delete=models.SET_NULL) # == voprov:activitydescription
    name = models.CharField(max_length=1024, blank=True, null=True)
    #description = 
    #referenceURL = 
    #created = 

    def __str__(self):
        return self.id

    def get_viewattributes(self):
        attributes = [
            'id',
            'name',
            'executionTime',
            'protocol'
        ]
        return attributes


class Protocol(models.Model):
    id = models.CharField(primary_key=True, max_length=128)  # new from prov
    name = models.CharField(max_length=128, blank=True, null=True) # = name of the code, not included in SimDM
    code = models.CharField(max_length=128, blank=True, null=True) # must be a URI, for downloading the code!!
    version = models.CharField(max_length=32, blank=True, null=True)
    description = models.CharField(max_length=32, blank=True, null=True)
    referenceURL = models.CharField(max_length=32, blank=True, null=True)
    #parameters = [] see InputParameter-class, which refers back to Protocol

    def __str__(self):
        return self.id

    def get_viewattributes(self):
        attributes = [
            'id',
            'name',
            'code',
            'version',
            'description',
            'referenceURL'
        ]
        return attributes


class AppliedAlgorithm(models.Model):
    id = models.AutoField(primary_key=True)
    algorithm = models.ForeignKey("Algorithm", null=True, on_delete=models.SET_NULL)
    experiment = models.ForeignKey("Experiment", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.id

    def get_viewattributes(self):
        attributes = [
            'id',
            'algorithm',
            'experiment'
        ]
        return attributes

class Algorithm(models.Model):
    id = models.CharField(primary_key=True, max_length=128)  # new from prov
    # This class is used in collections with AppliedAlgorithm for Experiment
    # and used directly (again as collection, contains-relationship) with protocol.
    # For modelling the relation, we therefore add here a reference to the "one"-side of the many-to-one-relationship with protocol
    name = models.CharField(max_length=1024, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    label = models.CharField(max_length=1024, blank=True, null=True) # should actually be one of the SKOS-vocabularies, = skoscocept
    protocol = models.ForeignKey("Protocol", null=True, on_delete=models.SET_NULL)  # should actually not be null!! composition-relationship!

    def __str__(self):
        return self.id

    def get_viewattributes(self):
        attributes = [
            'id',
            'name',
            'description',
            'label',
            'protocol'
        ]
        return attributes


class InputParameter(models.Model):
    id = models.CharField(primary_key=True, max_length=128)  # new from prov
    # This is refered to as "parameter" from Protocol
    protocol = models.ForeignKey("Protocol", null=True, on_delete=models.SET_NULL)
    # additional attributes for more usefulness:
    name = models.CharField(max_length=1024, blank=True, null=True)
    datatype = models.CharField(max_length=128, null=True)
    #unit = models.CharField(max_length=128, null=True)
    #ucd = models.CharField(max_length=128, null=True)
    #utype = models.CharField(max_length=128, null=True)
    #arraysize = models.CharField(max_length=128, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.id

    def get_viewattributes(self):
        attributes = [
            'id',
            'name',
            'datatype',
            'description',
            'protocol'
        ]
        return attributes


class ParameterSetting(models.Model):
    id = models.AutoField(primary_key=True)  # added for convenience
    # since parameters values could be of any type, but we cannot easily model this, 
    # a compromise was suggested for SimDM: numericValue is set if the value is double, integer, ...; stringValue is used for other cases;
    # but numericValue would be a quantity, consisting of value and unit; we simplifiy here by just using
    # a string, that contains the unit, if needed
    value = models.CharField(max_length=128, blank=True, null=True)
    inputParameter = models.ForeignKey("InputParameter", null=True, on_delete=models.SET_NULL) # not one-to-one, since there can be many instances of an experiment with its params
    experiment = models.ForeignKey("Experiment", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.id

    def get_viewattributes(self):
        attributes = [
            'id',
            'value',
            'inputParameter',
            'experiment'
        ]
        return attributes




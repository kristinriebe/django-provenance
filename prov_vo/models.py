from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.http import JsonResponse


ACTIVITY_TYPE_CHOICES = (
    ('cs:simulation', 'cs:simulation'),
    ('cs:processing', 'cs:processing'),
)
ACTIVITY_SUBTYPE_CHOICES = (
    ('cs:halofinding', 'cs:halofinding'),
    ('cs:mergertree-generation', 'cs:mergertree-generation'),
    ('cs:substructuretree-generation', 'cs:substructuretree-generation'),
)
AGENT_TYPE_CHOICES = (
    ('voprov:Project','voprov:Project'),
    ('prov:Person','prov:Person'),
)

# main ProvDM classes:
@python_2_unicode_compatible
class Activity(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    label = models.CharField(max_length=128, null=True)  # should require this, otherwise do not know what to show!
    description = models.ForeignKey("ActivityDescription", null=True)
#    parametervalues  = models.CharField(max_length=1024, blank=True, null=True)   
    annotation = models.CharField(max_length=1024, blank=True, null=True)
    startTime = models.DateTimeField(null=True)  # should be: null=False, default=timezone.now())
    endTime = models.DateTimeField(null=True)  # should be: null=False, default=timezone.now())
    docuLink = models.CharField('documentation link', max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.label
        # maybe better use self.id here??

    def get_viewattributes(self):
        attributes = [
            'id',
            'label',
            'description',
            'annotation',
            'startTime',
            'endTime',
            'docuLink'
        ]
        return attributes


    # TODO: add getjson to each class, use in json-serialisation
    def getjson(self, activity_id):
        activity_dict = {'id': id, 'label': label, 'description': description}
        return JsonResponse(activity_dict)


@python_2_unicode_compatible
class ActivityFlow(Activity):

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class ActivityDescription(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    label = models.CharField(max_length=128, null=True) # should require this, otherwise do not know what to show!
    type = models.CharField(max_length=128, null=True, choices=ACTIVITY_TYPE_CHOICES)
    subtype = models.CharField(max_length=128, blank=True, null=True, choices=ACTIVITY_SUBTYPE_CHOICES)
#    parametertypes = models.CharField(max_length=2048, blank=True, null=True)  # should actually be a json-construct
    description = models.CharField(max_length=1024, blank=True, null=True)
    docuLink = models.CharField('documentation link', max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.label

    def get_viewattributes(self):
        attributes = [
            'id',
            'label',
            'type',
            'subtype',
            'description',
            'docuLink'
        ]
        return attributes


@python_2_unicode_compatible
class Entity(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    label = models.CharField(max_length=128, null=True)
    type = models.CharField(max_length=128, null=True)
    location = models.CharField(max_length=128, null=True)
    access = models.CharField(max_length=128, null=True)
    size = models.CharField(max_length=128, null=True)
    format = models.CharField(max_length=128, null=True)
    annotation = models.CharField(max_length=1024, blank=True, null=True)
    description = models.ForeignKey("EntityDescription", null=True)

    def __str__(self):
        return self.label

    def get_viewattributes(self):
        attributes = [
            'id',
            'label',
            'type',
            'location',
            'access',
            'size',
            'format',
            'annotation',
            'description'
        ]
        return attributes


@python_2_unicode_compatible
class EntityDescription(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    label = models.CharField(max_length=128, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    docuLink = models.CharField('documentation link', max_length=512, blank=True, null=True)
    # (= url)
    dataproduct_type = models.CharField(max_length=128, null=True)
    dataproduct_subtype = models.CharField(max_length=128, null=True)
    level = models.IntegerField()

    def __str__(self):
        return self.label

    def get_viewattributes(self):
        attributes = [
            'id',
            'label',
            'description',
            'docuLink',
            'dataproduct_type',
            'dataproduct_subtype',
            'level'
        ]
        return attributes


# new classes for parameters
@python_2_unicode_compatible
class Parameter(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.ForeignKey("ParameterDescription", null=True)
    # = "label" in current working draft (21-11-2016)!!
    value = models.CharField(max_length=128, null=True)
    activity = models.ForeignKey("Activity", null=True)

    def __str__(self):
        return self.value

    def get_viewattributes(self):
        attributes = [
            'id',
            'description',
            'value',
            'activity'
        ]
        return attributes


@python_2_unicode_compatible
class ParameterDescription(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    label = models.CharField(max_length=128, null=True)
    activitydescription = models.ForeignKey("ActivityDescription", null=True)
    datatype = models.CharField(max_length=128, null=True)
    unit = models.CharField(max_length=128, null=True)
    ucd = models.CharField(max_length=128, null=True)
    utype = models.CharField(max_length=128, null=True)
    arraysize = models.CharField(max_length=128, null=True)
    annotation = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.label

    # define the attributes that shall/may be displayed in the detail view
    # for this class
    def get_viewattributes(self):
        attributes = [
            'id',
            'label',
            'activitydescription',
            'datatype',
            'unit',
            'ucd',
            'utype',
            'arraysize',
            'annotation'
        ]
        return attributes


@python_2_unicode_compatible
class Agent(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    name = models.CharField(max_length=128, null=True) # human readable label, firstname + lastname
    type = models.CharField(max_length=128, null=True, choices=AGENT_TYPE_CHOICES) # types of entities: single entity, dataset
    affiliation = models.CharField(max_length=1024, null=True)

    def __str__(self):
        return self.label

    def get_viewattributes(self):
        attributes = [
            'id',
            'name',
            'type',
            'affiliation'
        ]
        return attributes


# relation classes
@python_2_unicode_compatible
class Used(models.Model):
    id = models.AutoField(primary_key=True)
    activity = models.ForeignKey(Activity, null=True) #, on_delete=models.CASCADE) # Should be required!
    entity = models.ForeignKey(Entity, null=True) #, on_delete=models.CASCADE) # Should be required!
    description = models.ForeignKey("UsedDescription", null=True)

    def __str__(self):
        return "id=%s; activity=%s; entity=%s; desc.id=%s" % (str(self.id), self.activity, self.entity, self.description)


@python_2_unicode_compatible
class UsedDescription(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    activitydescription = models.ForeignKey(ActivityDescription, null=True) #, on_delete=models.CASCADE) # Should be required!
    entitydescription = models.ForeignKey(EntityDescription, null=True)     #, on_delete=models.CASCADE) # Should be required!
    role = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "id=%s; activity=%s; entity=%s; role=%s" % (str(self.id), self.activity, self.entity, self.role)

@python_2_unicode_compatible
class WasGeneratedBy(models.Model):
    id = models.AutoField(primary_key=True)
    entity = models.ForeignKey(Entity, null=True) #, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, null=True) #, on_delete=models.CASCADE)
    description = models.ForeignKey("WasGeneratedByDescription", null=True)

    def __str__(self):
        return "id=%s; entity=%s; activity=%s; desc.id=%s" % (str(self.id), self.entity, self.activity, self.description)


@python_2_unicode_compatible
class WasGeneratedByDescription(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    entitydescription = models.ForeignKey(EntityDescription, null=True) #, on_delete=models.CASCADE)
    activitydescription = models.ForeignKey(ActivityDescription, null=True) #, on_delete=models.CASCADE)
    role = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "id=%s; entity=%s; activity=%s; role=%s" % (str(self.id), self.entity, self.activity, self.role)


@python_2_unicode_compatible
class WasAssociatedWith(models.Model):
    id = models.AutoField(primary_key=True)
    activity = models.ForeignKey(Activity, null=True) 
    agent = models.ForeignKey(Agent, null=True) #, on_delete=models.CASCADE)
    role = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "id=%s; activity=%s; agent=%s; role=%s" % (str(self.id), self.activity, self.agent, self.role)


@python_2_unicode_compatible
class WasAttributedTo(models.Model):
    id = models.AutoField(primary_key=True)
    entity = models.ForeignKey(Entity, null=True) 
    agent = models.ForeignKey(Agent, null=True) #, on_delete=models.CASCADE)
    role = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "id=%s; entity=%s; agent=%s; role=%s" % (str(self.id), self.entity, self.agent, self.role)


@python_2_unicode_compatible
class WasDerivedFrom(models.Model):
    id = models.AutoField(primary_key=True)
    entity = models.ForeignKey(Entity, null=True) 
    progenitor = models.ForeignKey(Entity, null=True, related_name='progenitor')

    def __str__(self):
        return "id=%s; entity=%s; progenitor=%s" % (str(self.id), self.entity, self.progenitor)


@python_2_unicode_compatible
class HadStep(models.Model):
    id = models.AutoField(primary_key=True)
    activityflow = models.ForeignKey(ActivityFlow, null=True, related_name='activityflow') 
    activity = models.ForeignKey(Activity, null=True)

    def __str__(self):
        return "id=%s; activityflow=%s; activity=%s;" % (str(self.id), self.activityflow, self.activity)

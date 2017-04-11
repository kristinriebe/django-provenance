from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.http import JsonResponse


ACTIVITY_TYPE_CHOICES = (
    ('cs:simulation', 'cs:simulation'),
    ('cs:post-processing', 'cs:postprocessing'),
)
ACTIVITY_SUBTYPE_CHOICES = (
    ('cs:halofinder', 'cs:halofinder'),
    ('cs:mergertreebuilding', 'cs:mergertreebuilding'),
    ('cs:galaxybuilding', 'cs:galaxybuilding'),
)
AGENT_TYPE_CHOICES = (
    ('prov:Person', 'prov:Person'),
    ('prov:Organization', 'prov:Organization'),
)

AGENT_ROLE_CHOICES = (
    ("publisher", "publisher"),
    ("creator", "creator"),
    ("publisher", "operator"),
)


# main ProvDM classes:
@python_2_unicode_compatible
class Activity(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    label = models.CharField(max_length=128, null=True)  # should require this, otherwise do not know what to show!
    description = models.ForeignKey("ActivityDescription", null=True, on_delete=models.SET_NULL)
    annotation = models.CharField(max_length=1024, blank=True, null=True)
    startTime = models.DateField(null=True)  # should be: null=False, default=timezone.now())
    endTime = models.DateField(null=True)  # should be: null=False, default=timezone.now())
    doculink = models.CharField('documentation link', max_length=1024, blank=True, null=True)
    usedEntities = models.ManyToManyField("Entity", through="Used", related_name="usedForActivities")
    agents = models.ManyToManyField("Agent", through="WasAssociatedWith", related_name="associatedActivities")

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
            'doculink'
        ]
        return attributes

    def get_json(self):
        obj_dict = {}
        obj_dict[self.id] = {
            'prov:id': self.id,
            'prov:label': self.label,
            'prov:startTime': str(self.startTime),
            'prov:endTime': str(self.endTime),
            'vprov:annotation': self.annotation,
            'voprov:doculink': self.doculink,
            'voprov:type': self.description.type,
            'voprov:subtype': self.description.subtype,
            'voprov:description_label': self.description.label,
            'voprov:description_annotation': self.description.annotation,
            'voprov:description_doculink': self.description.doculink
        }
        print self.startTime
        return obj_dict

    def get_agents(self):
        agent_dict = Agent.objects.filter(wasassociatedwith__activity_id = self.id)
        return agent_dict


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
    annotation = models.CharField(max_length=1024, blank=True, null=True) # should be called annotation!
    doculink = models.CharField('documentation link', max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.id

    def get_viewattributes(self):
        attributes = [
            'id',
            'label',
            'type',
            'subtype',
            'annotation',
            'doculink'
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
    description = models.ForeignKey("EntityDescription", null=True, on_delete=models.SET_NULL)
    # note: in fact there should be only 1 generation activity! but there may be many activity-flows related to this entity
    generationActivities = models.ManyToManyField("Activity", through="WasGeneratedBy", related_name="generatedEntities")
    progenitors = models.ManyToManyField("self", through="WasDerivedFrom", related_name="derivatives", symmetrical=False)
    agents = models.ManyToManyField("Agent", through="WasAttributedTo", related_name="attributedEntities")

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


    def get_json(self):
        obj_dict = {}
        obj_dict[self.id] = {
            'prov:id': self.id,
            'prov:label': self.label,
            'prov:type': self.type,
            'cs:location': self.location,
            'cs:access': self.access,
            'cs:size': self.size,
            'cs:format': self.format,
            'voprov:annotation': self.annotation,
            'voprov:description_label': self.description.label,
            'voprov:description_doculink': self.description.doculink,
            'voprov:description_annotation': self.description.annotation,
            'voprov:dataproduct_type': self.description.dataproduct_type,
            'voprov:dataproduct_subtype': self.description.dataproduct_subtype,
            'voprov:level': self.description.level
        }
        return obj_dict


@python_2_unicode_compatible
class EntityDescription(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    label = models.CharField(max_length=128, null=True)
    annotation = models.CharField(max_length=1024, blank=True, null=True)
    doculink = models.CharField('documentation link', max_length=512, blank=True, null=True)
    # (= url)
    dataproduct_type = models.CharField(max_length=128, null=True)
    dataproduct_subtype = models.CharField(max_length=128, null=True)
    level = models.IntegerField()

    def __str__(self):
        return self.id

    def get_viewattributes(self):
        attributes = [
            'id',
            'label',
            'annotation',
            'doculink',
            'dataproduct_type',
            'dataproduct_subtype',
            'level'
        ]
        return attributes


# new classes for parameters
@python_2_unicode_compatible
class Parameter(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.ForeignKey("ParameterDescription", null=True, on_delete=models.SET_NULL)
    # = "label" in current working draft (21-11-2016)!!
    value = models.CharField(max_length=128, null=True)
    activity = models.ForeignKey("Activity", null=True, on_delete=models.SET_NULL)
    annotation = models.CharField(max_length=128, null=True, blank=True)

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

    def get_json(self):
        obj_dict = {}
        obj_dict[self.id] = {
            'prov:id': self.id,
            'prov:value': self.label,
            'prov:label': self.description.label,
            'voprov:activity': self.activity.id,
            'voprov:datatype': self.description.datatype,
            'voprov:unit': self.description.unit,
            'voprov:ucd': self.description.ucd,
            'voprov:utype': self.description.utype,
            'voprov:arraysize': self.description.arraysize,
            'voprov:annotation': self.annotation
         }
        return obj_dict


@python_2_unicode_compatible
class ParameterDescription(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    label = models.CharField(max_length=128, null=True)
    activitydescription = models.ForeignKey("ActivityDescription", null=True, on_delete=models.SET_NULL)
    datatype = models.CharField(max_length=128, null=True)
    unit = models.CharField(max_length=128, null=True)
    ucd = models.CharField(max_length=128, null=True)
    utype = models.CharField(max_length=128, null=True)
    arraysize = models.CharField(max_length=128, null=True)
    annotation = models.CharField(max_length=1024, blank=True, null=True)

    # add min, max and default value, for nicer search forms
    minval = models.CharField(max_length=128, blank=True, null=True)
    maxval = models.CharField(max_length=128, blank=True, null=True)
    default = models.CharField(max_length=128, blank=True, null=True)


    def __str__(self):
        return self.id

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
    label = models.CharField(max_length=128, null=True) # human readable label, firstname + lastname or project name
    type = models.CharField(max_length=128, null=True, choices=AGENT_TYPE_CHOICES) # types of agent
    affiliation = models.CharField(max_length=1024, blank=True, null=True)
    annotation = models.CharField(max_length=1024, blank=True, null=True)
    webpage = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.label

    def get_viewattributes(self):
        attributes = [
            'id',
            'label',
            'type',
            'affiliation'
        ]
        return attributes

    def get_json(self):
        obj_dict = {}
        obj_dict[self.id] = {
            'prov:id': self.id,
            'prov:label': self.label,
            'prov:type': self.type,
            'voprov:affiliation': self.affiliation
         }
        return obj_dict


# relation classes
# in principle, all of these classes are many-to-many-relations
@python_2_unicode_compatible
class Used(models.Model):
    id = models.AutoField(primary_key=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)  # models.CASCADE: delete the entry, if activity does not exist anymore
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    description = models.ForeignKey("UsedDescription", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "id=%s; activity=%s; entity=%s; desc.id=%s" % (str(self.id), self.activity, self.entity, self.description)

    def get_json(self):
        obj_dict = {}
        obj_dict[self.id] = {
            'prov:id': self.id,
            'prov:activity': self.activity.id,
            'prov:entity': self.entity.id,
            'voprov:role': self.description.role
        }
        return obj_dict


@python_2_unicode_compatible
class UsedDescription(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    activitydescription = models.ForeignKey(ActivityDescription, on_delete=models.CASCADE)
    entitydescription = models.ForeignKey(EntityDescription, on_delete=models.CASCADE)
    role = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "id=%s; activity=%s; entity=%s; role=%s" % (str(self.id), self.activity, self.entity, self.role)


@python_2_unicode_compatible
class WasGeneratedBy(models.Model):
    id = models.AutoField(primary_key=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    description = models.ForeignKey("WasGeneratedByDescription", null=True, on_delete=models.SET_NULL)
    # time

    def __str__(self):
        return "id=%s; entity=%s; activity=%s; desc.id=%s" % (str(self.id), self.entity, self.activity, self.description)

    def get_json(self):
        obj_dict = {}
        obj_dict[self.id] = {
            'prov:id': self.id,
            'prov:entity': self.entity.id,
            'prov:activity': self.activity.id,
            'voprov:role': self.description.role
        }
        return obj_dict


@python_2_unicode_compatible
class WasGeneratedByDescription(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    entitydescription = models.ForeignKey(EntityDescription, on_delete=models.CASCADE)
    activitydescription = models.ForeignKey(ActivityDescription, on_delete=models.CASCADE)
    role = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "id=%s; entity=%s; activity=%s; role=%s" % (str(self.id), self.entity, self.activity, self.role)


@python_2_unicode_compatible
class WasAssociatedWith(models.Model):
    id = models.AutoField(primary_key=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    role = models.CharField(max_length=128, blank=True, null=True, choices=AGENT_ROLE_CHOICES)

    def __str__(self):
        return "id=%s; activity=%s; agent=%s; role=%s" % (str(self.id), self.activity, self.agent, self.role)

    def get_json(self):
        obj_dict = {}
        obj_dict[self.id] = {
            'prov:id': self.id,
            'prov:activity': self.activity.id,
            'prov:agent': self.agent.id,
            'voprov:role': self.role
        }
        return obj_dict


@python_2_unicode_compatible
class WasAttributedTo(models.Model):
    id = models.AutoField(primary_key=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    role = models.CharField(max_length=128, blank=True, null=True, choices=AGENT_ROLE_CHOICES)

    def __str__(self):
        return "id=%s; entity=%s; agent=%s; role=%s" % (str(self.id), self.entity, self.agent, self.role)

    def get_json(self):
        obj_dict = {}
        obj_dict[self.id] = {
            'prov:id': self.id,
            'prov:entity': self.entity.id,
            'prov:agent': self.agent.id,
            'voprov:role': self.role
        }
        return obj_dict


@python_2_unicode_compatible
class WasDerivedFrom(models.Model):
    id = models.AutoField(primary_key=True)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    progenitor = models.ForeignKey(Entity, related_name='progenitor', on_delete=models.CASCADE)

    def __str__(self):
        return "id=%s; entity=%s; progenitor=%s" % (str(self.id), self.entity, self.progenitor)

    def get_json(self):
        obj_dict = {}
        obj_dict[self.id] = {
            'prov:id': self.id,
            'prov:generatedEntity': self.entity.id,
            'prov:usedEntity': self.progenitor.id,
        }
        return obj_dict


@python_2_unicode_compatible
class HadStep(models.Model):
    id = models.AutoField(primary_key=True)
    activityflow = models.ForeignKey(ActivityFlow, related_name='activityflow', on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        return "id=%s; activityflow=%s; activity=%s;" % (str(self.id), self.activityflow, self.activity)

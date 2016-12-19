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
)

AGENT_TYPE_CHOICES = (
    ('voprov:Project','voprov:Project'),
    ('prov:Person','prov:Person'),
)


# main ProvDM classes:
@python_2_unicode_compatible
class Activity(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    label = models.CharField(max_length=128, null=True) # should require this, otherwise do not know what to show!
    startTime = models.DateTimeField(null=True) # should be: null=False, default=timezone.now())
    endTime = models.DateTimeField(null=True) # should be: null=False, default=timezone.now())
    description = models.CharField(max_length=1024, blank=True, null=True)
    type = models.CharField(max_length=128, null=True, choices=ACTIVITY_TYPE_CHOICES)
    subtype = models.CharField(max_length=128, null=True, choices=ACTIVITY_SUBTYPE_CHOICES)
    code = models.CharField(max_length=128, blank=True, null=True)
    parameter = models.CharField(max_length=1024, blank=True, null=True)
    docuLink = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.label
        # maybe better use self.id here??

    def getjson(self, activity_id):
        activity_dict = {'id': id, 'label': label, 'type': type, 'description': description}
        return JsonResponse(activity_dict)



@python_2_unicode_compatible
class Entity(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    label = models.CharField(max_length=128, null=True)
    type = models.CharField(max_length=128, null=True)
    location = models.CharField(max_length=128, null=True)
    access = models.CharField(max_length=128, null=True)
    size = models.CharField(max_length=128, null=True)
    format = models.CharField(max_length=128, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    docuLink = models.CharField(max_length=1024, blank=True, null=True)
    dataproduct_type = models.CharField(max_length=1024, blank=True, null=True)
    dataproduct_subtype = models.CharField(max_length=1024, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.label


# relation classes
@python_2_unicode_compatible
class Used(models.Model):
    id = models.AutoField(primary_key=True)
    activity = models.ForeignKey(Activity, null=True, on_delete=models.CASCADE)
    entity = models.ForeignKey(Entity, null=True, on_delete=models.CASCADE)
    role = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return "id=%s; activity=%s; entity=%s; desc.id=%s" % (str(self.id), self.activity, self.entity, self.description)

@python_2_unicode_compatible
class WasGeneratedBy(models.Model):
    id = models.AutoField(primary_key=True)
    entity = models.ForeignKey(Entity, null=True, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, null=True, on_delete=models.CASCADE)
    role = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return "id=%s; entity=%s; activity=%s; role=%s" % (str(self.id), self.entity, self.activity, self.role)

@python_2_unicode_compatible
class Agent(models.Model):
    id = models.CharField(primary_key=True, max_length=128)
    label = models.CharField(max_length=128, null=True) # human readable label, firstname + lastname
    type = models.CharField(max_length=128, null=True, choices=AGENT_TYPE_CHOICES) # types of entities: single entity, dataset
    description = models.CharField(max_length=1024, blank=True, null=True)
    affiliation = models.CharField(max_length=1024, blank=True, null=True)

    def __str__(self):
        return self.label

@python_2_unicode_compatible
class WasAssociatedWith(models.Model):
    id = models.AutoField(primary_key=True)
    activity = models.ForeignKey(Activity, null=True, on_delete=models.CASCADE) 
    agent = models.ForeignKey(Agent, null=True, on_delete=models.CASCADE)
    role = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "id=%s; activity=%s; agent=%s; role=%s" % (str(self.id), self.activity, self.agent, self.role)

@python_2_unicode_compatible
class WasAttributedTo(models.Model):
    id = models.AutoField(primary_key=True)
    entity = models.ForeignKey(Entity, null=True, on_delete=models.CASCADE) 
    agent = models.ForeignKey(Agent, null=True, on_delete=models.CASCADE)
    role = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "id=%s; entity=%s; agent=%s; role=%s" % (str(self.id), self.entity, self.agent, self.role)

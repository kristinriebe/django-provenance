from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
import json
from django.http import JsonResponse
from django.db.models.fields.related import ManyToManyField
from django.core import serializers
from rest_framework.renderers import JSONRenderer

from .models import Activity, ActivityDescription, Entity, EntityDescription, Used, UsedDescription, WasGeneratedBy, Agent, WasAssociatedWith, WasAttributedTo


#def index(request):
#    return HttpResponse("Hello, world. You're at the prov_vo index.")

class IndexView(generic.ListView):
    template_name = 'prov_vo/index.html'
    context_object_name = 'activity_list'

    def get_queryset(self):
        """Return the activities (at most 1000, ordered by startTime)."""
        return Activity.objects.order_by('-startTime')[:1000]

class ActivitiesView(generic.ListView):
    template_name = 'prov_vo/activities.html'
    context_object_name = 'activity_list'

    def get_queryset(self):
        """Return the activities (at most 1000, ordered by startTime)."""
        return Activity.objects.order_by('-startTime')[:1000]


class ActivityDetailView(generic.DetailView):
    model = Activity

    def get_context_data(self, **kwargs):
        context = super(ActivityDetailView, self).get_context_data(**kwargs)
        #context['used_list'] = Used.objects.all()[:]
        #context['wasGeneratedBy_list'] = WasGeneratedBy.objects.all()[:]
        #context['wasAssociatedWith_list'] = WasAssociatedWith.objects.all()[:]
        return context


class EntitiesView(generic.ListView):
    template_name = 'prov_vo/entities.html'
    context_object_name = 'entity_list'

    def get_queryset(self):
        """Return the entities (at most 1000, ordered by label)."""
        return Entity.objects.order_by('-label')[:1000]


class EntityDetailView(generic.DetailView):
    model = Entity


class EntityDescriptionsView(generic.ListView):
    template_name = 'prov_vo/entitydescriptions.html'
    context_object_name = 'entitydescription_list'

    def get_queryset(self):
        """Return the entitydescriptions (at most 1000, ordered by label)."""
        return EntityDescription.objects.order_by('-label')[:1000]


class EntityDescriptionDetailView(generic.DetailView):
    model = EntityDescription


# graphical views
def graph(request):
    return render(request, 'prov_vo/graph.html', {})


# serialisations
# simple prov-n view, using just a function:
def provn(request):
    activity_list = Activity.objects.order_by('-startTime')[:]
    entity_list = Entity.objects.order_by('-label')[:]
    agent_list = Agent.objects.order_by('-label')[:]
    used_list = Used.objects.order_by('-id')[:]
    wasGeneratedBy_list = WasGeneratedBy.objects.order_by('-id')[:]
    wasAssociatedWith_list = WasAssociatedWith.objects.order_by('-id')[:]
    wasAttributedTo_list = WasAttributedTo.objects.order_by('-id')[:]
    #return JsonResponse(activity_dict)
    #return render(request, 'provapp/activities.html', {'activity_list': activity_list})

    provstr = "document\n"
    for a in activity_list:
        provstr = provstr + "activity(" + a.id + ", " + str(a.startTime) + ", " + str(a.endTime) + ", [prov:type = '" + a.type + "', prov:label = '" + a.label + "', prov:description = '" + a.description + "']),\n"

    for e in entity_list:
        provstr = provstr + "entity(" + e.id + ", [prov:type = '" + e.type + "', prov:label = '" + e.label + "', prov:description = '" + e.description + "']),\n"

    for ag in agent_list:
        provstr = provstr + "agent(" + ag.id + ", [prov:type = '" + ag.type + "', prov:label = '" + ag.label + "', prov:description = '" + ag.description + "']),\n"

    for u in used_list:
        provstr = provstr + "used(" + u.activity.id + ", " + u.entity.id + ", [id = '" + str(u.id) + "', prov:role = '" + u.role + "']),\n"

    for wg in wasGeneratedBy_list:
        provstr = provstr + "wasGeneratedBy(" + wg.entity.id + ", " + wg.activity.id + ", [id = '" + str(wg.id) + "', prov:role = '" + wg.role + "']),\n"

    for wa in wasAssociatedWith_list:
        provstr = provstr + "wasAssociatedWith(" + wa.activity.id + ", " + wa.agent.id + ", [id = '" + str(wa.id) + "', prov:role = '" + wa.role + "']),\n"

    for wa in wasAttributedTo_list:
        provstr = provstr + "wasAttributedTo(" + wa.entity.id + ", " + wa.agent.id + ", [id = '" + str(wa.id) + "', prov:role = '" + wa.role + "']),\n"

    provstr += "endDocument"

    return HttpResponse(provstr, content_type='text/plain')

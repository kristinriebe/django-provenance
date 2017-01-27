# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
import json
from django.http import JsonResponse
from django.db.models.fields.related import ManyToManyField
from django.core import serializers
from rest_framework.renderers import JSONRenderer

from .models import Activity, ActivityDescription, Entity, EntityDescription, Used, UsedDescription, WasGeneratedBy, Agent, WasAssociatedWith, WasAttributedTo
from .models import Parameter, ParameterDescription, ActivityFlow, HadStep

# use a custom details-class that does everything the way I want it;
# uses one template for all and sets the necessary context-variables
class CustomDetailView(generic.DetailView):
    model = Entity  # shall be overwritten from inherited classes!
    
    template_name = 'core/details.html'  # this is now general enough to be used with every detail class

    def get_context_data(self, **kwargs):
        context = super(CustomDetailView, self).get_context_data(**kwargs)
        obj = get_object_or_404(self.model, id=self.kwargs['pk'])
        context['attribute_list'] = obj.get_viewattributes()
        context['classname'] = self.model.__name__
        context['descriptionpath'] = context['classname'].lower() + "descriptions"
        context['classobject'] = obj
        return context


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


class ActivityDetailView(CustomDetailView):
    model = Activity


class ActivityDetailMoreView(generic.DetailView):
    model = Activity
    template_name = 'prov_vo/activity_detailmore.html'

    def get_context_data(self, **kwargs):
        context = super(ActivityDetailMoreView, self).get_context_data(**kwargs)

        self.id = self.kwargs['pk']
        parametervalue_list = Parameter.objects.filter(activity_id=self.id)
        context['parametervalue_list'] = parametervalue_list
        return context


class ActivityDescriptionsView(generic.ListView):
    template_name = 'prov_vo/activitydescriptions.html'
    context_object_name = 'activitydescription_list'

    def get_queryset(self):
        """Return the activitydescriptions (at most 1000, ordered by label)."""
        return ActivityDescription.objects.order_by('label')[:1000]


class ActivityDescriptionDetailView(CustomDetailView):
    model = ActivityDescription


class EntitiesView(generic.ListView):
    template_name = 'prov_vo/entities.html'
    context_object_name = 'entity_list'

    def get_queryset(self):
        """Return the entities (at most 1000, ordered by label)."""
        return Entity.objects.order_by('label')[:1000]


class EntityDetailView(CustomDetailView):
    model = Entity


class EntityDescriptionsView(generic.ListView):
    template_name = 'prov_vo/entitydescriptions.html'
    context_object_name = 'entitydescription_list'

    def get_queryset(self):
        """Return the entitydescriptions (at most 1000, ordered by label)."""
        return EntityDescription.objects.order_by('label')[:1000]


class EntityDescriptionDetailView(CustomDetailView):
    model = EntityDescription


class ParametersView(generic.ListView):
    template_name = 'prov_vo/parameters.html'
    context_object_name = 'parameter_list'

    def get_queryset(self):
        """Return the parameters (at most 1000, ordered by id)."""
        return Parameter.objects.order_by('id')[:1000]


class ParameterDetailView(CustomDetailView):
    model = Parameter


class ParameterDescriptionsView(generic.ListView):
    template_name = 'prov_vo/parameterdescriptions.html'
    context_object_name = 'parameterdescription_list'

    def get_queryset(self):
        """Return the parameterdescriptions (at most 1000, ordered by label)."""
        return ParameterDescription.objects.order_by('label')[:1000]


class ParameterDescriptionDetailView(CustomDetailView):
    model = ParameterDescription


class AgentsView(generic.ListView):
    template_name = 'prov_vo/agents.html'
    context_object_name = 'agent_list'

    def get_queryset(self):
        """Return the agents (at most 1000, ordered by name)."""
        return Agent.objects.order_by('label')[:1000]


class AgentDetailView(CustomDetailView):
    model = Agent


class ActivityFlowsView(generic.ListView):
    template_name = 'prov_vo/activityflows.html'
    context_object_name = 'activityflow_list'

    def get_queryset(self):
        """Return the activityflows (at most 1000, ordered by startTime)."""
        return ActivityFlow.objects.order_by('-startTime')[:1000]


class ActivityFlowDetailView(CustomDetailView):
    model = ActivityFlow


class ActivityFlowDetailMoreView(generic.DetailView):
    model = ActivityFlow
    template_name = 'prov_vo/activityflow_detailmore.html'

    def get_context_data(self, **kwargs):
        context = super(ActivityFlowDetailMoreView, self).get_context_data(**kwargs)

        self.id = self.kwargs['pk']

        # first get all substeps:
        hadstep_list = HadStep.objects.filter(activityflow_id=self.id)
        context['hadstep_list'] = hadstep_list

        # now get all parameters for the flow (probably there will only be 
        # parameters from the subactivities!)
        parametervalue_list = Parameter.objects.filter(activity_id=self.id)
        context['parametervalue_list'] = parametervalue_list

        return context


class ActivityDescriptionsView(generic.ListView):
    template_name = 'prov_vo/activitydescriptions.html'
    context_object_name = 'activitydescription_list'

    def get_queryset(self):
        """Return the activitydescriptions (at most 1000, ordered by label)."""
        return ActivityDescription.objects.order_by('label')[:1000]



# graphical views
def graph(request):
    return render(request, 'prov_vo/graph.html', {})


# serialisations
# simple prov-n view, using just a function:
def provn(request):
    activity_list = Activity.objects.order_by('-startTime')[:]
    entity_list = Entity.objects.order_by('-label')[:]
    agent_list = Agent.objects.order_by('label')[:]
    used_list = Used.objects.order_by('-id')[:]
    wasGeneratedBy_list = WasGeneratedBy.objects.order_by('-id')[:]
    wasAssociatedWith_list = WasAssociatedWith.objects.order_by('-id')[:]
    wasAttributedTo_list = WasAttributedTo.objects.order_by('-id')[:]
    parameter_list = Parameter.objects.order_by('id')[:]

    #return JsonResponse(activity_dict)
    #return render(request, 'provapp/activities.html', {'activity_list': activity_list})

    provstr = "document\n"
    for a in activity_list:
        af = ActivityFlow.objects.filter(id=a.id)
        if (af):
            provstr = provstr + "activity(" + a.id + ", " + str(a.startTime) + ", " + str(a.endTime) + ", [prov:label = '" + a.label + "', voprov:annotation = '" + a.annotation + "', voprov:doculink = '" + a.doculink + "', voprov:type = '" + a.description.type + "', voprov:subtype = '" + a.description.subtype + "',  voprov:description_docu = '" + a.description.doculink + "',  voprov:activityflow = '1'" + a.description.doculink + "']),\n" #  voprov:viewLevel = '" + a.viewLevel + "']),\n"
        else:
            provstr = provstr + "activity(" + a.id + ", " + str(a.startTime) + ", " + str(a.endTime) + ", [prov:label = '" + a.label + "', voprov:annotation = '" + a.annotation + "', voprov:doculink = '" + a.doculink + "', voprov:type = '" + a.description.type + "', voprov:subtype = '" + a.description.subtype + "',  voprov:description_docu = '" + a.description.doculink + "']),\n"
    for e in entity_list:
        provstr = provstr + "entity(" + e.id + ", [prov:type = '" + e.type + "', prov:label = '" + e.label + "', voprov:annotation = '" + e.annotation + "', voprov:dataproduct_type = '" + e.description.dataproduct_type + "', voprov:dataproduct_subtype = '" + e.description.dataproduct_subtype + "']),\n"
 
    for ag in agent_list:
        provstr = provstr + "agent(" + ag.id + ", [prov:type = '" + ag.type + "', voprov:name = '" + ag.label + "', voprov:affiliation = '" + ag.affiliation + "']),\n"

    for u in used_list:
        provstr = provstr + "used(" + u.activity.id + ", " + u.entity.id + ", [prov:role = '" + u.description.role + "']),\n"

    for wg in wasGeneratedBy_list:
        provstr = provstr + "wasGeneratedBy(" + wg.entity.id + ", " + wg.activity.id + ", [prov:role = '" + wg.description.role + "']),\n"

    for wa in wasAssociatedWith_list:
        provstr = provstr + "wasAssociatedWith(" + wa.activity.id + ", " + wa.agent.id + ", [prov:role = '" + wa.role + "']),\n"

    for wa in wasAttributedTo_list:
        provstr = provstr + "wasAttributedTo(" + wa.entity.id + ", " + wa.agent.id + ", [prov:role = '" + wa.role + "']),\n"

    for p in parameter_list:
        provstr = provstr + "entity(" + str(p.id) + ", [prov:type = 'parameter', prov:label = '" + p.description.label + "', prov:value = '" + str(p.value) + "', voprov:datatype = '" + str(p.description.datatype) + "', voprov:unit = '" + str(p.description.unit) + "', voprov:ucd = '" + str(p.description.ucd) + "', voprov:utype = '" + str(p.description.utype) + "', voprov:arraysize = '" + str(p.description.arraysize) + "', voprov:annotation = '" + str(p.description.annotation) + "']),\n"

    provstr += "endDocument"

    return HttpResponse(provstr, content_type='text/plain')


def json_view(request):
    activity_list = Activity.objects.order_by('label')[:]
    entity_list = Entity.objects.order_by('label')[:]
    agent_list = Agent.objects.order_by('label')[:]

    adict = {}
    for a in activity_list:
        adict.update(a.get_json())

    edict = {}
    for e in entity_list:
        edict.update(e.get_json())

    agdict = {}
    for ag in agent_list:
        agdict.update(ag.get_json())

    allobjects = {
        "activity": adict,
        "entity": edict,
        "agent": agdict
    }

    json_str = json.dumps(allobjects,
                sort_keys=True,
                indent=4
               )

    return HttpResponse(json_str, content_type='text/plain')

    # JsonResponse
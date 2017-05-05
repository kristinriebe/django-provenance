# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.generic.edit import FormView
import json
from django.http import JsonResponse
from django.db.models.fields.related import ManyToManyField
from django.core import serializers
from rest_framework.renderers import JSONRenderer

from .models import Activity, ActivityDescription, Entity, EntityDescription, Used, UsedDescription, WasGeneratedBy, Agent, WasAssociatedWith, WasAttributedTo
from .models import Parameter, ParameterDescription, ActivityFlow, HadStep, WasDerivedFrom

from .forms import DatasetForm
import sys

reload(sys)
sys.setdefaultencoding('utf8')

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


# form  view
class DatasetFormResultsView(FormView):
    template_name = 'prov_vo/dataset_form.html'
    form_class = DatasetForm

    def form_valid(self, form):
        project_id = form.cleaned_data['project']
        activitydescription_type = form.cleaned_data['activitydescription_type']
        activitydescription_id = form.cleaned_data['activitydescription']

        if project_id == 'any':
            activity_list = Activity.objects.all()
        else:
            # in Provenance, project is rather an agent connected with the entities or the activities, thus combine both:
            activity_list = Activity.objects.filter(wasassociatedwith__agent_id=project_id) | Activity.objects.filter(wasgeneratedby__entity__wasattributedto__agent_id=project_id)
            print activity_list


        if activitydescription_type != 'any':
            activity_list = activity_list.filter(description__type=activitydescription_type)

        # get all possible parameters for the experiments/protocols and check if they were checked in the form or not
        parameters = ParameterDescription.objects.filter(activitydescription=activitydescription_id)
        parametervalues = {}
        for i, p in enumerate(parameters):
            parameter_cleaned = form.cleaned_data['param_'+p.id]
            # print "p: ", p.id
            # print "parameter clean: ", parameter_cleaned
            if parameter_cleaned:
                value_min = -1
                value_max = -1
                value_sin = -1
                if 'paramvalue_min_'+p.id in form.cleaned_data:
                    value_min = form.cleaned_data['paramvalue_min_'+p.id]
                if 'paramvalue_max_'+p.id in form.cleaned_data:
                    value_max = form.cleaned_data['paramvalue_max_'+p.id]
                if 'paramvalue_sin_'+p.id in form.cleaned_data:
                    value_sin = form.cleaned_data['paramvalue_sin_'+p.id]

                parametervalues[p.id] = [value_min, value_max, value_sin]
                #print 'cleaned val: ', p.id, value_min, value_max, value_sin

        if activitydescription_id != 'any':
            activity_list = activity_list.filter(description=activitydescription_id)

            # restrict activity_list based on chosen parameters:
            parameter_activity_ids = []
            for p, values in parametervalues.iteritems():

                # find the experiment ids fitting to the parameter value;
                # need to cast the value to int or float, depending on the datatype
                # (otherwise cannot do >, < or range queries)
                parameter = ParameterDescription.objects.get(id=p)
                datatype = parameter.datatype
                minval = values[0]
                maxval = values[1]
                sinval = values[2]

                if datatype == 'int':
                    activity_list = activity_list.filter(parameter__description_id=p, parameter__value__int__range=(minval,maxval))
                elif datatype == 'float':
                    activity_list = activity_list.filter(parameter__description_id=p, parameter__value__float__range=(minval,maxval))
                else:
                    activity_list = activity_list.filter(parameter__description_id=p, parameter__value=sinval)
                #print activity_list.query

        dataset_list = []
        agent_list = {}
        activities = {}
        parametervalue_lists = {}
        for a in activity_list:
            elist = Entity.objects.filter(wasgeneratedby__activity_id=a.id)
            for e in elist:
                dataset_list.append(e)
                # print "id: ", e
                parametervalue_lists[str(e.id)] = Parameter.objects.filter(activity_id=a.id)

        # TODO: create a custom list of datasets, with agents, activities and -descriptions already included as
        # direct attributes. (Avoid many reverse lookups in the template!)
        return render_to_response('prov_vo/dataset_formresults.html', context={'dataset_list': dataset_list, 'parametervalue_lists': parametervalue_lists})


def get_activitydescriptions(request):  # url: datasetform_activitydescriptions
    # Get all available protocols for a given protocol_type,
    # will be used by javascript to fill the parameters automatically into the dataset search form

    activitydescription_type = request.GET.get('activitydescription_type')
    #print 'actdesctype: ', activitydescription_type
    actdesc_list = []
    if activitydescription_type:
        if activitydescription_type == 'any':
            # again load all possible parameters, not sure, how to do without:
            for p in ActivityDescription.objects.all():
                actdesc_list.append(dict(id=p.id, value=unicode(p.label)))
        else:
            for p in ActivityDescription.objects.filter(type=activitydescription_type):
                actdesc_list.append(dict(id=p.id, value=unicode(p.label)))

    return HttpResponse(json.dumps(actdesc_list), content_type='application/json')


def get_parameters(request):  # url: datasetform_parameters
    # Get all available parameters for a given protocol_id,
    # will be used by javascript to fill the parameters automatically into the dataset search form

    activitydescription_id = request.GET.get('activitydescription')
    #print 'id: ', activitydescription_id
    a  = ParameterDescription.objects.filter(activitydescription=activitydescription_id)
    #print a.query
    #print a
    #print "parent: ", protocol
    parameter_list = []
    if activitydescription_id:
        if activitydescription_id == 'any':
            # do load nothing in this case
            parameter_list = []
            #for param in InputParameter.objects.all():
            #    parameter_list.append(dict(id=param.id, value=unicode(param.name)))
        else:
            for param in ParameterDescription.objects.filter(activitydescription=activitydescription_id):
                parameter_list.append(dict(id=param.id, value=unicode(param.label)))

        # whatever happens, add option 'any' as well -- not really needed
        # ret.insert(0, dict(id='', value='any'))

    return HttpResponse(json.dumps(parameter_list), content_type='application/json')



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
            provstr = provstr + "activity(" + a.id + ", " + str(a.startTime) + ", " + str(a.endTime) + ", [voprov:label = '" + str(a.label) + "', voprov:annotation = '" + str(a.annotation) + "', voprov:doculink = '" + str(a.doculink) + "', voprov:type = '" + str(a.description.type) + "', voprov:subtype = '" + str(a.description.subtype) + "',  voprov:desc_doculink = '" + str(a.description.doculink) + "',  voprov:activityflow = '1']),\n" #  voprov:viewLevel = '" + a.viewLevel + "']),\n"
        else:
            provstr = provstr + "activity(" + a.id + ", " + str(a.startTime) + ", " + str(a.endTime) + ", [voprov:label = '" + str(a.label) + "', voprov:annotation = '" + str(a.annotation) + "', voprov:doculink = '" + str(a.doculink) + "', voprov:type = '" + str(a.description.type) + "', voprov:subtype = '" + str(a.description.subtype) + "',  voprov:desc_doculink = '" + str(a.description.doculink) + "']),\n"
    for e in entity_list:
        provstr = provstr + "entity(" + e.id + ", [voprov:type = '" + str(e.type) + "', voprov:label = '" + str(e.label) + "', voprov:annotation = '" + str(e.annotation) + "', voprov:desc_dataproduct_type = '" + str(e.description.dataproduct_type) + "', voprov:desc_dataproduct_subtype = '" + str(e.description.dataproduct_subtype) + "']),\n"

    for ag in agent_list:
        provstr = provstr + "agent(" + ag.id + ", [voprov:type = '" + str(ag.type) + "', voprov:name = '" + str(ag.label) + "', voprov:affiliation = '" + str(ag.affiliation) + "']),\n"

    for u in used_list:
        provstr = provstr + "used(" + u.activity.id + ", " + u.entity.id + ", [voprov:role = '" + str(u.description.role) + "']),\n"

    for wg in wasGeneratedBy_list:
        provstr = provstr + "wasGeneratedBy(" + wg.entity.id + ", " + wg.activity.id + ", [voprov:role = '" + str(wg.description.role) + "']),\n"

    for wa in wasAssociatedWith_list:
        provstr = provstr + "wasAssociatedWith(" + wa.activity.id + ", " + wa.agent.id + ", [voprov:role = '" + str(wa.role) + "']),\n"

    for wa in wasAttributedTo_list:
        provstr = provstr + "wasAttributedTo(" + wa.entity.id + ", " + wa.agent.id + ", [voprov:role = '" + str(wa.role) + "']),\n"

    for p in parameter_list:
        provstr = provstr + "entity(" + str(p.id)+ ", [voprov:type = 'parameter', voprov:label = '" + str(p.description.label) + "', voprov:value = '" + str(p.value) + "', voprov:datatype = '" + str(p.description.datatype) + "', voprov:unit = '" + str(p.description.unit) + "', voprov:ucd = '" + str(p.description.ucd) + "', voprov:utype = '" + str(p.description.utype) + "', voprov:arraysize = '" + str(p.description.arraysize) + "', voprov:annotation = '" + str(p.description.annotation) + "']),\n"

    provstr += "endDocument"

    return HttpResponse(provstr, content_type='text/plain')


def json_view(request):
    activity_list = Activity.objects.all()
    entity_list = Entity.objects.all()
    agent_list = Agent.objects.all()
    used_list = Used.objects.all()
    wasgeneratedby_list = WasGeneratedBy.objects.all()
    wasattributedto_list = WasAttributedTo.objects.all()
    wasassociatedwith_list = WasAssociatedWith.objects.all()
    wasderivedfrom_list = WasDerivedFrom.objects.all()



    adict = {}
    for a in activity_list:
        adict.update(a.get_json())

    edict = {}
    for e in entity_list:
        edict.update(e.get_json())

    agdict = {}
    for ag in agent_list:
        agdict.update(ag.get_json())

    udict = {}
    for u in used_list:
        udict.update(u.get_json())

    wgdict = {}
    for wg in wasgeneratedby_list:
        wgdict.update(wg.get_json())

    watdict = {}
    for wat in wasattributedto_list:
        watdict.update(wat.get_json())

    wasdict = {}
    for was in wasassociatedwith_list:
        wasdict.update(was.get_json())

    wddict = {}
    for wd in wasderivedfrom_list:
        wddict.update(wd.get_json())


    allobjects = {
        "activity": adict,
        "entity": edict,
        "agent": agdict,
        "used": udict,
        "wasGeneratedBy": wgdict,
        "wasAttributedTo": watdict,
        "wasAssociatedWith": wasdict,
        "wasDerivedFrom": wddict
    }

    json_str = json.dumps(allobjects,
                sort_keys=True,
                indent=4
               )

    return HttpResponse(json_str, content_type='text/plain')

    # JsonResponse
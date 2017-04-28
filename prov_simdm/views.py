# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.http import JsonResponse
from django.db.models.fields.related import ManyToManyField
from django.core import serializers
from django.views.generic.edit import FormView
from django.db.models import F  # for renaming fields extracted from database

from rest_framework.renderers import JSONRenderer
from django.db.models.fields import Field
from django.db.models import Transform

import json


from .models import Experiment, Protocol, InputParameter, ParameterSetting, Algorithm, AppliedAlgorithm, Project, OutputDataset, Party, Contact, InputDataset
from core.models import TAP_SCHEMA_tables, TAP_SCHEMA_columns, VOResource_Capability, VOResource_Interface, VOResource_AccessURL

from .forms import AlgorithmForm, DatasetForm
from .serializers import ProtocolSerializer
from .renderers import VOTableRenderer, VosiTablesRenderer, VosiTableRenderer, VosiAvailabilityRenderer, VosiCapabilityRenderer


class CustomDetailView(generic.DetailView):
    model = Experiment  # shall be overwritten from inherited classes!

    template_name = 'prov_simdm/details.html'  # this is now general enough to be used with every detail class
    link_dict = {}

    def get_context_data(self, **kwargs):
        context = super(CustomDetailView, self).get_context_data(**kwargs)
        obj = get_object_or_404(self.model, id=self.kwargs['pk'])
        context['attribute_list'] = obj.get_viewattributes()
        context['link_dict'] = self.link_dict
        context['classname'] = self.model.__name__
        #context['linkpath'] = context['classname'].lower() + "descriptions"
        context['classobject'] = obj
        return context


class IndexView(generic.ListView):
    template_name = 'prov_simdm/index.html'
    context_object_name = ""
    queryset = ""

    #def get_queryset(self):
    #    """Return"""
    #    return


class ExperimentsView(generic.ListView):
    template_name = 'prov_simdm/experiments.html'
    context_object_name = 'experiment_list'

    def get_queryset(self):
        """Return the experiments (at most 1000, ordered by time)."""
        return Experiment.objects.order_by('-executionTime')[:1000]

class ExperimentDetailView(CustomDetailView):
    model = Experiment
    link_dict = {'protocol': 'protocols'}

class ExperimentMoreDetailView(generic.DetailView):
    model = Experiment
    template_name = 'prov_simdm/experiment_moredetail.html'

    def get_context_data(self, **kwargs):
        context = super(ExperimentMoreDetailView, self).get_context_data(**kwargs)

        self.id = self.kwargs['pk']
        parametervalue_list = ParameterSetting.objects.filter(experiment_id=str(self.id))
        context['parametervalue_list'] = parametervalue_list
        return context


class ProtocolsView(generic.ListView):
    template_name = 'prov_simdm/protocols.html'
    context_object_name = 'protocol_list'

    def get_queryset(self):
        """Return the protocols (at most 1000)."""
        return Protocol.objects.order_by('id')[:1000]

class ProtocolDetailView(CustomDetailView):
    model = Protocol
    # contains: input-/ouput-dataobjecttype


class InputParametersView(generic.ListView):
    template_name = 'prov_simdm/inputparameters.html'
    context_object_name = 'inputparameter_list'

    def get_queryset(self):
        """Return the input parameters (at most 1000)."""
        return InputParameter.objects.order_by('id')[:1000]

class InputParameterDetailView(CustomDetailView):
    model = InputParameter
    link_dict = {'protocol': 'protocols'}


class ParameterSettingsView(generic.ListView):
    template_name = 'prov_simdm/parametersettings.html'
    context_object_name = 'parametersetting_list'

    def get_queryset(self):
        """Return the parameter settings (values) (at most 1000)."""
        return ParameterSetting.objects.order_by('id')[:1000]

class ParameterSettingDetailView(CustomDetailView):
    model = ParameterSetting
    link_dict = {'inputParameter': 'inputparameters', 'experiment': 'experiments'}


class AlgorithmsView(generic.ListView):
    template_name = 'prov_simdm/algorithms.html'
    context_object_name = 'algorithm_list'

    def get_queryset(self):
        return Algorithm.objects.order_by('id')[:1000]

class AlgorithmDetailView(CustomDetailView):
    model = Algorithm
    link_dict = {'protocol': 'protocols'}


# Form views
class AlgorithmFormResultsView(FormView):
    template_name = 'prov_simdm/algorithm_form.html'
    form_class = AlgorithmForm

    def form_valid(self, form):
        algorithm_id = form.cleaned_data['algorithm_id']
        algorithm = Algorithm.objects.get(id=algorithm_id)

        applied_set = AppliedAlgorithm.objects.filter(algorithm_id = algorithm.id)
        experiment_list = [Experiment.objects.get(id=a.experiment_id) for a in applied_set]

        for e in experiment_list:
            parametervalue_list = ParameterSetting.objects.filter(experiment_id=str(e.id))
            e.parametervalue_list = parametervalue_list

        return render_to_response('prov_simdm/algorithm_formresults.html', context={'algorithm': algorithm, 'experiment_list': experiment_list})

# helper classes for converting char fields from the database
# see http://stackoverflow.com/questions/28101580/how-do-i-cast-char-to-integer-while-querying-in-django-orm
# and https://docs.djangoproject.com/en/1.10/howto/custom-lookups/#custom-lookups
@Field.register_lookup
class IntegerValue(Transform):
    # Register this before you filter things, for example in models.py
    lookup_name = 'int'  # Used as object.filter(LeftField__int__gte, "777")
    bilateral = True  # To cast both left and right

    def as_sql(self, compiler, connection):
        sql, params = compiler.compile(self.lhs)
        sql = 'CAST(%s AS INTEGER)' % sql
        return sql, params

@Field.register_lookup
class FloatValue(Transform):
    # Register this before you filter things, for example in models.py
    lookup_name = 'float'  # Used as object.filter(LeftField__float__gte, "1.77")
    bilateral = True  # To cast both left and right

    def as_sql(self, compiler, connection):
        sql, params = compiler.compile(self.lhs)
        sql = 'CAST(%s AS FLOAT)' % sql
        return sql, params


class DatasetFormResultsView(FormView):
    template_name = 'prov_simdm/dataset_form.html'
    form_class = DatasetForm

    def form_valid(self, form):
        project_id = form.cleaned_data['project_id']
        protocol_type = form.cleaned_data['protocol_type']
        protocol = form.cleaned_data['protocol']

        if project_id == 'any':
            experiment_list = Experiment.objects.all()
        else:
            experiment_list = Experiment.objects.filter(project_id=project_id)

        if protocol_type != 'any':
            experiment_list = experiment_list.filter(protocol__type=protocol_type)

        # get all possible parameters for the experiments/protocols and check if they were checked in the form or not
        parameters = InputParameter.objects.filter(protocol=protocol)
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
                print 'cleaned val: ', p.id, value_min, value_max, value_sin

        if protocol != 'any':
            experiment_list = experiment_list.filter(protocol=protocol)

            # restrict experiment_list based on chosen parameters:
            parameter_experiment_ids = []
            for p, values in parametervalues.iteritems():

                # find the experiment ids fitting to the parameter value;
                # need to cast the value to int or float, depending on the datatype
                # (otherwise cannot do >, < or range queries)
                parameter = InputParameter.objects.get(id=p)
                datatype = parameter.datatype
                minval = values[0]
                maxval = values[1]
                sinval = values[2]

                if datatype == 'int':
                    experiment_list = experiment_list.filter(parametersetting__inputParameter_id=p, parametersetting__value__int__range=(minval,maxval))
                elif datatype == 'float':
                    experiment_list = experiment_list.filter(parametersetting__inputParameter_id=p, parametersetting__value__float__range=(minval,maxval))
                else:
                    experiment_list = experiment_list.filter(parametersetting__inputParameter_id=p, parametersetting__value=sinval)

                print experiment_list.query

        dataset_list = []
        parametervalue_lists = {}
        for e in experiment_list:
            olist = OutputDataset.objects.filter(experiment_id=e.id)
            for o in olist:
                dataset_list.append(o)
                print "id: ", o
                parametervalue_lists[str(o.id)] = ParameterSetting.objects.filter(experiment_id=e.id)
                #parametervalue_lists['yes'] = ParameterSetting.objects.filter(experiment_id=e.id)

        return render_to_response('prov_simdm/dataset_formresults.html', context={'dataset_list': dataset_list, 'parametervalue_lists': parametervalue_lists})


def get_protocols(request):  # url: datasetform_protocols
    # Get all available protocols for a given protocol_type,
    # will be used by javascript to fill the parameters automatically into the dataset search form

    protocol_type = request.GET.get('protocol_type')
    protocol_list = []
    if protocol_type:
        if protocol_type == 'any':
            # again load all possible parameters, not sure, how to do without:
            for p in Protocol.objects.all():
                protocol_list.append(dict(id=p.id, value=unicode(p.name)))
        else:
            for p in Protocol.objects.filter(type=protocol_type):
                protocol_list.append(dict(id=p.id, value=unicode(p.name)))

    return HttpResponse(json.dumps(protocol_list), content_type='application/json')


def get_parameters(request):  # url: datasetform_parameters
    # Get all available parameters for a given protocol_id,
    # will be used by javascript to fill the parameters automatically into the dataset search form

    protocol = request.GET.get('protocol')
    #print "parent: ", protocol
    parameter_list = []
    if protocol:
        if protocol == 'any':
            # do load nothing in this case
            parameter_list = []
            #for param in InputParameter.objects.all():
            #    parameter_list.append(dict(id=param.id, value=unicode(param.name)))
        else:
            for param in InputParameter.objects.filter(protocol__id=protocol):
                parameter_list.append(dict(id=param.id, value=unicode(param.name)))

        # whatever happens, add option 'any' as well -- not really needed
        # ret.insert(0, dict(id='', value='any'))

    return HttpResponse(json.dumps(parameter_list), content_type='application/json')


# ProvenanceDM views of simulation data
# =====================================

def voprov_entities(request):
    # get datasets and rename fields from database, so they fit to provenancedm-attributes of Entity
    data = OutputDataset.objects.order_by('id').annotate(
            location=F('accessURL'),
            type=F('objectType_id'),
            label=F('name')
           ).values('id','label','type','location')

    tabledescription = "ProvenanceDM list of entitites, extracted from SimDM"
    tableattrs = {'utype': 'prov:Entity'}
    utypes = {}
    utypes['type'] = 'voprov:type'
    utypes['id'] = 'prov:id'
    utypes['label'] = 'prov:label'

    fields = []
    for fieldname in utypes.keys():
        fields.append(
                {'FIELD': {
                    'attrs': {'name': fieldname, 'utype': utypes[fieldname]}
                    }
                }
        )

    votable_meta = {
                    'VOTABLE': {
                        'RESOURCE': {
                            #'attrs': {'type': 'results'},
                            'TABLE': {
                                'attrs': tableattrs,
                                'DESCRIPTION': tabledescription,
                                'FIELDS': fields,
                            }
                        }
                    }
                }

    # ... then render as xml VOTable using VOTableRenderer,
    # (missing field definitions will be added automatically)
    votable = VOTableRenderer().render(data, votable_meta=votable_meta, prettyprint=False)
    response = HttpResponse(votable, content_type="application/xml")
    return response

def voprov_activities(request):
    # get datasets and rename fields from database, so they fit to provenancedm-attributes of Entity
    data = Experiment.objects.order_by('id').annotate(
            label=F('name'),
            endTime=F('executionTime'),
            annotation=F('description'),
            description_ref=F('protocol_id')
           ).values('id','label','endTime','description_ref','annotation')

    votable = VOTableRenderer().render(data, prettyprint=False)
    response = HttpResponse(votable, content_type="application/xml")
    return response

def voprov_activitydescriptions(request):
    # get datasets and rename fields from database, so they fit to provenancedm-attributes of Entity
    data = Protocol.objects.order_by('id').annotate(
            label=F('name'),
            #type=F('ptype'),
            annotation=F('description'),
            doculink=F('referenceURL')
           ).values('id','label','type','annotation','doculink')

    votable = VOTableRenderer().render(data, prettyprint=False)
    response = HttpResponse(votable, content_type="application/xml")
    return response

def voprov_provn(request):
    experiments = Experiment.objects.order_by('id')#.annotate(
#            label=F('name'),
#            endTime=F('executionTime'),
#            annotation=F('description'),
#            description_ref=F('protocol_id')
#           ).values('id','label','endTime','description_ref','annotation')

    outputdatasets = OutputDataset.objects.order_by('id')#.annotate(
#            label=F('name'),
#            activity=F('experiment'),
#           ).values('id','label','activity')

    inputdatasets = InputDataset.objects.order_by('id')#.annotate(
#            label=F('name'),
#            activity=F('experiment'),
#            product=F('product'),
#           ).values('id','label','activity', 'product')
    parties = Party.objects.order_by('id')
    projects = Project.objects.order_by('id')
    contacts = Contact.objects.order_by('id')
    parametersettings = ParameterSetting.objects.order_by('id')

    # TODO: also construct wasDerivedFrom relations

    provstr = "document\n"
    for e in experiments:
        provstr = provstr + "activity(" + e.id + ", "", " + str(e.executionTime) + ", [prov:label = '" + e.name + "', voprov:annotation = '" + str(e.description) + "', voprov:type = '" + str(e.protocol.type) + "']),\n"

    for o in outputdatasets:
        # TODO: inputdatasets that are not refering to an outputdataset are still missing
        provstr = provstr + "entity(" + o.id + ", [prov:type = 'entity', prov:label = '" + o.name + "', voprov:accessLink = '" + str(o.accessURL) + "', voprov:dataproduct_type = '" + str(o.objectType.name) + "']),\n"

    for ag in parties:
        agtype = 'Person' # or can it be something else as well?
        provstr = provstr + "agent(" + ag.id + ", [prov:type = '" + agtype + "', voprov:name = '" + ag.name + "', voprov:affiliation = '" + ag.affiliation + "']),\n"

    for ag in projects:
        agtype = 'Project' # or can it be something else as well?
        provstr = provstr + "agent(" + ag.id + ", [prov:type = '" + agtype + "', voprov:name = '" + ag.name + "', voprov:link = '" + ag.referenceURL + "']),\n"

    for u in inputdatasets:
        provstr = provstr + "used(" + u.experiment.id + ", " + u.id + ", [prov:role = '" + u.description + "']),\n"

    for wg in outputdatasets:
        # no role in SimDM for outputs?
        wgrole = "result"
        provstr = provstr + "wasGeneratedBy(" + wg.id + ", " + wg.experiment.id + ", [prov:role = '" + wgrole + "']),\n"

    for wa in contacts:
        provstr = provstr + "wasAssociatedWith(" + wa.experiment.id + ", " + wa.party.id + ", [prov:role = '" + wa.role + "']),\n"

    for wa in outputdatasets:
        provstr = provstr + "wasAttributedTo(" + wa.id + ", " + wa.experiment.project.id + "),\n"

    for p in parametersettings:
        provstr = provstr + "entity(" + str(p.id) + ", [prov:type = 'parameter', prov:label = '" + p.inputParameter.name + "', prov:value = '" + str(p.value) + "', voprov:datatype = '" + str(p.inputParameter.datatype) + "', voprov:unit = '" + str(p.inputParameter.unit) + "']),\n"  #, voprov:ucd = '" + str(p.description.ucd) + "', voprov:utype = '" + str(p.description.utype) + "', voprov:arraysize = '" + str(p.description.arraysize) + "', voprov:annotation = '" + str(p.description.annotation) + "']),\n"

    provstr += "endDocument"

    return HttpResponse(provstr, content_type='text/plain')


# SimDAL views
# ============

# SimDAL Repository
#class Projects(generic.ListView):
#    template_name = 'prov_simdm/projects.html'
#    context_object_name = 'project_list'
#
#    def get_queryset(self):
#        projects = Project.objects.order_by('id')
#        # TODO: convert to xml representation
#        return projects

def simdal_projects(request):
    projects = Project.objects.order_by('id')
    data = projects.values()
    votable = VOTableRenderer().render(data, prettyprint=False)
    response = HttpResponse(votable, content_type="application/xml")
    return response


def simdal_protocols(request):
    protocols = Protocol.objects.order_by('id')

    # test serializers:
    data = serializers.serialize('xml', protocols) #, fields=('name','')) # => works

    # use custom serializer:
    serializer = ProtocolSerializer(protocols, many=True)
    data = serializer.data
    # xmlns:simdm="http://www.ivoa.net/documents/SimDM"

    # generate a VOTable, with one resource and one table only
    # first construct a simple dictionary ...
    data = protocols.values()

    # -- optional additional metadata
    tabledescription = "SimDAL list of protocols"
    tableattrs = {'utype': 'SimDM:/resource/protocol/Protocol'}
    fields = [
                {'FIELD': {
                    'attrs': {'name': 'code', 'utype': 'SimDM:/resource/protocol/Protocol.code'},
                    'DESCRIPTION': 'url for source code or code description'
                    }
                }
            ]

    votable_meta = {
                    'VOTABLE': {
                        'RESOURCE': {
                            #'attrs': {'type': 'results'},
                            'TABLE': {
                                'attrs': tableattrs,
                                'DESCRIPTION': tabledescription,
                                'FIELDS': fields,
                            }
                        }
                    }
                }

    # ... then render as xml VOTable using VOTableRenderer,
    # (missing field definitions will be added automatically)
    votable = VOTableRenderer().render(data, votable_meta=votable_meta, prettyprint=False)
    #votable = VOTableRenderer().render(data, prettyprint=False)

    response = HttpResponse(votable, content_type="application/xml")
    #response = HttpResponse(votable, content_type="text/plain")

    # could also easily render serialized data into json:
    #json = JSONRenderer().render(protocols.values())
    #response = HttpResponse(json, content_type='application/json')

    return response


# SimDAL Search
def simdal_experiments(request):
    data = Experiment.objects.order_by('id').values()
    votable = VOTableRenderer().render(data, prettyprint=False)
    response = HttpResponse(votable, content_type="application/xml")
    return response


# SimDAL Data Access
#class Datasets(generic.ListView):
#    template_name = 'prov_simdm/datasets.html'
#    context_object_name = 'dataset_list'
#
#    def get_queryset(self):
#        datasets = OutputDataset.objects.order_by('id')
#        # TODO: convert to xml representation
#        return datasets

def simdal_datasets(request):
    data = TAP_SCHEMA_Tables.objects.order_by('id').values()
    votable = VOTableRenderer().render(data, prettyprint=False)
    response = HttpResponse(votable, content_type="application/xml")
    return response


def simdal_vositables(request):
    # This uses the TAP_SCHEMA_tables for listing all tables.
    data = TAP_SCHEMA_tables.objects.order_by('schema_name').order_by('table_name').values()

    # first try: just render as a votable:
    votable = VOTableRenderer().render(data, prettyprint=False)
    response = HttpResponse(votable, content_type="application/xml")

    # return XML using the VOSI standard defined at
    # http://www.ivoa.net/documents/VOSI/20161214/PR-VOSI-1.1-20161214.pdf
    vositables = VosiTablesRenderer().render(data)
    response = HttpResponse(vositables, content_type="application/xml")

    return response


def simdal_vositabledetails(request, table_name):
    table = TAP_SCHEMA_columns.objects.filter(table_name=table_name).order_by('sortid').order_by('column_name').values()
    print 'table_name, table: ', table_name, table

    data = table
    print "data: ", data
    vositable = VosiTableRenderer().render(data)
    response = HttpResponse(vositable, content_type="application/xml")
    return response

def simdal_vosiavailability(request):
    # should perform checks, if databases are still reachable etc.

    data = {'available': 'true', 'note': 'service is ready for queries'}
    vosiavailability = VosiAvailabilityRenderer().render(data)
    response = HttpResponse(vosiavailability, content_type="application/xml")
    return response

def simdal_vosicapability(request):

    capabilities = VOResource_Capability.objects.order_by('id')
#    interfaces = VOResource_Interface.objects.order_by('id')
#    accessurls = VOResource_AccessURL.objects.order_by('id')

    # now join them together
#    for capability in capabilities:
#
#        interfaces = VOResource_Interface.objects.filter('capability='+capability.id)
#        for interface in interfaces:
#            accessurls = VOResource_AccessURL.objects.filter('interface='+interface.id)

    #data = {'available': 'true', 'note': 'service is ready for queries'}
    #data = capabilities
    vosicap = VosiCapabilityRenderer().render(capabilities)
    # response = HttpResponse(vosicap, content_type="text/xml")
    response = HttpResponse(vosicap, content_type="application/xml")
    return response

# def get_capabilities(qs):
#     capability = []
#     interfaces = VOResource_Interface.objects.filter(capability=qs)

#     capability += interfaces
#     if interfaces:
#         interim_cap_qs = get_capabilities(interfaces)
#         for qs in interim_cap_qs:
#             capability.append(qs)
#     else:
#         capability = [qs]

#     return capability

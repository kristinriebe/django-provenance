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

import json


from .models import Experiment, Protocol, InputParameter, ParameterSetting, Algorithm, AppliedAlgorithm, Project, OutputDataset
from .forms import AlgorithmForm, DatasetForm
from .serializers import ProtocolSerializer
from .renderers import VOTableRenderer


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


class DatasetFormResultsView(FormView):
    template_name = 'prov_simdm/dataset_form.html'
    form_class = DatasetForm

    def form_valid(self, form):
        project_id = form.cleaned_data['project_id']
        protocol_type = form.cleaned_data['protocol_type']
        #parameters = form.cleaned_data['parameters']

        if project_id == 'any':
            experiment_list = Experiment.objects.all()
        else:
            experiment_list = Experiment.objects.filter(project_id=project_id)

        if protocol_type != 'any':
            experiment_list = experiment_list.filter(protocol__type=protocol_type)

        # restrict experiment_list based on chosen parameters:
        #if parameters:
        #    print parameters
            #experiment_list = experiment_list.filter(inputParameter_protocol=experiment_protocolprotocol_type)

        dataset_list = []
        for e in experiment_list:
            olist = OutputDataset.objects.filter(experiment_id=e.id)
            for o in olist:
                dataset_list.append(o)

        return render_to_response('prov_simdm/dataset_formresults.html', context={'dataset_list': dataset_list})


def get_protocols(request): # url: datasetform_protocols
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


def get_parameters(request): # url: datasetform_parameters
    # Get all available parameters for a given protocol_id,
    # will be used by javascript to fill the parameters automatically into the dataset search form

    protocol = request.GET.get('protocol')
    #print "parent: ", protocol
    parameter_list = []
    if protocol:
        if protocol == 'any':
            # again load all possible parameters, not sure, how to do without:
            for param in InputParameter.objects.all():
                parameter_list.append(dict(id=param.id, value=unicode(param.name)))
        else:
            for param in InputParameter.objects.filter(protocol__id=protocol):
                parameter_list.append(dict(id=param.id, value=unicode(param.name)))

        # whatever happens, add option 'any' as well -- not really needed
        # ret.insert(0, dict(id='', value='any'))

    return HttpResponse(json.dumps(parameter_list), content_type='application/json')


# ProvenanceDM views
# ==================

def voprov_entities(request):
    # get datasets and rename fields from database, so they fit to provenancedm-attributes of Entity
    data = OutputDataset.objects.order_by('id').annotate(location=F('accessURL'), type=F('objectType_id')).values('id','name','type','location')
    votable = VOTableRenderer().render(data, prettyprint=False)
    response = HttpResponse(votable, content_type="application/xml")
    return response


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
                    'attrs': {'name': 'code'},
                    'DESCRIPTION': 'url for source code or code description'
                    }
                }
            ]

    votable_meta = {
                    'VOTABLE': {
                        'RESOURCE': {
                            'attrs': {'type': 'results'},
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
    data = OutputDataset.objects.order_by('id').values()
    votable = VOTableRenderer().render(data, prettyprint=False)
    response = HttpResponse(votable, content_type="application/xml")
    return response

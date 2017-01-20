# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
import json
from django.http import JsonResponse
from django.db.models.fields.related import ManyToManyField
from django.core import serializers
from rest_framework.renderers import JSONRenderer
from django.views.generic.edit import FormView

from .models import Experiment, Protocol, InputParameter, ParameterSetting, Algorithm, AppliedAlgorithm
from .forms import AlgorithmForm


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


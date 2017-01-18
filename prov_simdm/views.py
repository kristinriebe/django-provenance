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

from .models import Experiment, Protocol, InputParameter, ParameterSetting


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
    print "link_dict: ", link_dict['protocol']

class ExperimentMoreDetailView(generic.DetailView):
    model = Experiment
    template_name = 'prov_simdm/experiment_moredetail.html'

    def get_context_data(self, **kwargs):
        context = super(ExperimentMoreDetailView, self).get_context_data(**kwargs)

        self.id = self.kwargs['pk']
        parametervalue_list = ParameterSetting.objects.filter(experiment_id=str(self.id))
        if parametervalue_list.exists():
    		print("There is at least one object in some_queryset")
    	#print "parameter list: ", parametervalue_list.query
        #print "p ", parametervalue_list.headline
        for p in parametervalue_list:
        	print(p.id, p.inputParameter.id)
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

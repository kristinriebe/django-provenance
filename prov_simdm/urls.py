from django.conf.urls import url
from . import views

app_name = 'prov_simdm'

urlpatterns = [
    # index view
    url(r'^$', views.IndexView.as_view(), name='index'),

    # experiments etc.
    url(r'^experiments/$', views.ExperimentsView.as_view(), name='experiments'),
    url(r'^experiments/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.ExperimentDetailView.as_view(), name='experiment_detail'),
    url(r'^experiments/(?P<pk>[0-9a-zA-Z.:_-]+)/more$', views.ExperimentMoreDetailView.as_view(), name='experiment_moredetail'),
    url(r'^protocols/$', views.ProtocolsView.as_view(), name='protocols'),
    url(r'^protocols/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.ProtocolDetailView.as_view(), name='protocol_detail'),
    url(r'^inputparameters/$', views.InputParametersView.as_view(), name='inputparameters'),
    url(r'^inputparameters/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.InputParameterDetailView.as_view(), name='inputparameter_detail'),
    url(r'^parametersettings/$', views.ParameterSettingsView.as_view(), name='parametersettings'),
    url(r'^parametersettings/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.ParameterSettingDetailView.as_view(), name='parametersetting_detail'),
    url(r'^alorithms/$', views.AlgorithmsView.as_view(), name='algorithms'),
    url(r'^algorithms/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.AlgorithmDetailView.as_view(), name='algorithm_detail'),
    url(r'^form/$', views.AlgorithmFormResultsView.as_view(), name='algorithm_form'),
    #url(r'^form/$', views.get_algorithmId, name='get_algorithmId'), # also works!
    #url(r'^form/results/$', views.AlgorithmFormResultsView.as_view(), name='algorithm_form'),

    url(r'^datasetform/$', views.DatasetFormResultsView.as_view(), name='dataset_form'),
    url(r'^datasetform_parameters/$', views.get_parameters, name='datasetform_parameters'),

    # provenancedm urls
    url(r'^voprov/entities/$', views.voprov_entities, name='voprov_entities'),


    # simdal urls
    url(r'^simdal/protocols/$', views.simdal_protocols, name='simdal_protocols'),
    url(r'^simdal/projects/$', views.simdal_projects, name='simdal_projects'),
    url(r'^simdal/experiments/$', views.simdal_experiments, name='simdal_experiments'),
    url(r'^simdal/datasets/$', views.simdal_datasets, name='simdal_datasets'),

]


from django.conf.urls import url
from . import views

app_name = 'prov_simdm'

urlpatterns = [
    # index view
    url(r'^$', views.IndexView.as_view(), name='index'),

    # experiments
    url(r'^experiments/$', views.ExperimentsView.as_view(), name='experiments'),
    url(r'^experiments/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.ExperimentDetailView.as_view(), name='experiment_detail'),
    url(r'^experiments/(?P<pk>[0-9a-zA-Z.:_-]+)/more$', views.ExperimentMoreDetailView.as_view(), name='experiment_moredetail'),
    url(r'^protocols/$', views.ProtocolsView.as_view(), name='protocols'),
    url(r'^protocols/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.ProtocolDetailView.as_view(), name='protocol_detail'),
    url(r'^inputparameters/$', views.InputParametersView.as_view(), name='inputparameters'),
    url(r'^inputparameters/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.InputParameterDetailView.as_view(), name='inputparameter_detail'),
    url(r'^parametersettings/$', views.ParameterSettingsView.as_view(), name='parametersettings'),
    url(r'^parametersettings/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.ParameterSettingDetailView.as_view(), name='parametersetting_detail'),
]


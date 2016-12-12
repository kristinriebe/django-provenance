from django.conf.urls import url
from . import views

app_name = 'prov_vo'

urlpatterns = [
    # index view
    url(r'^$', views.IndexView.as_view(), name='index'), # for class-based view
    #url(r'^$', views.index, name='index') # for simple index-view
    
    # activities
    url(r'^activities/$', views.ActivitiesView.as_view(), name='activities'),
    url(r'^activities/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.ActivityDetailView.as_view(), name='activity_detail'),
    url(r'^activities/(?P<pk>[0-9a-zA-Z.:_-]+)/params$', views.ActivityDetailParamsView.as_view(), name='activity_detailparams'),
    url(r'^activitydescriptions/$', views.ActivityDescriptionsView.as_view(), name='activitydescriptions'),
    url(r'^activitydescriptions/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.ActivityDescriptionDetailView.as_view(), name='activitydescription_detail'),
    
    # entities
    url(r'^entities/$', views.EntitiesView.as_view(), name='entities'),
    url(r'^entities/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.EntityDetailView.as_view(), name='entity_detail'),
    url(r'^entitydescriptions/$', views.EntityDescriptionsView.as_view(), name='entitydescriptions'),
    url(r'^entitydescriptions/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.EntityDescriptionDetailView.as_view(), name='entitydescription_detail'),

    # parameters
    url(r'^parameters/$', views.ParametersView.as_view(), name='parameters'),
    url(r'^parameters/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.ParameterDetailView.as_view(), name='parameter_detail'),
    url(r'^parameterdescriptions/$', views.ParameterDescriptionsView.as_view(), name='parameterdescriptions'),
    url(r'^parameterdescriptions/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.ParameterDescriptionDetailView.as_view(), name='parameterdescription_detail'),

    # agents
    url(r'^agents/$', views.AgentsView.as_view(), name='agents'),
    url(r'^agents/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.AgentDetailView.as_view(), name='agent_detail'),  

    # activityflow
    url(r'^activityflows/$', views.ActivityFlowsView.as_view(), name='activityflows'),
    url(r'^activityflows/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.ActivityFlowDetailView.as_view(), name='activityflow_detail'),
    url(r'^activityflows/(?P<pk>[0-9a-zA-Z.:_-]+)/params$', views.ActivityFlowDetailParamsView.as_view(), name='activityflow_detailparams'),


    # graphs
    url(r'^graph/$', views.graph, name='graph'),

    # serialisations
    url(r'^provn/$', views.provn, name='provn')

]

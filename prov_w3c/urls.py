from django.conf.urls import url
from . import views

app_name = 'prov_w3c'

urlpatterns = [
    # index view
    url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^$', views.index, name='index')

    # activities
    url(r'^activities/$', views.ActivitiesView.as_view(), name='activities'),
    url(r'^activities/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.ActivityDetailView.as_view(), name='activity_detail'),
    
    # entities
    url(r'^entities/$', views.EntitiesView.as_view(), name='entities'),
    url(r'^entities/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.EntityDetailView.as_view(), name='entity_detail'),

    # agents
    url(r'^agents/$', views.AgentsView.as_view(), name='agents'),
    url(r'^agents/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.AgentDetailView.as_view(), name='agent_detail'),
    # graphs
    url(r'^graph/$', views.graph, name='graph'),
    url(r'^graph/graphjson$', views.fullgraphjson, name='graphjson'),
    
#    url(r'^graph/mdpl2$', views.graphsingle, name='graph'),
#    url(r'^graph/(?[0-9a-zA-Z.:_-]+)/graphjson$', views.graphjsonact, name='graphjsonact'),

    # serialisations
    url(r'^provn/$', views.provn, name='provn'),
    url(r'^provjson/$', views.provjson, name='provjson'),

]
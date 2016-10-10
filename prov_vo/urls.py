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
    
    # entities
    url(r'^entities/$', views.EntitiesView.as_view(), name='entities'),
    url(r'^entities/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.EntityDetailView.as_view(), name='entity_detail'),
    url(r'^entitydescriptions/$', views.EntityDescriptionsView.as_view(), name='entitydescriptions'),
    url(r'^entitydescriptions/(?P<pk>[0-9a-zA-Z.:_-]+)/$', views.EntityDescriptionDetailView.as_view(), name='entitydescription_detail'),

    # graphs
    url(r'^graph/$', views.graph, name='graph'),

    # serialisations
    url(r'^provn/$', views.provn, name='provn')

]

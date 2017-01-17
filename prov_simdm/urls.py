from django.conf.urls import url
from . import views

app_name = 'prov_simdm'

urlpatterns = [
    # index view
    url(r'^$', views.IndexView.as_view(), name='index'),

    # experiments
    url(r'^experiments/$', views.ExperimentsView.as_view(), name='experiments'),
    url(r'^protocols/$', views.ProtocolsView.as_view(), name='protocols'),
]

"""provenance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
from prov_vo import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^core/', include('core.urls')),
    url(r'^vo/', include('prov_vo.urls')),
    url(r'^w3c/', include('prov_w3c.urls')),
    url(r'^simdm/', include('prov_simdm.urls')),
    url(r'^admin/', admin.site.urls),
]

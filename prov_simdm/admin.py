from django.contrib import admin
from .models import Experiment, Protocol, InputParameter, ParameterSetting, Algorithm

admin.site.register(Experiment)
admin.site.register(Protocol)
admin.site.register(InputParameter)
admin.site.register(Algorithm)


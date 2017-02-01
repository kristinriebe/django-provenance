from django.contrib import admin

from .models import Activity, ActivityDescription, Entity, EntityDescription, Used, UsedDescription, WasGeneratedBy, Agent, WasAssociatedWith, WasAttributedTo
from .models import Parameter, ParameterDescription

# Register your models here.

admin.site.register(Activity)
admin.site.register(ActivityDescription)
admin.site.register(Entity)
admin.site.register(EntityDescription)

admin.site.register(Parameter)
admin.site.register(ParameterDescription)


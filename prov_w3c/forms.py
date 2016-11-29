from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from prov_w3c.models import Entity

class EntityForm(forms.Form):
    #observation_id = forms.CharField(label='RAVE observation id', max_length=1024)    # An inline class to provide additional information on the form.
    entity_list = Entity.objects.all()
    entity_id = forms.ChoiceField(choices=[(e.id, e.label+" ("+e.type+")") for e in entity_list])

    def clean_entity_id(self):
        desired_id = self.cleaned_data['entity_id']
        if desired_id not in [e.id for e in self.entity_list]:
            print "id: " + desired_id
            raise ValidationError(
                _('Invalid value: %(value)s is not a valid entity_id'),
                code='invalid',
                params={'value': desired_id},
            )

        # always return data!
        return desired_id

    #class Meta:
    #    # Provide an association between the ModelForm and a model
    #    model = Entity

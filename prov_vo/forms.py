from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from prov_vo.models import Entity, EntityDescription, Activity, ActivityDescription, Agent, Parameter, ParameterDescription


class DatasetForm(forms.Form):


    # do not use a multi-checkbox with MultipleChoiceField with CheckboxSelectMultiple, but rather
    # make a set of form fields for each parameter
    # => use a boolean for the single check boxes, and add a custom range/value field
    # add all parameters to the form initially, but will hide them using display: none initially using javascript
    def __init__(self, *args, **kwargs):
        super(DatasetForm, self).__init__(*args, **kwargs)

        # dynamically preload the fields, thus put them in the init-fct.
        
        # project choices
        project_list = Agent.objects.filter(type="prov:Organization")
        project_choices = [(p.id, p.label) for p in project_list]
        project_choices.insert(0, ('any', 'any'))
        self.fields['project'] = forms.ChoiceField(choices=project_choices, initial='any')

        # get possible choices for protocol -- TODO: should  get these from models (or from database)
        activitydescription_type_choices = [('cs:simulation', 'Simulation'), ('cs:post-processing', 'Analysis')]
        activitydescription_type_choices.append(('any', 'any'))
        self.fields['activitydescription_type'] = forms.ChoiceField(widget=forms.RadioSelect, choices=activitydescription_type_choices, initial='any')

        # automatically load all possible parameter names and value ranges for the possible protocols/experiments
        activitydescription_choices = [(p.id, p.label) for p in ActivityDescription.objects.all()]
        activitydescription_choices.insert(0, ('any', 'any'))
        self.fields['activitydescription'] = forms.ChoiceField(choices=activitydescription_choices, initial=0, required=False)

        for i, p in enumerate(ParameterDescription.objects.all()):
            label = p.label
            if p.unit and p.unit != '':
                label = p.label + " ["+p.unit+"]"

            self.fields['param_'+p.id] = forms.BooleanField(label=label, required=False)
            if p.datatype == "int":
                self.fields['paramvalue_min_'+p.id] = forms.IntegerField(label='value', required=False)
                self.fields['paramvalue_max_'+p.id] = forms.IntegerField(label='value', required=False)
                self.fields['paramvalue_min_'+p.id].widget.attrs.update({'fieldset': 'param', 'fieldtype': 'paramvalue', 'min': p.minval, 'max': p.maxval, 'value': p.minval})
                self.fields['paramvalue_max_'+p.id].widget.attrs.update({'fieldset': 'param', 'fieldtype': 'paramvalue', 'min': p.minval, 'max': p.maxval, 'value': p.maxval})
            elif p.datatype == "float":
                self.fields['paramvalue_min_'+p.id] = forms.FloatField(label='value', required=False)
                self.fields['paramvalue_max_'+p.id] = forms.FloatField(label='value', required=False)
                self.fields['paramvalue_min_'+p.id].widget.attrs.update({'fieldset': 'param', 'fieldtype': 'paramvalue', 'min': p.minval, 'max': p.maxval, 'value': p.minval})
                self.fields['paramvalue_max_'+p.id].widget.attrs.update({'fieldset': 'param', 'fieldtype': 'paramvalue', 'min': p.minval, 'max': p.maxval, 'value': p.maxval})
            elif p.datatype == "char":
                self.fields['paramvalue_sin_'+p.id] = forms.CharField(label='value', required=False)
                self.fields['paramvalue_sin_'+p.id].widget.attrs.update({'fieldset': 'param', 'fieldtype': 'paramvalue', 'value': p.default})
            else:
                self.fields['paramvalue_sin_'+p.id] = forms.CharField(label='value', required=False)
                self.fields['paramvalue_sin_'+p.id].widget.attrs.update({'fieldset': 'param', 'fieldtype': 'paramvalue', 'value': p.default})

            self.fields['param_'+p.id].widget.attrs.update({'fieldset': 'param', 'fieldtype': 'paramlabel'})
            # add help_text as well
            self.fields['param_'+p.id].help_text = p.annotation


from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from prov_simdm.models import Algorithm, Protocol, Project, Experiment, ParameterSetting, InputParameter


class AlgorithmForm(forms.Form):
    algorithm_list = Algorithm.objects.all()
    algorithm_id = forms.ChoiceField(choices=[(a.id, a.name) for a in algorithm_list])


class DatasetForm(forms.Form):
    # project choices
    project_list = Project.objects.all()
    project_choices = [(p.id, p.name) for p in project_list]
    project_choices.insert(0, ('any', 'any'))
    project_id = forms.ChoiceField(choices=project_choices, initial='any')

    # get possible choices for protocol -- TODO: should  get these from models (or from database)
    protocol_type_choices = [('Simulation', 'Simulation'), ('Analysis', 'Analysis')]
    protocol_type_choices.append(('any', 'any'))
    protocol_type = forms.ChoiceField(widget=forms.RadioSelect, choices=protocol_type_choices, initial='any')

    # automatically load all possible parameter names and value ranges for the possible protocols/experiments
    protocol_choices = [(p.id, p.name) for p in Protocol.objects.all()]
    protocol_choices.insert(0, ('any', 'any'))
    protocol = forms.ChoiceField(choices=protocol_choices, initial=0, required=False)

    # do not use a multi-checkbox with MultipleChoiceField with CheckboxSelectMultiple, but rather
    # make a set of form fields for each parameter
    # => use a boolean for the single check boxes, and add a custom range/value field
    # add all parameters to the form initially, but will hide them using display: none initially using javascript
    def __init__(self, *args, **kwargs):
        super(DatasetForm, self).__init__(*args, **kwargs)

        for i, p in enumerate(InputParameter.objects.all()):
            label = p.name
            if p.unit != '':
                label = p.name + " ["+p.unit+"]"

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

    # Initialize the displayed parameters based on pre-selected protocol
    # skipped this here, because want to include all params anyway in form, and show/hide them using javascript
    #
    # def __init__(self, *args, **kwargs):
    #     forms.Form.__init__(self, *args, **kwargs)
    #     parents = Protocol.objects.all()
    #     if len(parents)==1:
    #         self.fields['protocol'].initial = parents[0].id
    #
    #     parent_id = self.fields['protocol'].initial or self.initial.get('protocol') \
    #              # or self._raw_value('parent')
    #     if parent_id:
    #         # parent is known. Now I can display the matching children.
    #         children = InputParameter.objects.filter(protocol__id=parent_id)
    #         self.fields['parameter'].queryset=children
    #         if len(children)==1:
    #             self.fields['parameter'].initial=children[0].id

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

    # add list of all parameters to the form initially (especially since protocol is set to'any' initially)
    parameter_choices = [(p.id, p.name) for p in InputParameter.objects.all()]
    parameter = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=parameter_choices, required=False)


    # Initialize the displayed parameters based on pre-selected protocol
    # skipped this here, because want to display all params anyway and show/hide them using javascript
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

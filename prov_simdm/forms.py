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

    # get possible choices for protocol -- TODO: should  get these from models(0 or from database)
    protocol_type_choices = [('Simulation', 'Simulation'), ('Analysis', 'Analysis')]
    protocol_type_choices.append(('any', 'any'))
    protocol_type = forms.ChoiceField(widget=forms.RadioSelect, choices=protocol_type_choices, initial='any')


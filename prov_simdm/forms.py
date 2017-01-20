from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from prov_simdm.models import Algorithm, Protocol

class AlgorithmForm(forms.Form):
    algorithm_list = Algorithm.objects.all()
    algorithm_id = forms.ChoiceField(choices=[(a.id, a.name) for a in algorithm_list])

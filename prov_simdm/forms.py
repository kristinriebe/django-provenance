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
    project_id.group = 'main'

    # get possible choices for protocol -- TODO: should  get these from models (or from database)
    protocol_type_choices = [('Simulation', 'Simulation'), ('Analysis', 'Analysis')]
    protocol_type_choices.append(('any', 'any'))
    protocol_type = forms.ChoiceField(widget=forms.RadioSelect, choices=protocol_type_choices, initial='any')
    protocol_type.group = 'main'

    # automatically load all possible parameter names and value ranges for the possible protocols/experiments
    protocol_choices = [(p.id, p.name) for p in Protocol.objects.all()]
    protocol_choices.insert(0, ('any', 'any'))
    protocol = forms.ChoiceField(choices=protocol_choices, initial=0, required=False)
    protocol.group = 'main'

    # add list of all parameters to the form initially (especially since protocol is set to 'any' initially)
    #parameter_choices = [(p.id, p.name) for p in InputParameter.objects.all()]
    #parameters = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=parameter_choices, required=False)

    # change strategy: rather make a set of form fields for each parameter, not multi-checkbox
    # thus can use a boolean for the single check boxes, and add a custom range/value field
    def __init__(self, *args, **kwargs):
        super(DatasetForm, self).__init__(*args, **kwargs)

        for i, p in enumerate(InputParameter.objects.all()):
            #parameters = formset
            self.fields['param_'+p.name] = forms.BooleanField(label=p.name, required=False)
            self.fields['paramvalue_'+p.name] = forms.IntegerField(label='value', required=False)

            self.fields['param_'+p.name].widget.attrs.update({'title': 'the title', 'fieldset': 'param'})
            self.fields['paramvalue_'+p.name].widget.attrs.update({'fieldset': 'param', 'fieldsettype': 'value'})

            self.fields['param_'+p.name].group = 'parameters'
            self.fields['paramvalue_'+p.name].group = 'parameters'

            print self.fields

    def maingroup(self):
        fie = {f for f in self.fields.values() if f.group == 'main'}
        for f in fie:  #self.fields.values():
            print f.label
            #print f.group
            #print f.id
        return filter(lambda x: x.group == 'main', self.fields.values())

    def paramgroup(self):
        #for f in self.fields:
        #    print f.widget.widget_attrs

        return filter(lambda x: x.group == 'parameters', self.fields.values())

    def allgroups(self):
        return self.fields #{f.get_bound_field() for f in self.fields}

    # add input fields for the parameter values
    # -- should be put next to each param! (do with javascript?)
#    parameter_settings = [(p.value, p.value) for p in ParameterSetting.objects.all()]
#    parameters = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=parameter_choices, required=False)




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

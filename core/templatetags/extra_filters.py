from django import template

register = template.Library()


@register.filter(name='lookup_attribute')
def lookup_attribute(classname, attribute):
    # usage: {{ mydict|lookup_attribute:keyname }}
    return getattr(classname, attribute)

#register.filter('lookup', lookup)

@register.filter(name='get_dictvalue')
def get_value_from_dict(dict_data, key):
    # usage: {{ mydict|get_dictvalue:keyname }}
    if key:
        return dict_data.get(key)
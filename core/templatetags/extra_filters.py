from django import template

register = template.Library()


@register.filter(name='lookup_attribute')
def lookup_attribute(classname, attribute):
    return getattr(classname, attribute)
# usage: {{ mydict|lookup:keyname }}

#register.filter('lookup', lookup)

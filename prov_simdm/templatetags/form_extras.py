from django import template

register = template.Library()

def strip_right_of_first(value, arg):
    """Removes everything right of first occurence of given arg-string"""
    substr = value.split(arg)[0]
    # ... this returns the original string, if arg is not found, which is fine
    return substr
register.filter('strip_right_of_first', strip_right_of_first)

def strip_left_of_last(value, arg):
    """Removes everything left of last occurence of given arg-string"""
    substr = value.split(arg)[-1]
    # ... this returns the original string, if arg is not found, which is fine
    return substr
register.filter('strip_left_of_last', strip_left_of_last)

def strip_left_of_first(value, arg):
    """Removes everything left of first occurence of given arg-string"""
    i = value.find(arg)
    substr = value[i+1:]
    # if arg is not found, then i=-1 => substr = value[0:]
    # => also returns the original string, if arg is not found
    return substr
register.filter('strip_left_of_first', strip_left_of_first)

def startswith(value, arg):
    """Checks if value-string starts with arg-string, returns True or False"""
    success = value.startswith(arg)
    # ... thhis returns the original string, if no '_' is found, which is fine
    return success
register.filter('startswith', startswith)

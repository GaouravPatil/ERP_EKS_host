from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using a key"""
    return dictionary.get(key, [])

@register.filter
def make_list(value):
    """Split a comma-separated string into a list"""
    if isinstance(value, str):
        return [item.strip() for item in value.split(',')]
    return value

@register.filter
def default_if_none(value, default):
    """Return default if value is None"""
    if value is None:
        return default
    return value

@register.filter
def lookup(dictionary, key):
    """Lookup a key in dictionary"""
    try:
        return dictionary[key]
    except (KeyError, TypeError):
        return []
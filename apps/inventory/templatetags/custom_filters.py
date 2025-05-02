from django import template

register = template.Library()

@register.filter(name='uppercase')
def uppercase(value):
    """Converts the input to uppercase."""
    return str(value).upper()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """Safely gets a value from a dictionary using a key."""
    try:
        return dictionary.get(key)
    except (AttributeError, TypeError):
        return None

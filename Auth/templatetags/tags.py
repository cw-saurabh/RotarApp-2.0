from django import template
from django.core.files.storage import default_storage

register = template.Library()

@register.filter(name='image_exists')
def image_exists(filepath):
    if default_storage.exists(filepath):
        return filepath
    else:
        return 'distLogos/district_logo.png'
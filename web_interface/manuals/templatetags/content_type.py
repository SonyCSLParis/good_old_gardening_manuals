from django import template
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.filter
def content_type(obj):
    if not obj:
        return False
    return ContentType.objects.get_for_model(obj)

#ct = ContentType.objects.get_for_id(content_type)
#obj = ct.get_object_for_this_type(pk=object_id)

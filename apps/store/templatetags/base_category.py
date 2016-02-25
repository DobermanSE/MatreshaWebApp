from django import template
from apps.store import models
register = template.Library()


@register.inclusion_tag('base_category.html')
def category_list():
    return {'categories': models.Category.objects.all()}


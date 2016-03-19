from django import template
from apps.store import models
register = template.Library()


@register.inclusion_tag('base_category.html')
def category_list():
    categories = models.Category.objects.all()
    parent_categories = filter(lambda x: x.parentCategory is None, categories)

    grouped_categories = dict()

    for category in parent_categories:
        child_categories = list(filter(lambda x: x.parentCategory == category, categories))
        if len(child_categories) > 0:
            grouped_categories[category] = child_categories

    return {'categories': grouped_categories}

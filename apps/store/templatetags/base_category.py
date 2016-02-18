from django import template

register = template.Library()


# TODO: Load categories from DB
@register.inclusion_tag('base_category.html')
def category_list():
    return {'categories': ['Верхняя одежда', 'Одежда', 'Обувь', 'Бельё', 'Детская одежда']}


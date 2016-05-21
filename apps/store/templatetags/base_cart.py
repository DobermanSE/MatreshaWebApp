from django import template
from apps.store import models
register = template.Library()


@register.inclusion_tag('base_cart.html', takes_context=True)
def cart(context):
    request = context['request']
    goods_in_cart = 0
    if 'cart' in request.session:
        goods_in_cart = len(request.session['cart'])
    return {'goods_in_cart': goods_in_cart}

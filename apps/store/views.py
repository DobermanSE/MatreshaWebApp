from django.shortcuts import render, redirect
from apps.store.models import Product, Category, ProductImage, ProductDetail, ProductDetailValue
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from apps.store.forms import AddProductFrom
from django.http import HttpResponse
from django.core import serializers
import json


def index(request):
    context = {'products': Product.objects.all()[:5]}
    return render(request, "index.html", context)


def product(request, product_id):
    context = {
        "product":  Product.objects.get(pk=product_id),
        "images": ProductImage.objects.filter(product=product_id, isMain=False)[:5],
        "main_image": ProductImage.objects.get(product=product_id, isMain=True),
    }
    return render(request, "product.html", context)


def products_by_category(request, category_id):
    context = {
        "products":  Product.objects.filter(category=category_id),
        "category": Category.objects.get(pk=category_id)
    }
    return render(request, "products.html", context)


def get_subcategories(request):
    """ Получить подкатегорию в зависимости от выбранной категории """
    categories_query = Category.objects.filter(parentCategory__id=request.GET['category'])
    response_data = serializers.serialize("json", categories_query, ensure_ascii=False)
    return HttpResponse(
            json.dumps(response_data, ensure_ascii=False), content_type="application/json; encoding=utf-8")


def get_product_details(request):
    """ Получить основныее и дополнительные характеристики """
    product_detail_query = ProductDetail.objects.filter(category__id=request.GET['category'])

    if product_detail_query is None or product_detail_query.count() < 1:
        return HttpResponse()

    product_details = product_detail_query.values()

    result = dict([('main', list()), ('sub', list())])

    for detail in product_details:
        product_detail_value_query = ProductDetailValue.objects.filter(productDetail__id=detail['id'])
        if product_detail_value_query is None or product_detail_value_query.count() < 1:
            continue
        product_detail_values = list(product_detail_value_query.values())
        if detail['is_main']:
            result['main'].append(dict([(detail['name'], product_detail_values)]))
        else:
            result['sub'].append(dict([(detail['name'], product_detail_values)]))

    json_response = json.dumps(result, ensure_ascii=False)

    return HttpResponse(json_response, content_type="application/json; encoding=utf-8")


def add_to_cart(request):
    """ Добавление в корзину """
    if 'cart' not in request.session:
        request.session['cart'] = dict()

    product_id = request.POST['product_id']

    if product_id not in request.session['cart']:
        request.session['cart'][product_id] = 1
    else:
        current_count = request.session['cart'][product_id]
        request.session['cart'][product_id] = current_count + 1

    request.session.modified = True
    return redirect('cart')


def delete_from_cart(request):
    """ Удаление из корзины """
    if 'cart' in request.session:
        del request.session['cart'][request.POST['product_id']]
    request.session.modified = True
    return redirect('cart')


def cart(request):
    """ Корзина """
    products = dict()
    for key, value in request.session['cart'].items():
        products[Product.objects.get(pk=key)] = value
    context = {
        "products": products,
        "products_count": len(products)
    }
    return render(request, "cart.html", context)


class AddProduct(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    context = {
        "product_form": AddProductFrom()
    }

    def get(self, *args, **kwargs):
        if self.request.user.groups.filter(name='sellers').exists():
            return render(self.request, 'add_product.html', self.context)
        else:
            return render(self.request, 'login.html', self.context)


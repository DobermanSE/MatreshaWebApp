from django.shortcuts import render, redirect
from apps.store.models import Product, Category, ProductImage, ProductDetail, ProductDetailValue, Manufacturer, ProductPosition, ValueProductPosition
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from apps.store.forms import AddProductFrom
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers

import json


def index(request):
    context = {'products': Product.objects.all()[:5]}
    return render(request, "index.html", context)


def product(request, product_id):

    main_value_product_positions = ValueProductPosition.objects.filter(product__id=product_id, product_position__isnull=True)
    extra_details = dict()

    if main_value_product_positions is not None:
        main_details = [p.product_detail_value for p in main_value_product_positions]

    extra_value_product_positions = ValueProductPosition.objects.filter(product__id=product_id, product_position__isnull=False)

    for extra_value_product_position in extra_value_product_positions:
        if extra_value_product_position.product_detail_value.productDetail.name not in extra_details:
            extra_details[extra_value_product_position.product_detail_value.productDetail.name] = list()
            extra_details[extra_value_product_position.product_detail_value.productDetail.name].append(extra_value_product_position.product_detail_value)
        else:
            extra_details[extra_value_product_position.product_detail_value.productDetail.name].append(extra_value_product_position.product_detail_value)

    context = {
        "product":  Product.objects.get(pk=product_id),
        "images": ProductImage.objects.filter(product=product_id, isMain=False)[:5],
        "main_image": ProductImage.objects.get(product=product_id, isMain=True),
        "main_details": main_details,
        "extra_details": extra_details
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
    if 'cart' not in request.session:
        request.session['cart'] = dict()
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
    form_class = AddProductFrom
    template_name = "add_product.html"

    def get(self, *args, **kwargs):
        if self.request.user.groups.filter(name='sellers').exists():
            return render(self.request, 'add_product.html', self.context)
        else:
            return render(self.request, 'login.html', self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            # <process form cleaned data>
            product_positions = dict()

            product_indexes = [p[p.rfind('_')+1:] for p in form.data.keys() if p.startswith('sub_select_')]
            unique_product_indexes = set(product_indexes)
            product_indexes_list = list(unique_product_indexes)

            sub_details = [p for p in form.data.keys() if p.startswith('sub_select_') and p.endswith('_p_' + product_indexes_list[0])]
            sub_details_count = len(sub_details)

            for product_index in product_indexes_list:
                product_positions[product_index] = dict()
                for i in range(0, sub_details_count):
                    product_positions[product_index][i] = form.data['sub_select_' + str(i) + '_p_' + product_index]
                product_positions[product_index]['count'] = form.data['count_input_p_' + product_index]

            new_product = Product(name=form.data['name'],
                              description=form.data['description'],
                              productStatus=1,
                              price=form.data['price'],
                              manufacturer=Manufacturer.objects.filter(id=1)[0],
                              category=Category.objects.filter(id=form.data['category'])[0],
                              seller=request.user)

            new_product.save()

            value_product_position = ValueProductPosition(product_detail_value=ProductDetailValue.objects.filter(id=form.data['select_0'])[0],
                                                          product=new_product)
            value_product_position.save()

            for key in product_positions.keys():
                product_position = ProductPosition(product=new_product, count=product_positions[key]['count'])
                product_position.save()
                for sub_key in product_positions[key].keys():
                    if sub_key == 'count':
                        continue
                    value_product_position = ValueProductPosition(product_detail_value=ProductDetailValue.objects.filter(id=product_positions[key][sub_key])[0],
                                                          product=new_product, product_position=product_position)
                    value_product_position.save()

            for file_key in request.FILES.keys():
                main_image = ProductImage(image=request.FILES[file_key], isMain=file_key == 'main_image', product=new_product)
                main_image.save()

            return render(request, 'index.html')

        return render(request, self.template_name, {'form': form})

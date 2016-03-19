from django.shortcuts import render
from apps.store.models import Product, Category, ProductImage
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
    categories_query = Category.objects.filter(parentCategory__id=request.GET['category'][0])
    response_data = serializers.serialize("json", categories_query)
    return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


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


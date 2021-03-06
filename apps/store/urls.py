from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /store/
    url(r'^$', views.index, name='index'),
    # ex: /store/product/5/
    url(r'^product/(?P<product_id>[0-9]+)/$', views.product, name="product"),
    # ex: /store/category/5/products/
    url(r'^category/(?P<category_id>[0-9]+)/products/$', views.products_by_category, name="products_by_category"),
    # ex: /store/add_product
    url(r'^add_product/$', views.AddProduct.as_view(), name="add_product"),
    # ex: /store/get_subcategories
    url(r'^get_subcategories/$', views.get_subcategories, name="get_subcategories"),
    # ex: /store/get_product_details
    url(r'^get_product_details/$', views.get_product_details, name="get_product_details"),
    # ex: /store/cart
    url(r'^cart/$', views.cart, name="cart"),
    # ex: /store/add_to_cart/
    # POST
    url(r'^add_to_cart/$', views.add_to_cart, name="add_to_cart"),
    # ex: /store/delete_from_cart/
    # POST
    url(r'^delete_from_cart/$', views.delete_from_cart, name="delete_from_cart"),
]



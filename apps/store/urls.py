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
    # ex: /store/cart
    url(r'^cart/$', views.cart, name="cart"),
]



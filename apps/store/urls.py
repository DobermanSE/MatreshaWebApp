from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /store/
    url(r'^$', views.index, name='index'),
    # ex: /store/product/5/
    url(r'^product/(?P<product_id>[0-9]+)/$', views.product, name="product"),
    # ex: /store/category/5/
    url(r'^category/(?P<category_id>[0-9]+)/$', views.products_by_category, name="products_by_category"),
]

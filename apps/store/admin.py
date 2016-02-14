from django.contrib import admin
from .models import Product, OrderStatus, ProductStatus, ProductDetail, ProductDetailValue, Category, Manufacturer, OrderPosition, Order

admin.site.register(Product)
admin.site.register(OrderStatus)
admin.site.register(ProductStatus)
admin.site.register(ProductDetail)
admin.site.register(ProductDetailValue)
admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(OrderPosition)
admin.site.register(Order)

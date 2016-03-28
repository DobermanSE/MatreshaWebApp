from django.contrib import admin
from . import models

admin.site.register(models.Product)
admin.site.register(models.ProductDetail)
admin.site.register(models.ProductDetailValue)
admin.site.register(models.Category)
admin.site.register(models.Manufacturer)
admin.site.register(models.OrderPosition)
admin.site.register(models.Order)
admin.site.register(models.ProductImage)
admin.site.register(models.ProductPosition)
admin.site.register(models.ValueProductPosition)

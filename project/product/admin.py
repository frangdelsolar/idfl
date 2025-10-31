from django.contrib import admin
from .models import (
    Product, 
    ProductCategory, 
    ProductDetail, 
    RawMaterial
)

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductDetail)
admin.site.register(RawMaterial)

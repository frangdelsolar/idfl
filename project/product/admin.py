from django.contrib import admin

from .forms import (
    ProductModelForm, 
    RawMaterialInlineForm
)

from .models import (
    Product, 
    ProductCategory, 
    ProductDetail, 
    RawMaterial
)

class RawMaterialInline(admin.TabularInline):
    """
    Inline editor for managing raw materials associated with products.
    
    Features:
    - Displays raw materials as tabular inline entries
    - Uses DAL autocomplete for efficient material selection
    - Allows adding/removing materials without page navigation
    """
    model = Product.raw_materials.through 
    form = RawMaterialInlineForm
    extra = 1 

class ProductAdmin(admin.ModelAdmin):
    """
    Custom admin interface for Product management.
    
    Features:
    - Autocomplete for detail and category fields
    - Inline raw material management
    - Search functionality across related fields
    - Clean form interface with excluded duplicate fields
    """
    form = ProductModelForm
    inlines = [RawMaterialInline]

    list_display = ('name', 'detail__description', 'category__description')
    search_fields = ['name', 'detail__description', 'category__description']
    exclude  = ['raw_materials']
    ordering = ['name']


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(ProductDetail)
admin.site.register(RawMaterial)
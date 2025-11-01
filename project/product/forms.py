from dal import autocomplete
from django import forms

from .models import Product


class RawMaterialInlineForm(forms.ModelForm):
    """
    Form for inline raw material entries with autocomplete.
    
    Enables:
    - Quick search and selection of raw materials
    - Validation through the through model
    """
    class Meta:
        model = Product.raw_materials.through 
        fields = '__all__'
        widgets = {
            "rawmaterial": autocomplete.ModelSelect2(url="raw_material_autocomplete"), 
        }


class ProductModelForm(forms.ModelForm):
    """
    Custom form for Product model with autocomplete widgets.
    
    Provides:
    - Autocomplete selection for product details
    - Autocomplete selection for product categories
    - Optimized for large datasets with lazy loading
    """
    class Meta:
        model = Product
        fields = [
            'name',
            'detail',
            'category',
        ]
        widgets = {
            "detail": autocomplete.ModelSelect2(url="product_detail_autocomplete"),
            "category": autocomplete.ModelSelect2(url="product_category_autocomplete"),
        }
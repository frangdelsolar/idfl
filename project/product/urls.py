from django.urls import path
from product.views import (
    ProductCategoryAutocomplete, 
    ProductDetailAutocomplete, 
    RawMaterialAutocomplete
)

urlpatterns = [
    path(
        'product-category-autocomplete/',
        ProductCategoryAutocomplete.as_view(),
        name='product_category_autocomplete',
    ),
    path(
        'product-detail-autocomplete/',
        ProductDetailAutocomplete.as_view(),
        name='product_detail_autocomplete',
    ),
    path(
        'raw-material-autocomplete/',
        RawMaterialAutocomplete.as_view(),
        name='raw_material_autocomplete',
    ),
]
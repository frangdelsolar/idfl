from dal import autocomplete
from .models import ProductCategory, ProductDetail, RawMaterial

class ProductCategoryAutocomplete(autocomplete.Select2QuerySetView):
    """
    Autocomplete view for ProductCategory model.
    
    Filters:
    - Only returns active product categories
    - Searches by description field
    - Requires user authentication
    """

    def get_queryset(self):
        """Return filtered queryset based on search term and active status."""

        if not self.request.user.is_authenticated:
            return ProductCategory.objects.none()
        qs = ProductCategory.objects.filter(is_active=True)
        if self.q:
            qs = qs.filter(description__icontains=self.q)
        return qs


class ProductDetailAutocomplete(autocomplete.Select2QuerySetView):
    """
    Autocomplete view for ProductDetail model.
    
    Filters:
    - Only returns active product details
    - Searches by description field
    - Requires user authentication
    """

    def get_queryset(self):
        """Return filtered queryset based on search term and active status."""

        if not self.request.user.is_authenticated:
            return ProductDetail.objects.none()
        qs = ProductDetail.objects.filter(is_active=True)
        if self.q:
            qs = qs.filter(description__icontains=self.q)
        return qs


class RawMaterialAutocomplete(autocomplete.Select2QuerySetView):
    """
    Autocomplete view for RawMaterial model.
    
    Filters:
    - Only returns active raw materials
    - Searches by description field
    - Requires user authentication
    """

    def get_queryset(self):
        """Return filtered queryset based on search term and active status."""

        if not self.request.user.is_authenticated:
            return RawMaterial.objects.none()
        qs = RawMaterial.objects.filter(is_active=True)
        if self.q:
            qs = qs.filter(description__icontains=self.q)
        return qs
    
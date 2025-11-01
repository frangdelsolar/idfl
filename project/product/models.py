from django.db import models


class ProductCategory(models.Model):
    """
    Hierarchical classification system for product organization.
    
    Provides structured categorization for products (e.g., "Men's Apparel", "Electronics", 
    "Home Goods") to enable filtering, reporting, and navigation.
    """
    code = models.CharField(
        max_length=120, 
        unique=True, 
        null=False, 
        blank=False,
        help_text="Unique category identifier (e.g., 'APP-MEN', 'ELEC-SMARTPHONE')."
    )
    description = models.CharField(
        max_length=120, 
        null=False, 
        blank=False,
        help_text="Human-readable category name for display and selection (e.g., 'Men's Apparel')."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this category from selection in new products (retains historical data)."
    )

    class Meta:
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return f'{self.code} - {self.description}'


class ProductDetail(models.Model):
    """
    Specific product variant or SKU-level information.
    
    Stores detailed specifications for individual product variants, allowing multiple
    products to share the same base details while maintaining unique identifiers.
    """
    code = models.CharField(
        max_length=120, 
        unique=True, 
        null=False, 
        blank=False,
        help_text="Unique product variant code (SKU). Example: 'IPHONE14-BLK-128'."
    )
    description = models.CharField(
        max_length=120, 
        null=False, 
        blank=False,
        help_text="Detailed specification or variant description (e.g., size, color, model year)."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Controls if this product detail is available for new product creation."
    )
    
    class Meta:
        verbose_name_plural = "Product Details"

    def __str__(self):
        return f'{self.code} - {self.description}'


class RawMaterial(models.Model):
    """
    Inventory of raw materials and components used in product manufacturing.
    
    Tracks all materials, ingredients, or components required for product assembly
    or manufacturing. Supports bill of materials (BOM) calculations and inventory management.
    """
    code = models.CharField(
        max_length=120, 
        unique=True, 
        null=False, 
        blank=False,
        help_text="Unique identifier for inventory tracking (e.g., 'COTTON-100PCT', 'STEEL-GA16')."
    )
    description = models.CharField(
        max_length=120, 
        null=False, 
        blank=False,
        help_text="Detailed description of the material, grade, or composition."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates if the material is currently available for new product formulations."
    )
 
    class Meta:
        verbose_name_plural = "Raw Materials"

    def __str__(self):
        return f'{self.code} - {self.description}'


class Product(models.Model):
    """
    Master product record linking categorization, specifications, and composition.
    
    Serves as the central entity connecting product categories, detailed specifications,
    and raw material requirements. Supports complete product definition from marketing
    to manufacturing.
    """
    name = models.CharField(
        max_length=120, 
        null=True, 
        blank=True,
        help_text="Marketing name or common product identifier (optional)."
    )
    detail = models.ForeignKey(
        'product.ProductDetail', 
        null=True, 
        on_delete=models.SET_NULL,
        help_text="Specific product variant (SKU) details and specifications."
    )
    category = models.ForeignKey(
        'product.ProductCategory', 
        null=True, 
        on_delete=models.SET_NULL,
        help_text="The classification group this product belongs to."
    )
    raw_materials = models.ManyToManyField(
        'product.RawMaterial',
        help_text="List of raw materials and components required for this product."
    )

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        """Descriptive representation combining category and product details."""
        category_name = self.category.description if self.category else "Uncategorized"
        detail_name = self.detail.description if self.detail else "No Details"
        return f"{category_name} - {detail_name}"
from django.db import models


class ProductCategory(models.Model):
    """
    Represents a category for products (e.g., "Men's Apparel", "Electronics").
    
    Attributes:
        code: Unique identifier for the category (e.g., "PC0001")
        description: Human-readable name of the category
    """
    code = models.CharField(max_length=120, null=False, blank=False)
    description = models.CharField(max_length=120, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return f'{self.code} - {self.description}'


class ProductDetail(models.Model):
    """
    Stores detailed information about a specific product variant.
    
    Attributes:
        code: SKU or product identifier (e.g., "PD-001")
        description: Detailed product description or name
    """
    code = models.CharField(max_length=120, null=False, blank=False)
    description = models.CharField(max_length=120, null=False, blank=False)
    
    class Meta:
        verbose_name_plural = "Product Details"

    def __str__(self):
        return f'{self.code} - {self.description}'


class RawMaterial(models.Model):
    """
    Represents raw materials used in product manufacturing.
    
    Attributes:
        code: Material identifier (e.g., "RM-001") 
        description: Description of the raw material
    """
    code = models.CharField(max_length=120, null=False, blank=False)
    description = models.CharField(max_length=120, null=False, blank=False)
    
    class Meta:
        verbose_name_plural = "Raw Materials"

    def __str__(self):
        return f'{self.code} - {self.description}'


class Product(models.Model):
    """
    Main product model that links details, category, and raw materials.
    
    Attributes:
        detail: Specific product variant details
        category: Product classification category
        raw_materials: Materials used to manufacture this product
        name: Product name (you need to add this field!)
    """
    detail = models.ForeignKey('product.ProductDetail', null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey('product.ProductCategory', null=True, on_delete=models.SET_NULL)
    raw_materials = models.ManyToManyField('product.RawMaterial')

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.category} - {self.detail.description}"
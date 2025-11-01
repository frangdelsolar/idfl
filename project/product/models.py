from django.db import models


class ProductCategory(models.Model):
    """
    Hierarchical classification system for product organization.
    
    Provides structured categorization for products (e.g., "Men's Apparel", "Electronics", 
    "Home Goods") to enable filtering, reporting, and navigation.
    
    Attributes:
        code (str): Unique category identifier following business coding conventions.
                    Examples: "PC0001", "APP-MEN", "ELEC-SMARTPHONE"
        description (str): Human-readable category name for display and selection
        is_active (bool): Controls category visibility in active selection lists.
                         Inactive categories remain in database for historical reporting.
    
    Business Rules:
        - Code must be unique across all categories
        - Both code and description are required for proper identification
        - Categories can be deactivated without losing historical product associations
    
    Example:
        >>> category = ProductCategory(code="APP-MEN", description="Men's Apparel")
        >>> category.save()
    """
    code = models.CharField(max_length=120, unique=True, null=False, blank=False)
    description = models.CharField(max_length=120, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return f'{self.code} - {self.description}'


class ProductDetail(models.Model):
    """
    Specific product variant or SKU-level information.
    
    Stores detailed specifications for individual product variants, allowing multiple
    products to share the same base details while maintaining unique identifiers.
    
    Attributes:
        code (str): Stock Keeping Unit (SKU) or unique product variant identifier.
                   Examples: "IPHONE14-BLK-128", "TSHIRT-MED-BLUE"
        description (str): Comprehensive product description including specifications,
                          features, and variant details
        is_active (bool): Indicates whether this product variant is currently available
                         for sale or manufacturing
    
    Use Cases:
        - Different sizes/colors of the same product
        - Product revisions or model years
        - Regional product variations
    
    Example:
        >>> detail = ProductDetail(code="TSHIRT-M-BLU", description="Cotton T-Shirt - Medium - Blue")
        >>> detail.save()
    """
    code = models.CharField(max_length=120, unique=True, null=False, blank=False)
    description = models.CharField(max_length=120, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Product Details"

    def __str__(self):
        return f'{self.code} - {self.description}'


class RawMaterial(models.Model):
    """
    Inventory of raw materials and components used in product manufacturing.
    
    Tracks all materials, ingredients, or components required for product assembly
    or manufacturing. Supports bill of materials (BOM) calculations and inventory management.
    
    Attributes:
        code (str): Unique material identifier for inventory tracking.
                   Examples: "COTTON-100PCT", "STEEL-GA16", "ELECT-MOTOR-5HP"
        description (str): Detailed material description including specifications,
                          grade, or composition
        is_active (bool): Indicates material is available for use in new products.
                        Inactive materials remain for historical product records.
    
    Inventory Context:
        - Used in product composition tracking
        - Supports supply chain and procurement planning
        - Enables material requirement planning (MRP) calculations
    """
    code = models.CharField(max_length=120, unique=True, null=False, blank=False)
    description = models.CharField(max_length=120, null=False, blank=False)
    is_active = models.BooleanField(default=True)
 
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
    
    Attributes:
        name (str): Marketing or common product name. Optional for system-generated names
                   based on category and detail information.
        detail (ForeignKey): Specific product variant details and specifications.
                           SET_NULL preserves product if detail record is removed.
        category (ForeignKey): Product classification and categorization.
                             SET_NULL maintains product in historical categories.
        raw_materials (ManyToMany): Bill of materials defining required components
                                   and quantities for manufacturing.
    
    Design Considerations:
        - Optional name allows for system-generated descriptive names
        - SET_NULL on foreign keys maintains data integrity during category/detail changes
        - Many-to-many relationship supports complex product compositions
    
    Example:
        >>> product = Product.objects.create(
        ...     name="Premium Cotton T-Shirt",
        ...     category=apparel_category,
        ...     detail=tshirt_detail
        ... )
        >>> product.raw_materials.add(cotton, thread, dye)
        >>> product.save()
    """
    name = models.CharField(max_length=120, null=True, blank=True)
    detail = models.ForeignKey('product.ProductDetail', null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey('product.ProductCategory', null=True, on_delete=models.SET_NULL)
    raw_materials = models.ManyToManyField('product.RawMaterial')

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        """Descriptive representation combining category and product details."""
        category_name = self.category.description if self.category else "Uncategorized"
        detail_name = self.detail.description if self.detail else "No Details"
        return f"{category_name} - {detail_name}"
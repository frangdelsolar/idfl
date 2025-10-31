from django.db import models


class ProductCategory(models.Model):
    code = models.CharField(max_length=120, null=False, blank=False)
    description = models.CharField(max_length=120, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Product Categories"

    def __str__(self):
        return f'{self.code} - {self.description}'

class ProductDetail(models.Model):
    code = models.CharField(max_length=120, null=False, blank=False)
    description = models.CharField(max_length=120, null=False, blank=False)
    
    class Meta:
        verbose_name_plural = "Product Details"

    def __str__(self):
        return f'{self.code} - {self.description}'

class RawMaterial(models.Model):
    code = models.CharField(max_length=120, null=False, blank=False)
    description = models.CharField(max_length=120, null=False, blank=False)
    
    class Meta:
        verbose_name_plural = "Raw Materials"

    def __str__(self):
        return f'{self.code} - {self.description}'

class Product(models.Model):
    detail = models.ForeignKey('product.ProductDetail', null=True, on_delete=models.SET_NULL) 
    category = models.ForeignKey('product.ProductCategory', null=True, on_delete=models.SET_NULL)
    raw_materials = models.ManyToManyField('product.RawMaterial')

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name

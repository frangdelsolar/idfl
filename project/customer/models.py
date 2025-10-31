from django.db import models

# null=True -> db can store null value in the column
# blank=True -> form can accept empty value in the field

class Address(models.Model):
    address = models.CharField(max_length=120, null=False, blank=False)
    city = models.CharField(max_length=120, null=False, blank=False)
    state = models.CharField(max_length=120, null=False, blank=False)
    zip_code = models.CharField(max_length=120, null=False, blank=False)
    country = models.CharField(max_length=120, null=False, blank=False)
    class Meta: 
        verbose_name_plural = "Addresses" # We improve pluralization

    def __str__(self):
        return f'{self.address}, {self.city}, {self.state}, {self.country}'

class Company(models.Model):
    users = models.ManyToManyField('auth.User')
    name = models.CharField(max_length=120, null=False, blank=False) # max_length is required for CharField
    address = models.ForeignKey('customer.Address', null=True, on_delete=models.SET_NULL) # SET_NULL we will persist company data even if we don't have an address

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name

class SupplyChainCompany(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)
    is_valid = models.BooleanField(default=False)
    address = models.ForeignKey('customer.Address', null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = "Supply Chain Companies"

    def __str__(self):
        return self.name

class CertificationBody(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)
    address = models.ForeignKey('customer.Address', null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = "Certification Bodies"

    def __str__(self):
        return self.name
from django.db import models

# null=True -> db can store null value in the column
# blank=True -> form can accept empty value in the field

class Address(models.Model):
    """
    Comprehensive geographical address model.
    
    Stores complete address information that can be reused across
    multiple entities (companies, supply chain partners, etc.).
    
    Attributes:
        address (str): Street address line
        city (str): City name
        state (str): State or province
        zip_code (str): Postal or ZIP code
        country (str): Country name
    """
    address = models.CharField(max_length=120, null=False, blank=False)
    city = models.CharField(max_length=120, null=False, blank=False)
    state = models.CharField(max_length=120, null=False, blank=False)
    zip_code = models.CharField(max_length=120, null=False, blank=False)
    country = models.CharField(max_length=120, null=False, blank=False)
    
    class Meta: 
        verbose_name_plural = "Addresses" # We improve pluralization

    def __str__(self):
        """Human-readable representation of the full address."""
        return f'{self.address}, {self.city}, {self.state}, {self.country}'


class Company(models.Model):
    """
    Primary company entity with user access control.
    
    Represents a business organization that can have multiple users
    associated with it. Maintains company data even if address is removed.
    
    Attributes:
        users (ManyToMany): Django auth users with company access
        name (str): Legal company name
        address (ForeignKey): Physical location reference
    
    Business Logic:
        - SET_NULL preserves company record if address is deleted
        - Many-to-many users allows multiple staff access
        - Name is required for identification
    """
    users = models.ManyToManyField('auth.User')
    name = models.CharField(max_length=120, null=False, blank=False) # max_length is required for CharField
    address = models.ForeignKey('customer.Address', null=True, on_delete=models.SET_NULL) # SET_NULL we will persist company data even if we don't have an address

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        """Simple name-based identification."""
        return self.name


class SupplyChainCompany(models.Model):
    """
    Supply chain partner or vendor entity.
    
    Tracks external companies in the supply chain with validation status
    to distinguish between approved and unapproved partners.
    
    Attributes:
        name (str): Company name
        is_valid (bool): Approval status for supply chain operations
        address (ForeignKey): Business location
    
    Usage:
        - Use is_valid to filter approved supply chain partners
        - SET_NULL maintains partner record if address is removed
        - Required name ensures partner identification
    """
    name = models.CharField(max_length=120, null=False, blank=False)
    is_valid = models.BooleanField(default=False)
    address = models.ForeignKey('customer.Address', null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = "Supply Chain Companies"

    def __str__(self):
        """Name-based representation with validation hint."""
        return f"{self.name} {'✓' if self.is_valid else '✗'}"


class CertificationBody(models.Model):
    """
    Certification or standards organization.
    
    Represents entities that provide certifications, audits, or
    compliance verification for companies and supply chain partners.
    
    Attributes:
        name (str): Certification body name
        address (ForeignKey): Official business address
    
    Examples:
        - ISO certification bodies
        - Industry-specific audit organizations
        - Regulatory compliance agencies
    """
    name = models.CharField(max_length=120, null=False, blank=False)
    address = models.ForeignKey('customer.Address', null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = "Certification Bodies"

    def __str__(self):
        """Name-based identification."""
        return self.name
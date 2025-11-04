from django.db import models

class Address(models.Model):
    """
    Comprehensive geographical address model.
    
    Stores complete address information that can be reused across
    multiple entities (companies, supply chain partners, etc.).
    """
    address = models.CharField(
        max_length=120, 
        null=False, 
        blank=False,
        help_text="Street address line 1 (Required)."
    )
    city = models.CharField(
        max_length=120, 
        null=False, 
        blank=False,
        help_text="City or town name (Required)."
    )
    state = models.CharField(
        max_length=120, 
        null=False, 
        blank=False,
        help_text="State, province, or region (Required)."
    )
    zip_code = models.CharField(
        max_length=120, 
        null=False, 
        blank=False,
        help_text="Postal code or ZIP code (Required)."
    )
    country = models.CharField(
        max_length=120, 
        null=False, 
        blank=False,
        help_text="Country name (Required)."
    )
    
    class Meta: 
        verbose_name_plural = "Addresses" 
    def __str__(self):
        """Human-readable representation of the full address."""
        return f'{self.address}, {self.city}, {self.state}, {self.country}'


class Company(models.Model):
    """
    Primary company entity with user access control.
    
    Represents a business organization that can have multiple users
    associated with it. Maintains company data even if address is removed.
    """
    users = models.ManyToManyField(
        'auth.User',
        help_text="Django users who have access permissions for this company's data."
    )
    name = models.CharField(
        max_length=120, 
        null=False, 
        blank=False,
        help_text="The official legal name of the company."
    )
    address = models.ForeignKey(
        'customer.Address', 
        null=True, 
        on_delete=models.SET_NULL,
        help_text="The primary physical address of the company."
    )

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
    """
    name = models.CharField(
        max_length=120, 
        null=False, 
        blank=False,
        help_text="The legal name of the supply chain partner."
    )
    is_valid = models.BooleanField(
        default=False,
        help_text="Check if this partner has been approved and validated for certification processes."
    )
    address = models.ForeignKey(
        'customer.Address', 
        null=True, 
        on_delete=models.SET_NULL,
        help_text="The business location of the supply chain partner."
    )

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
    """
    name = models.CharField(
        max_length=120, 
        null=False, 
        blank=False,
        help_text="The full name of the certification or standards organization."
    )
    address = models.ForeignKey(
        'customer.Address', 
        null=True, 
        on_delete=models.SET_NULL,
        help_text="The official business address of the certification body."
    )

    class Meta:
        verbose_name_plural = "Certification Bodies"

    def __str__(self):
        """Name-based identification."""
        return self.name
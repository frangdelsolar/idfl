from django.db import models
import uuid
import os

# Constants
APPLICATION_FOLDER = 'application_files'

def application_file_path(instance, filename):
    """
    Generate a unique file path for application files.
    """
    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4().hex}.{ext}"
    subdirectory = APPLICATION_FOLDER
    return os.path.join('data', subdirectory, unique_filename)


class Application(models.Model):
    """Represents an application submission."""
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_REVIEW = 'in_review', 'In Review'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
    
    name = models.CharField(max_length=120)
    description = models.TextField()
    submission_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=120, choices=Status.choices, default=Status.PENDING)
    file = models.FileField(upload_to=application_file_path, blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.status}"
    
    class Meta:
        ordering = ['-submission_date'] 


class ApplicationCompanyInfo(models.Model):
    """Staging model for the applicant company."""
    application = models.OneToOneField(
        'application.Application',
        on_delete=models.CASCADE,
        related_name='company_info',
        null=False, blank=False
    )
    
    name = models.CharField(max_length=120, null=True, blank=True)
    address = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120, null=True, blank=True)
    state = models.CharField(max_length=120, null=True, blank=True)
    zip_code = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=120, null=True, blank=True)

    is_approved = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Application Company Info (Staging)"
        verbose_name_plural = "Application Company Info (Staging)"

    def __str__(self):
        app_name = getattr(self.application, 'name', 'N/A')
        return f"Info for Application: {app_name} ({self.name})"
    

class ApplicationSupplyChainPartner(models.Model):
    """Staging model for a supply chain partner."""
    application = models.ForeignKey(
        'application.Application',
        on_delete=models.CASCADE,
        related_name='supply_chain_partners',
        null=False, blank=False
    )

    name = models.CharField(max_length=120, null=True, blank=True)
    address = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120, null=True, blank=True)
    state = models.CharField(max_length=120, null=True, blank=True)
    zip_code = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=120, null=True, blank=True)
    
    is_approved = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Application Supply Chain Partner (Staging)"
        verbose_name_plural = "Application Supply Chain Partners (Staging)"

    def __str__(self):
        app_name = getattr(self.application, 'name', 'N/A')
        return f"Partner: {self.name} for App: {app_name}"
    
    
class ApplicationProduct(models.Model):
    """Staging model for a product submitted by a supply chain partner."""
    application = models.ForeignKey(
        'application.Application',
        on_delete=models.CASCADE,
        related_name='products', 
        null=False, blank=False
    )
    
    supply_chain_partner_name_raw = models.CharField(
        max_length=120, 
        null=True, 
        blank=True
    )

    product_name = models.CharField(max_length=120, null=True, blank=True)
    product_category = models.CharField(max_length=120, null=True, blank=True)
    raw_materials_list = models.TextField(
        null=True, 
        blank=True
    )
    
    is_approved = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Application Product (Staging)"
        verbose_name_plural = "Application Products (Staging)"

    def __str__(self):
        app_name = getattr(self.application, 'name', 'N/A')
        partner_name = self.supply_chain_partner_name_raw or 'Unspecified Partner'
        return f"Product: {self.product_name} by {partner_name} for App: {app_name}"
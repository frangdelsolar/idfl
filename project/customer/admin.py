from django.contrib import admin
from .models import (
    Address, 
    Company, 
    SupplyChainCompany, 
    CertificationBody
)

# We register our models to make them available in django admin site
admin.site.register(Address)
admin.site.register(Company)
admin.site.register(SupplyChainCompany)
admin.site.register(CertificationBody)
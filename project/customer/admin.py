from django.contrib import admin
from .models import (
    Address, 
    Company, 
    SupplyChainCompany, 
    CertificationBody
)

admin.site.register(Address)
admin.site.register(Company)
admin.site.register(SupplyChainCompany)
admin.site.register(CertificationBody)
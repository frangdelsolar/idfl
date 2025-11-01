from django.contrib import admin
from .models import (
    Application, 
    ApplicationCompanyInfo,
    ApplicationSupplyChainPartner,
    ApplicationProduct
)


class ApplicationCompanyInfoInline(admin.StackedInline):
    """Inline for applicant company information."""
    model = ApplicationCompanyInfo
    can_delete = False
    max_num = 1
    fields = [
        'name', 'address', 'city', 'state', 'zip_code', 
        'country', 'is_approved', 'rejection_reason'
    ]
    classes = ['collapse']


class ApplicationSupplyChainPartnerInline(admin.StackedInline):
    """Inline for supply chain partner information."""
    model = ApplicationSupplyChainPartner
    extra = 1
    fieldsets = (
        ('Partner Details', {
            'fields': ('name', 'address', 'city', 'state', 'zip_code', 'country'),
            'classes': ['collapse']
        }),
        ('Review Status', {
            'fields': ('is_approved', 'rejection_reason'),
            'classes': ['collapse']
        })
    )
    classes = ['collapse']


class ApplicationProductInline(admin.StackedInline):
    """Inline for product information and composition."""
    model = ApplicationProduct
    extra = 1
    fieldsets = (
        ('Product Information', {
            'fields': (
                'supply_chain_partner_name_raw',
                'product_name', 
                'product_category'
            ),
            'classes': ['collapse']
        }),
        ('Raw Materials', {
            'fields': ('raw_materials_list',),
            'classes': ['collapse']
        }),
        ('Review Status', {
            'fields': (('is_approved', 'rejection_reason'),),
            'classes': ['collapse']
        })
    )
    classes = ['collapse']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """Admin interface for managing applications."""
    
    list_display = ('name', 'status', 'submission_date')
    list_filter = ('status',)
    search_fields = ('name',)
    readonly_fields = ('submission_date',)
    
    fieldsets = (
        ('Application Details', {
            'fields': ('name', 'description', 'file'),
            'classes': ['collapse']
        }),
        ('Review Status', {
            'fields': ('status', 'rejection_reason'),
            'classes': ['collapse']
        }),
    )

    inlines = [
        ApplicationCompanyInfoInline,
        ApplicationSupplyChainPartnerInline,
        ApplicationProductInline,
    ]
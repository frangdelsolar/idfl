from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from .models import (
    Application, 
    ApplicationCompanyInfo,
    ApplicationSupplyChainPartner,
    ApplicationProduct
)

from application import utils


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
        }),
        ('Review Status', {
            'fields': ('is_approved', 'rejection_reason'),
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
        }),
        ('Raw Materials', {
            'fields': ('raw_materials_list',),
        }),
        ('Review Status', {
            'fields': (('is_approved', 'rejection_reason'),),
        })
    )
    classes = ['collapse']


class ApplicationAdmin(admin.ModelAdmin):
    """Admin interface for managing applications."""
    
    list_display = ('name', 'status', 'submission_date', 'completion_actions', 'download_actions')
    list_filter = ('status',)
    search_fields = ('name',)
    readonly_fields = ('submission_date',)
    
    fieldsets = (
        ('Application Details', {
            'fields': ('name', 'description', 'file'),
        }),
        ('Review Status', {
            'fields': ('status', 'rejection_reason'),
        }),
    )

    inlines = [
        ApplicationCompanyInfoInline,
        ApplicationSupplyChainPartnerInline,
        ApplicationProductInline,
    ]

    def completion_actions(self, obj):
        """Display completion action buttons in list view."""
        if obj.status == 'rejected':
            return format_html('<span style="color: red;">✗ Rejected</span>')
        
        elif obj.status != 'completed':
            return format_html(
                '<a class="button" href="{}">Complete Application</a>',
                reverse('admin:application_application_complete', args=[obj.pk])
            )

        return format_html('<span style="color: green;">✓ Completed</span>')
    
    completion_actions.short_description = 'Actions'

    def download_actions(self, obj):
        """Display PDF download button in list view."""
        if obj.status == 'completed':
            return format_html(
                '<a class="button" href="{}" style="background: #ff6b35;">📄 Download PDF</a>',
                reverse('admin:application_application_download_pdf', args=[obj.pk])
            )

        return format_html('<span style="color: #ccc;">Not available</span>')
    
    download_actions.short_description = 'Certificate'

    def get_urls(self):
        """Add custom URLs for completion and download actions."""
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/complete/',
                self.admin_site.admin_view(self.complete_application),
                name='application_application_complete',
            ),
            path(
                '<path:object_id>/download-pdf/',
                self.admin_site.admin_view(self.download_pdf),
                name='application_application_download_pdf',
            ),
        ]
        return custom_urls + urls

    def complete_application(self, request, object_id):
        """Handle application completion from list view."""
        obj = self.get_object(request, object_id)  
        if obj:
            success = utils.complete_application(application=obj)
            if not success:
                self.message_user(
                    request, 
                    f"Failed to mark application '{obj.name}' as completed", 
                    level='ERROR'
                )
            else:
                self.message_user(request, f"Application '{obj.name}' marked as completed")
        
        return HttpResponseRedirect(reverse('admin:application_application_changelist'))

    def download_pdf(self, request, object_id):
        """Handle PDF certificate download."""
        obj = self.get_object(request, object_id)
        if obj:
            success = utils.generate_pdf_certificate(obj)
            if not success:
                self.message_user(
                    request, 
                    f"Failed to generate PDF for '{obj.name}'", 
                    level='ERROR'
                )
            else:
                self.message_user(request, f"PDF download triggered for '{obj.name}' - add your logic here")
        
        return HttpResponseRedirect(reverse('admin:application_application_changelist'))




admin.site.register(Application, ApplicationAdmin)
admin.site.register(ApplicationCompanyInfo)
admin.site.register(ApplicationSupplyChainPartner)
admin.site.register(ApplicationProduct)
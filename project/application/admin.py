from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from .models import (
    Application, 
    ApplicationCompanyInfo,
    ApplicationSupplyChainPartner,
    ApplicationProduct,
    BulkSubmission
)
from application import utils


class ApplicationCompanyInfoInline(admin.StackedInline):
    """
    Inline admin for company information with role-based field permissions.
    Customer Service can edit company details but not approval status.
    Reviewer can only edit approval status when application is in review.
    """
    model = ApplicationCompanyInfo
    can_delete = False
    max_num = 1
    fieldsets = (
        ('Company Information', {
            'fields': (
                'name',
                ('address', 'city'),
                ('state', 'zip_code'), 
                'country'
            ),
            'classes': ('collapse',),
        }),
        ('Review Status', {
            'fields': (
                'is_approved',
                'rejection_reason',
            ),
            'classes': ('collapse',),
        })
    )
    classes = ['collapse']

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj) or [])
        
        if request.user.groups.filter(name='Customer Service').exists():
            readonly_fields.extend(['is_approved', 'rejection_reason'])
        elif request.user.groups.filter(name='Reviewer').exists():
            readonly_fields.extend(['name', 'address', 'city', 'state', 'zip_code', 'country'])
        
        return readonly_fields


class ApplicationSupplyChainPartnerInline(admin.StackedInline):
    """
    Inline admin for supply chain partners with role-based permissions.
    Follows same permission pattern as company info inline.
    """
    model = ApplicationSupplyChainPartner
    fieldsets = (
        ('Partner Information', {
            'fields': (
                'name',
                ('address', 'city'),
                ('state', 'zip_code'),
                'country'
            ),
            'classes': ('collapse',),
        }),
        ('Review Status', {
            'fields': (
                'is_approved',
                'rejection_reason',
            ),
            'classes': ('collapse',),
        })
    )
    classes = ['collapse']

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj) or [])
        
        if request.user.groups.filter(name='Customer Service').exists():
            readonly_fields.extend(['is_approved', 'rejection_reason'])
        elif request.user.groups.filter(name='Reviewer').exists():
            readonly_fields.extend(['name', 'address', 'city', 'state', 'zip_code', 'country'])
        
        return readonly_fields


class ApplicationProductInline(admin.StackedInline):
    """
    Inline admin for product information and composition details.
    Customer Service can edit product details but not approval decisions.
    Reviewer can only approve/reject products when application is in review.
    """
    model = ApplicationProduct
    fieldsets = (
        ('Product Information', {
            'fields': (
                'supply_chain_partner_name_raw',
                'product_name', 
                'product_category'
            ),
            'classes': ('collapse',),
        }),
        ('Composition Details', {
            'fields': (
                'raw_materials_list',
            ),
            'classes': ('collapse',),
        }),
        ('Review Status', {
            'fields': (
                'is_approved',
                'rejection_reason',
            ),
            'classes': ('collapse',),
        })
    )
    classes = ['collapse']

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj) or [])
        
        if request.user.groups.filter(name='Customer Service').exists():
            readonly_fields.extend(['is_approved', 'rejection_reason'])
        elif request.user.groups.filter(name='Reviewer').exists():
            readonly_fields.extend(['supply_chain_partner_name_raw', 'product_name', 'product_category', 'raw_materials_list'])
        
        return readonly_fields


class ApplicationAdmin(admin.ModelAdmin):
    """
    Custom admin interface for managing sustainability certification applications.
    Provides role-based workflows for Customer Service and Reviewer groups.
    """
    list_display = ('name', 'status', 'submission_date', 'submission_actions', 'completion_actions', 'download_actions')
    list_filter = ('status',)
    search_fields = ('name',)
    readonly_fields = ('submission_date',)
    
    fieldsets = (
        ('Application Details', {
            'fields': (
                'name',
                'description', 
                'file'
            ),
            'classes': ('collapse',),
        }),
        ('Review Status', {
            'fields': (
                'status',
                'rejection_reason',
            ),
            'classes': ('collapse',),
        })
    )

    inlines = [
        ApplicationCompanyInfoInline,
        ApplicationSupplyChainPartnerInline,
        ApplicationProductInline,
    ]

    def get_readonly_fields(self, request, obj=None):
        """Apply role-based field permissions for main application model."""
        readonly_fields = list(super().get_readonly_fields(request, obj) or [])
        
        if request.user.groups.filter(name='Customer Service').exists():
            readonly_fields.extend(['status', 'rejection_reason'])
        elif request.user.groups.filter(name='Reviewer').exists():
            readonly_fields.extend(['name', 'description', 'file', 'status'])
        
        return readonly_fields

    def get_inline_instances(self, request, obj=None):
        """Apply role-based permissions to inline instances dynamically."""
        inline_instances = []
        for inline_class in self.inlines:
            inline = inline_class(self.model, self.admin_site)
            
            if obj:
                if request.user.groups.filter(name='Customer Service').exists():
                    if hasattr(inline, 'readonly_fields'):
                        inline.readonly_fields = list(inline.readonly_fields) + ['is_approved', 'rejection_reason']
                    else:
                        inline.readonly_fields = ['is_approved', 'rejection_reason']
                elif request.user.groups.filter(name='Reviewer').exists():
                    if obj.status != 'in_review':
                        if hasattr(inline, 'readonly_fields'):
                            inline.readonly_fields = list(inline.readonly_fields) + ['is_approved', 'rejection_reason']
                        else:
                            inline.readonly_fields = ['is_approved', 'rejection_reason']
            
            inline_instances.append(inline)
        
        return inline_instances

    def submission_actions(self, obj):
        """Display submit button for Customer Service on pending applications."""
        if (obj.status == 'pending' and 
            hasattr(self, 'request') and 
            self.request.user.groups.filter(name='Customer Service').exists()):
            return format_html(
                '<a class="button" href="{}" style="background: #4CAF50;">Submit Application</a>',
                reverse('admin:application_application_submit', args=[obj.pk])
            )
        return format_html('<span style="color: #ccc;">-</span>')
    
    submission_actions.short_description = 'Submit'

    def completion_actions(self, obj):
        """Display complete/reject actions for Reviewer and show final status."""
        if (obj.status == 'in_review' and 
            hasattr(self, 'request') and 
            self.request.user.groups.filter(name='Reviewer').exists()):
            return format_html(
                '<a class="button" href="{}">Complete Application</a>',
                reverse('admin:application_application_complete', args=[obj.pk])
            )
        elif obj.status == 'rejected':
            return format_html('<span style="color: red;">✗ Rejected</span>')
        elif obj.status == 'completed':
            return format_html('<span style="color: green;">✓ Completed</span>')
        
        return format_html('<span style="color: #ccc;">-</span>')
    
    completion_actions.short_description = 'Complete'

    def download_actions(self, obj):
        """Display PDF certificate download button for completed applications."""
        if obj.status == 'completed' or obj.status == 'rejected':
            return format_html(
                '<a class="button" href="{}" style="background: #ff6b35;">📄 Download PDF</a>',
                reverse('admin:application_application_download_pdf', args=[obj.pk])
            )
        return format_html('<span style="color: #ccc;">Not available</span>')
    
    download_actions.short_description = 'Certificate'

    def changelist_view(self, request, extra_context=None):
        """Store request object for use in list display action methods."""
        self.request = request
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        """Add custom URLs for application workflow actions."""
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/submit/',
                self.admin_site.admin_view(self.submit_application),
                name='application_application_submit',
            ),
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

    def submit_application(self, request, object_id):
        """Handle application submission - moves from pending to in_review status."""
        if not request.user.groups.filter(name='Customer Service').exists():
            self.message_user(request, "You don't have permission to submit applications", level='ERROR')
            return HttpResponseRedirect(reverse('admin:application_application_changelist'))
        
        obj = self.get_object(request, object_id)  
        if obj and obj.status == 'pending':
            obj.status = 'in_review'
            obj.submission_date = timezone.now()
            obj.save()
            self.message_user(request, f"Application '{obj.name}' submitted for review")
        else:
            self.message_user(request, "Application cannot be submitted", level='ERROR')
        
        return HttpResponseRedirect(reverse('admin:application_application_changelist'))

    def complete_application(self, request, object_id):
        """
        Handle application completion - approves or rejects based on component approvals.
        Application is completed only if all company info, partners, and products are approved.
        """
        if not request.user.groups.filter(name='Reviewer').exists():
            self.message_user(request, "You don't have permission to complete applications", level='ERROR')
            return HttpResponseRedirect(reverse('admin:application_application_changelist'))
        
        obj = self.get_object(request, object_id)  
        if obj and obj.status == 'in_review':
            all_approved = (
                obj.company_info.is_approved and
                obj.supply_chain_partners.filter(is_approved=False).count() == 0 and
                obj.products.filter(is_approved=False).count() == 0
            )
            
            if all_approved:
                success = utils.complete_application(obj)
                if not success:
                    self.message_user(
                        request, 
                        f"Application '{obj.name}' approved but failed to create permanent records. Please try again.", 
                        level='ERROR'
                    )
                    return HttpResponseRedirect(reverse('admin:application_application_changelist'))
                
                obj.status = 'completed'
                self.message_user(request, f"Application '{obj.name}' approved and completed")
            else:
                obj.status = 'rejected'
                self.message_user(request, f"Application '{obj.name}' rejected - not all components approved", level='WARNING')
            
            obj.save()
        else:
            self.message_user(request, "Application cannot be completed", level='ERROR')
        
        return HttpResponseRedirect(reverse('admin:application_application_changelist'))

    def download_pdf(self, request, object_id):
        """Handle PDF certificate generation and download for completed applications."""
        obj = self.get_object(request, object_id)
        if obj and (obj.status == 'completed' or obj.status == 'rejected'):
            pdf_content = utils.generate_pdf_certificate(obj)
            if pdf_content:
                response = HttpResponse(pdf_content, content_type='application/pdf')
                filename = f"sustainability_certificate_{obj.name.replace(' ', '_')}.pdf"
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                
                return response
            else:
                self.message_user(
                    request, 
                    f"Failed to generate PDF for '{obj.name}'", 
                    level='ERROR'
                )
        else:
            self.message_user(request, "Certificate only available for completed or rejected applications", level='ERROR')
        
        return HttpResponseRedirect(reverse('admin:application_application_changelist'))

    def has_change_permission(self, request, obj=None):
        """
        Control edit permissions based on user role and application status.
        Customer Service can only edit pending applications.
        Reviewer can only edit applications in review.
        """
        if obj:
            if (request.user.groups.filter(name='Customer Service').exists() and 
                obj.status != 'pending'):
                return False
            
            if (request.user.groups.filter(name='Reviewer').exists() and 
                obj.status != 'in_review'):
                return False
        
        return super().has_change_permission(request, obj)
    
    def save_model(self, request, obj, form, change):
        """
        Detect when a file is uploaded and trigger Excel processing
        """
        file_uploaded = 'file' in form.changed_data and obj.file

        super().save_model(request, obj, form, change)
        
        if file_uploaded and obj.file:
            try:
                utils.process_xlsx_application_form(obj)
            except Exception as e:
                self.message_user(request, f"Failed to process Excel file for application: {obj.name}. Error: {e}", level='ERROR')

        return obj
    
class ApplicationInline(admin.StackedInline):
    model = Application
    extra = 1
    readonly_fields = ['submission_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'file')
        }),
        ('Status', {
            'fields': ('status', 'submission_date'),
            'classes': ('collapse',)
        })
    )

class BulkSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ApplicationInline]
    
    fieldsets = (
        ('Submission Details', {
            'fields': ('name', 'description')
        }),
        ('Status & Timing', {
            'fields': ('status', ('created_at', 'updated_at'))
        }),
        ('Errors', {
            'fields': ('error_message', 'error_details'),
            'classes': ('collapse',)
        })
    )

    def get_readonly_fields(self, request, obj=None):
        """Apply role-based field permissions"""
        readonly_fields = list(super().get_readonly_fields(request, obj) or [])
        
        if request.user.groups.filter(name='Reviewer').exists():
            # Reviewer can only read, not edit
            readonly_fields.extend(['name', 'description', 'status', 'error_message', 'error_details'])
        elif request.user.groups.filter(name='Customer Service').exists():
            # Customer Service can only edit when status is DRAFT
            if obj and obj.status != BulkSubmission.Status.DRAFT:
                readonly_fields.extend(['name', 'description', 'status', 'error_message', 'error_details'])
        
        return readonly_fields

    def get_inline_instances(self, request, obj=None):
        """Apply role-based permissions to inline instances"""
        inline_instances = []
        for inline_class in self.inlines:
            inline = inline_class(self.model, self.admin_site)
            
            if request.user.groups.filter(name='Reviewer').exists():
                # Reviewer - read only
                inline.readonly_fields = list(getattr(inline, 'readonly_fields', [])) + [
                    'name', 'description', 'file', 'status', 'submission_date'
                ]
                inline.can_delete = False
                inline.max_num = 0
            elif request.user.groups.filter(name='Customer Service').exists():
                # Customer Service - only editable when status is DRAFT
                if obj and obj.status != BulkSubmission.Status.DRAFT:
                    inline.readonly_fields = list(getattr(inline, 'readonly_fields', [])) + [
                        'name', 'description', 'file', 'status', 'submission_date'
                    ]
                    inline.can_delete = False
                    inline.max_num = 0
            
            inline_instances.append(inline)
        
        return inline_instances

    def has_change_permission(self, request, obj=None):
        """Role-based change permissions"""
        if request.user.groups.filter(name='Reviewer').exists():
            return False
        
        if (request.user.groups.filter(name='Customer Service').exists() and 
            obj and obj.status != BulkSubmission.Status.DRAFT):
            return False
            
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request):
        """Role-based add permissions"""
        if request.user.groups.filter(name='Reviewer').exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        """Role-based delete permissions"""
        if request.user.groups.filter(name='Reviewer').exists():
            return False
        
        if (request.user.groups.filter(name='Customer Service').exists() and 
            obj and obj.status != BulkSubmission.Status.DRAFT):
            return False
            
        return super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        """
        Custom save logic for BulkSubmission
        """
        super().save_model(request, obj, form, change)
        
        obj.status = BulkSubmission.Status.PROCESSING
        obj.save()
        
        utils.process_bulk_submission_async(obj.id)


# Register models with custom admin interface
admin.site.register(Application, ApplicationAdmin)
admin.site.register(ApplicationCompanyInfo)
admin.site.register(ApplicationSupplyChainPartner)
admin.site.register(ApplicationProduct)
admin.site.register(BulkSubmission, BulkSubmissionAdmin)



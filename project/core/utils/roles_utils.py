from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from application.models import (
    Application, 
    ApplicationCompanyInfo,
    ApplicationSupplyChainPartner,
    ApplicationProduct
)

def setup_customer_service_role():
    """
    Setup Customer Service role with appropriate permissions.
    
    Creates Customer Service group with permissions to:
    - All basic CRU (Create, Read, Update) permissions for application models
    - No delete permissions
    
    Returns:
        Group: Customer Service group object
    """
    # Create Customer Service role
    customer_service_group, created = Group.objects.get_or_create(name='Customer Service')
    
    # Get content types for all models
    app_content_type = ContentType.objects.get_for_model(Application)
    company_info_content_type = ContentType.objects.get_for_model(ApplicationCompanyInfo)
    partner_content_type = ContentType.objects.get_for_model(ApplicationSupplyChainPartner)
    product_content_type = ContentType.objects.get_for_model(ApplicationProduct)
    
    # Application permissions (no delete)
    app_add_perm = Permission.objects.get(codename='add_application', content_type=app_content_type)
    app_change_perm = Permission.objects.get(codename='change_application', content_type=app_content_type)
    app_view_perm = Permission.objects.get(codename='view_application', content_type=app_content_type)
    
    # ApplicationCompanyInfo permissions (no delete)
    company_info_add_perm = Permission.objects.get(codename='add_applicationcompanyinfo', content_type=company_info_content_type)
    company_info_change_perm = Permission.objects.get(codename='change_applicationcompanyinfo', content_type=company_info_content_type)
    company_info_view_perm = Permission.objects.get(codename='view_applicationcompanyinfo', content_type=company_info_content_type)
    
    # ApplicationSupplyChainPartner permissions (no delete)
    partner_add_perm = Permission.objects.get(codename='add_applicationsupplychainpartner', content_type=partner_content_type)
    partner_change_perm = Permission.objects.get(codename='change_applicationsupplychainpartner', content_type=partner_content_type)
    partner_view_perm = Permission.objects.get(codename='view_applicationsupplychainpartner', content_type=partner_content_type)
    
    # ApplicationProduct permissions (no delete)
    product_add_perm = Permission.objects.get(codename='add_applicationproduct', content_type=product_content_type)
    product_change_perm = Permission.objects.get(codename='change_applicationproduct', content_type=product_content_type)
    product_view_perm = Permission.objects.get(codename='view_applicationproduct', content_type=product_content_type)
    
    # Assign all permissions to group (no delete permissions)
    all_permissions = [
        app_add_perm, app_change_perm, app_view_perm,
        company_info_add_perm, company_info_change_perm, company_info_view_perm,
        partner_add_perm, partner_change_perm, partner_view_perm,
        product_add_perm, product_change_perm, product_view_perm
    ]
    
    customer_service_group.permissions.add(*all_permissions)
    
    return customer_service_group

def setup_reviewer_role():
    """
    Setup Reviewer role with appropriate permissions.
    
    Creates Reviewer group with permissions to:
    - All CRUD (Create, Read, Update, Delete) permissions for application models
    
    Returns:
        Group: Reviewer group object
    """
    # Create Reviewer role  
    reviewer_group, created = Group.objects.get_or_create(name='Reviewer')
    
    # Get content types for all models
    app_content_type = ContentType.objects.get_for_model(Application)
    company_info_content_type = ContentType.objects.get_for_model(ApplicationCompanyInfo)
    partner_content_type = ContentType.objects.get_for_model(ApplicationSupplyChainPartner)
    product_content_type = ContentType.objects.get_for_model(ApplicationProduct)
    
    # Application permissions (full CRUD)
    app_add_perm = Permission.objects.get(codename='add_application', content_type=app_content_type)
    app_change_perm = Permission.objects.get(codename='change_application', content_type=app_content_type)
    app_view_perm = Permission.objects.get(codename='view_application', content_type=app_content_type)
    app_delete_perm = Permission.objects.get(codename='delete_application', content_type=app_content_type)
    
    # ApplicationCompanyInfo permissions (full CRUD)
    company_info_add_perm = Permission.objects.get(codename='add_applicationcompanyinfo', content_type=company_info_content_type)
    company_info_change_perm = Permission.objects.get(codename='change_applicationcompanyinfo', content_type=company_info_content_type)
    company_info_view_perm = Permission.objects.get(codename='view_applicationcompanyinfo', content_type=company_info_content_type)
    company_info_delete_perm = Permission.objects.get(codename='delete_applicationcompanyinfo', content_type=company_info_content_type)
    
    # ApplicationSupplyChainPartner permissions (full CRUD)
    partner_add_perm = Permission.objects.get(codename='add_applicationsupplychainpartner', content_type=partner_content_type)
    partner_change_perm = Permission.objects.get(codename='change_applicationsupplychainpartner', content_type=partner_content_type)
    partner_view_perm = Permission.objects.get(codename='view_applicationsupplychainpartner', content_type=partner_content_type)
    partner_delete_perm = Permission.objects.get(codename='delete_applicationsupplychainpartner', content_type=partner_content_type)
    
    # ApplicationProduct permissions (full CRUD)
    product_add_perm = Permission.objects.get(codename='add_applicationproduct', content_type=product_content_type)
    product_change_perm = Permission.objects.get(codename='change_applicationproduct', content_type=product_content_type)
    product_view_perm = Permission.objects.get(codename='view_applicationproduct', content_type=product_content_type)
    product_delete_perm = Permission.objects.get(codename='delete_applicationproduct', content_type=product_content_type)
    
    # Assign all permissions to group (including delete)
    all_permissions = [
        app_add_perm, app_change_perm, app_view_perm, app_delete_perm,
        company_info_add_perm, company_info_change_perm, company_info_view_perm, company_info_delete_perm,
        partner_add_perm, partner_change_perm, partner_view_perm, partner_delete_perm,
        product_add_perm, product_change_perm, product_view_perm, product_delete_perm
    ]
    
    reviewer_group.permissions.add(*all_permissions)
    
    return reviewer_group

def setup_roles():
    """
    Setup both Customer Service and Reviewer roles with appropriate permissions.
    
    Convenience function that calls both individual role setup functions.
    
    Returns:
        tuple: (customer_service_group, reviewer_group) Group objects
    """
    customer_service_group = setup_customer_service_role()
    reviewer_group = setup_reviewer_role()
    
    return customer_service_group, reviewer_group
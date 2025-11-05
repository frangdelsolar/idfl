from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from application.models import (
    Application, 
    ApplicationCompanyInfo,
    ApplicationSupplyChainPartner,
    ApplicationProduct,
    BulkSubmission
)
from customer.models import CustomerProfile  # Import CustomerProfile model

def setup_customer_role():
    """
    Setup Customer role with appropriate permissions.
    
    Creates Customer group with permissions to:
    - Create and view their own applications
    - Update their own applications (before submission/approval)
    - Create and manage application-related data (company info, partners, products)
    - View and update their own customer profile
    - No delete permissions for applications or profiles
    - No access to BulkSubmission
    
    Returns:
        Group: Customer group object
    """
    # Create Customer role
    customer_group, created = Group.objects.get_or_create(name='Customer')
    
    # Get content types for application models
    app_content_type = ContentType.objects.get_for_model(Application)
    company_info_content_type = ContentType.objects.get_for_model(ApplicationCompanyInfo)
    partner_content_type = ContentType.objects.get_for_model(ApplicationSupplyChainPartner)
    product_content_type = ContentType.objects.get_for_model(ApplicationProduct)
    customer_profile_content_type = ContentType.objects.get_for_model(CustomerProfile)
    
    # Application permissions (Create, Read, Update - no Delete)
    app_add_perm = Permission.objects.get(codename='add_application', content_type=app_content_type)
    app_change_perm = Permission.objects.get(codename='change_application', content_type=app_content_type)
    app_view_perm = Permission.objects.get(codename='view_application', content_type=app_content_type)
    
    # ApplicationCompanyInfo permissions (Create, Read, Update - no Delete)
    company_info_add_perm = Permission.objects.get(codename='add_applicationcompanyinfo', content_type=company_info_content_type)
    company_info_change_perm = Permission.objects.get(codename='change_applicationcompanyinfo', content_type=company_info_content_type)
    company_info_view_perm = Permission.objects.get(codename='view_applicationcompanyinfo', content_type=company_info_content_type)
    
    # ApplicationSupplyChainPartner permissions (Create, Read, Update - no Delete)
    partner_add_perm = Permission.objects.get(codename='add_applicationsupplychainpartner', content_type=partner_content_type)
    partner_change_perm = Permission.objects.get(codename='change_applicationsupplychainpartner', content_type=partner_content_type)
    partner_view_perm = Permission.objects.get(codename='view_applicationsupplychainpartner', content_type=partner_content_type)
    
    # ApplicationProduct permissions (Create, Read, Update - no Delete)
    product_add_perm = Permission.objects.get(codename='add_applicationproduct', content_type=product_content_type)
    product_change_perm = Permission.objects.get(codename='change_applicationproduct', content_type=product_content_type)
    product_view_perm = Permission.objects.get(codename='view_applicationproduct', content_type=product_content_type)
    
    # CustomerProfile permissions (Read, Update - no Create/Delete for own profile)
    customer_profile_change_perm = Permission.objects.get(codename='change_customerprofile', content_type=customer_profile_content_type)
    customer_profile_view_perm = Permission.objects.get(codename='view_customerprofile', content_type=customer_profile_content_type)
    
    # Assign permissions to group (CRU - no Delete, no BulkSubmission access)
    customer_permissions = [
        app_add_perm, app_change_perm, app_view_perm,
        company_info_add_perm, company_info_change_perm, company_info_view_perm,
        partner_add_perm, partner_change_perm, partner_view_perm,
        product_add_perm, product_change_perm, product_view_perm,
        customer_profile_change_perm, customer_profile_view_perm,  # Customer can view and update their own profile
    ]
    
    customer_group.permissions.add(*customer_permissions)
    
    return customer_group

def setup_customer_service_role():
    """
    Setup Customer Service role with appropriate permissions.
    
    Creates Customer Service group with permissions to:
    - All basic CRU (Create, Read, Update) permissions for application models
    - CRU permissions for BulkSubmission (no delete)
    - Full CRUD permissions for CustomerProfile (can manage customer profiles)
    
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
    bulk_submission_content_type = ContentType.objects.get_for_model(BulkSubmission)
    customer_profile_content_type = ContentType.objects.get_for_model(CustomerProfile)
    
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
    
    # BulkSubmission permissions (CRU - no delete)
    bulk_add_perm = Permission.objects.get(codename='add_bulksubmission', content_type=bulk_submission_content_type)
    bulk_change_perm = Permission.objects.get(codename='change_bulksubmission', content_type=bulk_submission_content_type)
    bulk_view_perm = Permission.objects.get(codename='view_bulksubmission', content_type=bulk_submission_content_type)
    
    # CustomerProfile permissions (Full CRUD - can manage all customer profiles)
    customer_profile_add_perm = Permission.objects.get(codename='add_customerprofile', content_type=customer_profile_content_type)
    customer_profile_change_perm = Permission.objects.get(codename='change_customerprofile', content_type=customer_profile_content_type)
    customer_profile_view_perm = Permission.objects.get(codename='view_customerprofile', content_type=customer_profile_content_type)
    customer_profile_delete_perm = Permission.objects.get(codename='delete_customerprofile', content_type=customer_profile_content_type)
    
    # Assign all permissions to group (no delete for most, but full CRUD for CustomerProfile)
    all_permissions = [
        app_add_perm, app_change_perm, app_view_perm,
        company_info_add_perm, company_info_change_perm, company_info_view_perm,
        partner_add_perm, partner_change_perm, partner_view_perm,
        product_add_perm, product_change_perm, product_view_perm,
        bulk_add_perm, bulk_change_perm, bulk_view_perm,
        customer_profile_add_perm, customer_profile_change_perm, customer_profile_view_perm, customer_profile_delete_perm,  # Full CRUD for CustomerProfile
    ]
    
    customer_service_group.permissions.add(*all_permissions)
    
    return customer_service_group

def setup_reviewer_role():
    """
    Setup Reviewer role with appropriate permissions.
    
    Creates Reviewer group with permissions to:
    - All CRUD (Create, Read, Update, Delete) permissions for ALL models
    - Full CRUD permissions for CustomerProfile
    
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
    bulk_submission_content_type = ContentType.objects.get_for_model(BulkSubmission)
    customer_profile_content_type = ContentType.objects.get_for_model(CustomerProfile)
    
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
    
    # BulkSubmission permissions (full CRUD)
    bulk_add_perm = Permission.objects.get(codename='add_bulksubmission', content_type=bulk_submission_content_type)
    bulk_change_perm = Permission.objects.get(codename='change_bulksubmission', content_type=bulk_submission_content_type)
    bulk_view_perm = Permission.objects.get(codename='view_bulksubmission', content_type=bulk_submission_content_type)
    bulk_delete_perm = Permission.objects.get(codename='delete_bulksubmission', content_type=bulk_submission_content_type)
    
    # CustomerProfile permissions (full CRUD)
    customer_profile_add_perm = Permission.objects.get(codename='add_customerprofile', content_type=customer_profile_content_type)
    customer_profile_change_perm = Permission.objects.get(codename='change_customerprofile', content_type=customer_profile_content_type)
    customer_profile_view_perm = Permission.objects.get(codename='view_customerprofile', content_type=customer_profile_content_type)
    customer_profile_delete_perm = Permission.objects.get(codename='delete_customerprofile', content_type=customer_profile_content_type)
    
    # Assign all permissions to group (full CRUD for everything)
    all_permissions = [
        app_add_perm, app_change_perm, app_view_perm, app_delete_perm,
        company_info_add_perm, company_info_change_perm, company_info_view_perm, company_info_delete_perm,
        partner_add_perm, partner_change_perm, partner_view_perm, partner_delete_perm,
        product_add_perm, product_change_perm, product_view_perm, product_delete_perm,
        bulk_add_perm, bulk_change_perm, bulk_view_perm, bulk_delete_perm,
        customer_profile_add_perm, customer_profile_change_perm, customer_profile_view_perm, customer_profile_delete_perm,  # Full CRUD for CustomerProfile
    ]
    
    reviewer_group.permissions.add(*all_permissions)
    
    return reviewer_group

def setup_roles():
    """
    Setup Customer, Customer Service and Reviewer roles with appropriate permissions.
    
    Convenience function that calls all individual role setup functions.
    
    Returns:
        tuple: (customer_group, customer_service_group, reviewer_group) Group objects
    """
    customer_group = setup_customer_role()
    customer_service_group = setup_customer_service_role()
    reviewer_group = setup_reviewer_role()
    
    return customer_group, customer_service_group, reviewer_group
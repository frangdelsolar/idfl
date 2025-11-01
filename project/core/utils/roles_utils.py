from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from application.models import Application

def setup_customer_service_role():
    """
    Setup Customer Service role with appropriate permissions.
    
    Creates Customer Service group with permissions to:
    - add_application
    - change_application  
    - view_application
    
    Returns:
        Group: Customer Service group object
    """
    # Create Customer Service role
    customer_service_group, created = Group.objects.get_or_create(name='Customer Service')
    
    # Add basic permissions
    app_content_type = ContentType.objects.get_for_model(Application)
    
    add_perm = Permission.objects.get(codename='add_application', content_type=app_content_type)
    change_perm = Permission.objects.get(codename='change_application', content_type=app_content_type)
    view_perm = Permission.objects.get(codename='view_application', content_type=app_content_type)
    
    # Assign permissions to group
    customer_service_group.permissions.add(add_perm, change_perm, view_perm)
    
    return customer_service_group

def setup_reviewer_role():
    """
    Setup Reviewer role with appropriate permissions.
    
    Creates Reviewer group with permissions to:
    - add_application
    - change_application
    - view_application
    
    Returns:
        Group: Reviewer group object
    """
    # Create Reviewer role  
    reviewer_group, created = Group.objects.get_or_create(name='Reviewer')
    
    # Add basic permissions
    app_content_type = ContentType.objects.get_for_model(Application)
    
    add_perm = Permission.objects.get(codename='add_application', content_type=app_content_type)
    change_perm = Permission.objects.get(codename='change_application', content_type=app_content_type)
    view_perm = Permission.objects.get(codename='view_application', content_type=app_content_type)
    
    # Assign permissions to group
    reviewer_group.permissions.add(add_perm, change_perm, view_perm)
    
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
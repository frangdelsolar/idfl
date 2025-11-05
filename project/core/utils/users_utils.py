from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

def setup_admin_user():
    """
    Setup Admin superuser.
    
    Creates:
    - admin / admin (Superuser)
    
    Returns:
        User: Admin user object
    """
    User = get_user_model()
    
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin')
        admin_user.save()
    
    return admin_user

def setup_customer_service_user():
    """
    Setup Customer Service user.
    
    Creates:
    - cservice / cservice (Customer Service role)
    
    Returns:
        User: Customer Service user object
    """
    User = get_user_model()
    
    # Get the Customer Service group
    customer_service_group = Group.objects.get(name='Customer Service')
    
    customer_service_user, created = User.objects.get_or_create(
        username='cservice',
        defaults={
            'email': 'cservice@example.com',
            'is_staff': True
        }
    )
    if created:
        customer_service_user.set_password('cservice')
        customer_service_user.save()
        customer_service_user.groups.add(customer_service_group)
    
    return customer_service_user

def setup_reviewer_user():
    """
    Setup Reviewer user.
    
    Creates:
    - reviewer / reviewer (Reviewer role)
    
    Returns:
        User: Reviewer user object
    """
    User = get_user_model()
    
    # Get the Reviewer group
    reviewer_group = Group.objects.get(name='Reviewer')
    
    reviewer_user, created = User.objects.get_or_create(
        username='reviewer',
        defaults={
            'email': 'reviewer@example.com', 
            'is_staff': True
        }
    )
    if created:
        reviewer_user.set_password('reviewer')
        reviewer_user.save()
        reviewer_user.groups.add(reviewer_group)
    
    return reviewer_user

def setup_customer_user():
    """
    Setup Customer user.
    
    Creates:
    - customer / customer (Customer role)
    
    Returns:
        User: Customer user object
    """
    User = get_user_model()
    
    # Get the Customer group
    customer_group = Group.objects.get(name='Customer')
    
    customer_user, created = User.objects.get_or_create(
        username='customer',
        defaults={
            'email': 'customer@example.com',
            'is_staff': False  # Customers typically are not staff
        }
    )
    if created:
        customer_user.set_password('customer')
        customer_user.save()
        customer_user.groups.add(customer_group)
    
    return customer_user

def setup_users():
    """
    Setup all default users.
    
    Convenience function that calls all individual user setup functions.
    
    Returns:
        tuple: (admin_user, customer_service_user, reviewer_user, customer_user) User objects
    """
    admin_user = setup_admin_user()
    customer_service_user = setup_customer_service_user()
    reviewer_user = setup_reviewer_user()
    customer_user = setup_customer_user()
    
    return admin_user, customer_service_user, reviewer_user, customer_user
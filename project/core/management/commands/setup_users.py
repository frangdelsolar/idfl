from django.core.management.base import BaseCommand
from core import utils


class Command(BaseCommand):
    """
    Setup default users for Admin, Customer Service, Reviewer, and Customer roles.
    
    Creates four users:
    - admin / admin (Superuser)
    - cservice / cservice (Customer Service role)
    - reviewer / reviewer (Reviewer role)
    - customer / customer (Customer role)
    
    Example usage:
        python manage.py setup_users
    """
    
    help = 'Setup default users for Admin, Customer Service, Reviewer, and Customer roles'

    def handle(self, *args, **options):
        """
        Execute the user setup command.
        """
        self.stdout.write("Setting up default users...")

        try:
            admin_user, customer_service_user, reviewer_user, customer_user = utils.setup_users()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to setup users: {e}"))
            return

        self.stdout.write(self.style.SUCCESS(
            f"✓ Created Admin user: {admin_user.username}/{admin_user.username}"
        ))
        self.stdout.write(self.style.SUCCESS(
            f"✓ Created Customer Service user: {customer_service_user.username}/{customer_service_user.username}"
        ))
        self.stdout.write(self.style.SUCCESS(
            f"✓ Created Reviewer user: {reviewer_user.username}/{reviewer_user.username}"
        ))
        self.stdout.write(self.style.SUCCESS(
            f"✓ Created Customer user: {customer_user.username}/{customer_user.username}"
        ))
        
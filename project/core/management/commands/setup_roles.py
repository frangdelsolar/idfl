from django.core.management.base import BaseCommand
from core import utils

class Command(BaseCommand):
    """
    Setup Customer Service and Reviewer roles with appropriate permissions.
    
    Creates two groups:
    - Customer Service: Can add, change, and view applications
    - Reviewer: Can add, change, and view applications
    
    Example usage:
        python manage.py setup_roles
    """
    
    help = 'Setup Customer Service and Reviewer roles with permissions'

    def handle(self, *args, **options):
        """
        Execute the role setup command.
        """
        self.stdout.write("Setting up user roles and permissions...")

        try:
            customer_service_group, reviewer_group = utils.setup_roles()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to setup roles: {e}"))
            return

        self.stdout.write(self.style.SUCCESS(
            f"✓ Created Customer Service group: {customer_service_group}"
        ))
        self.stdout.write(self.style.SUCCESS(
            f"✓ Created Reviewer group: {reviewer_group}"
        ))
        self.stdout.write(self.style.SUCCESS('Successfully setup roles and permissions'))
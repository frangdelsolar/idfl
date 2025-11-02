from django.core.management.base import BaseCommand
from core import utils

class Command(BaseCommand):
    """
    Create dummy application data for testing and demonstration.
    
    Creates:
    - 1 Application in 'pending' status (📝 TO BE SUBMITTED - for Customer Service)
    - 1 Application in 'in_review' status (✅ TO BE APPROVED - all items correct)
    - 1 Application in 'in_review' status (❌ TO BE REJECTED - has unapproved items)
    
    Example usage:
        python manage.py dummy_data
    """
    
    help = 'Create dummy application data for testing and demonstration'

    def handle(self, *args, **options):
        """
        Execute the dummy data creation command.
        """
        self.stdout.write("Creating dummy application data...")

        try:
            submitted_app, approved_app, rejected_app = utils.create_dummy_data()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to create dummy data: {e}"))
            return

        self.stdout.write(self.style.SUCCESS("✓ Created 3 Applications:"))
        self.stdout.write(self.style.SUCCESS(f"  - {submitted_app.name} (Status: {submitted_app.status})"))
        self.stdout.write(self.style.SUCCESS(f"  - {approved_app.name} (Status: {approved_app.status})"))
        self.stdout.write(self.style.SUCCESS(f"  - {rejected_app.name} (Status: {rejected_app.status})"))
        self.stdout.write(self.style.SUCCESS('Successfully created dummy application data!'))
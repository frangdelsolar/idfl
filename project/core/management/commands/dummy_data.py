from django.core.management.base import BaseCommand
from core import utils

class Command(BaseCommand):
    """
    Create dummy application data for testing and demonstration.
    
    Creates:
    - Company data with addresses, supply chain companies, and certification bodies
    - 1 Application in 'pending' status (📝 TO BE SUBMITTED - for Customer Service)
    - 1 Application in 'in_review' status (✅ TO BE APPROVED - all items correct)
    - 1 Application in 'in_review' status (❌ TO BE REJECTED - has unapproved items)
    - Bulk submissions with various statuses
    
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
            data = utils.create_dummy_data()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to create dummy data: {e}"))
            return

        company_data = data['company_data']
        applications = data['applications']
        bulk_submissions = data['bulk_submissions']

        self.stdout.write(self.style.SUCCESS("✓ Created Company Data:"))
        self.stdout.write(self.style.SUCCESS(f"  - {len(company_data['companies'])} Companies"))
        self.stdout.write(self.style.SUCCESS(f"  - {len(company_data['supply_chain_companies'])} Supply Chain Companies"))
        self.stdout.write(self.style.SUCCESS(f"  - {len(company_data['certification_bodies'])} Certification Bodies"))
        self.stdout.write(self.style.SUCCESS(f"  - {len(company_data['customer_profiles'])} Customer Profiles"))
        self.stdout.write(self.style.SUCCESS(f"  - {len(company_data['addresses'])} Addresses"))

        self.stdout.write(self.style.SUCCESS("✓ Created 3 Applications:"))
        self.stdout.write(self.style.SUCCESS(f"  - {applications['submitted'].name} (Status: {applications['submitted'].status})"))
        self.stdout.write(self.style.SUCCESS(f"  - {applications['approved'].name} (Status: {applications['approved'].status})"))
        self.stdout.write(self.style.SUCCESS(f"  - {applications['rejected'].name} (Status: {applications['rejected'].status})"))

        self.stdout.write(self.style.SUCCESS(f"✓ Created {len(bulk_submissions)} Bulk Submissions"))

        self.stdout.write(self.style.SUCCESS('Successfully created all dummy data!'))
        
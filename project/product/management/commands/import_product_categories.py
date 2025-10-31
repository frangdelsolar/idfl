import logging
from django.core.management.base import BaseCommand

from product.utils.parsers import parse_product_category_xlsx 

class Command(BaseCommand):
    help = 'Import product categories from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the Excel file')

    def handle(self, *args, **options):
        
        file_path = options['file_path']
        
        self.stdout.write(f"Starting import from: {file_path}")

        try:
            parse_product_category_xlsx(file_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to import product categories: {e}"))
            return

        self.stdout.write(self.style.SUCCESS('Successfully imported product categories'))
        


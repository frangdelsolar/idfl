from django.core.management.base import BaseCommand
from product.utils.parsers import parse_product_category_xlsx 

class Command(BaseCommand):
    """
    Import product categories from an Excel file into the database.
    
    The Excel file should have two columns:
    - 'Codes' (e.g., PC0001, PC0002) 
    - 'Description' (e.g., "Men's apparel", "Women's apparel")
    
    Example usage:
        python manage.py import_product_categories /path/to/product_categories.xlsx
    
    This command uses get_or_create() to avoid duplicate entries.
    If a category with the same code already exists, it will be skipped.
    """
    
    help = 'Import product categories from Excel file' 

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path', 
            type=str, 
            help='Path to the Excel file (.xlsx) containing product categories'
        )

    def handle(self, *args, **options):
        """
        Execute the import command.
        
        Args:
            file_path (str): Path to the Excel file to import
            
        Raises:
            FileNotFoundError: If the specified file doesn't exist
            ValueError: If the file format is invalid or columns are missing
        """
        file_path = options['file_path']
        
        self.stdout.write(f"Starting import from: {file_path}")

        try:
            parse_product_category_xlsx(file_path)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to import product categories: {e}"))
            return

        self.stdout.write(self.style.SUCCESS('Successfully imported product categories'))
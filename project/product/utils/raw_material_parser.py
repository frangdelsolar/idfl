import pandas as pd
from enum import Enum
from product.models import RawMaterial
import logging


class RawMaterialColumn(str, Enum):
    """Column names for raw materials Excel file."""
    CODE = 'Codes'
    DESCRIPTION = 'Description'


def parse_raw_material_xlsx(file_path):
    """
    Import raw materials from Excel file into database.
    
    Args:
        file_path: Path to Excel file with 'Codes' and 'Description' columns
        
    Raises:
        ValueError: If file is missing or cannot be read
    """
    if not file_path:
        raise ValueError("File path is required")

    logging.info(f"Reading Excel file: {file_path}")
    
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        raise ValueError(f"Failed to read Excel file: {e}")
    
    logging.info(f"Total rows: {len(df)}")

    for index, row in df.iterrows():
        code = row[RawMaterialColumn.CODE]
        description = row[RawMaterialColumn.DESCRIPTION]

        # DATA CLEANUP AND VALIDATION
        # In real world app, there would be validations, and data cleanup
        # I'll just validate that fields are not empty.
        # and skip faulty rows
        
        if not code:
            logging.warning(f"Empty code at row {index}. Skipping...")
            continue
        
        if not description:
            logging.warning(f"Empty description at row {index}. Skipping...")
            continue

        item, created = RawMaterial.objects.get_or_create(
            code=code,
            description=description
        )

        if created:
            logging.info(f"Created: {item}")
        else:
            logging.info(f"Exists: {item}")

    logging.info("Import completed")
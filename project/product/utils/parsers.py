import pandas as pd
from enum import Enum
from product.models import ProductCategory
import logging


class ProductCategoryColumn(str, Enum):
    """
    ProductCategoryColumn enumerates the column names of the excel file
    """
    CODE = 'Codes'
    DESCRIPTION = 'Description'


def parse_product_category_xlsx(file_path):

    if not file_path:
        raise ValueError("File path is required")

    logging.info(f"Reading Excel file: {file_path}")

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        raise ValueError(f"Failed to read Excel file: {e}")
    
    logging.info(f"Total number of rows: {len(df)}")

    for index, row in df.iterrows():
        code = row[ProductCategoryColumn.CODE]
        description = row[ProductCategoryColumn.DESCRIPTION]

        item, created = ProductCategory.objects.get_or_create(
            code=code,
            description=description
        )

        if created:
            logging.info(f"Created product category: {index}, {item}")
        else:
            logging.info(f"Product category already exists: {index}, {item}")

    logging.info(f"Successfully imported product categories")
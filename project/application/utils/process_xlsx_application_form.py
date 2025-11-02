import pandas as pd
import logging
from application.models import (
    Application,
    ApplicationCompanyInfo,
    ApplicationSupplyChainPartner,
    ApplicationProduct
)

# Set up logging
logger = logging.getLogger(__name__)


def process_xlsx_application_form(application_form):
    """
    Process an Excel application form and create corresponding database records.
    
    Args:
        application_form: The application form object containing the Excel file
        
    Returns:
        bool: True if processing was successful
        
    Raises:
        ValueError: If required sheets are missing or data format is invalid
        Exception: For any other processing errors
    """
    file_path = application_form.file.path
    
    try:
        logger.info(f"Starting processing of application form: {application_form.name}")
        
        # Load and validate Excel file structure
        excel_file = pd.ExcelFile(file_path)
        required_sheets = ['info', 'supply chain company', 'product']
        missing_sheets = [sheet for sheet in required_sheets if sheet not in excel_file.sheet_names]
        
        if missing_sheets:
            error_msg = f"Missing required sheets: {missing_sheets}. Found sheets: {excel_file.sheet_names}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info("All required sheets found, reading data from Excel file")
        
        # Read data from each sheet
        company_df = pd.read_excel(file_path, sheet_name='info')
        supply_chain_df = pd.read_excel(file_path, sheet_name='supply chain company')
        products_df = pd.read_excel(file_path, sheet_name='product')
        
        # Retrieve the main application instance
        application = Application.objects.get(name=application_form.name)
        logger.info(f"Retrieved application: {application_form.name}")
        
        # Extract and process data from each sheet
        company_data = _extract_company_info(company_df)
        supply_chain_data = _extract_supply_chain_partners(supply_chain_df)
        products_data = _extract_products(products_df)
        
        # Create database records
        ApplicationCompanyInfo.objects.create(application=application, **company_data)
        logger.info("Created company info record")
        
        for partner_data in supply_chain_data:
            ApplicationSupplyChainPartner.objects.create(application=application, **partner_data)
        logger.info(f"Created {len(supply_chain_data)} supply chain partner records")
        
        for product_data in products_data:
            ApplicationProduct.objects.create(application=application, **product_data)
        logger.info(f"Created {len(products_data)} product records")
        
        logger.info("Application form processing completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error processing application form {application_form.name}: {str(e)}")
        raise e


def _extract_company_info(company_df):
    """
    Extract company information from the info sheet.
    
    Args:
        company_df: DataFrame containing company information
        
    Returns:
        dict: Processed company data
        
    Raises:
        ValueError: If the data format is invalid
    """
    try:
        company_data = {
            'name': _get_cell_value(company_df, 1, 2),
            'address': _get_cell_value(company_df, 2, 2),
            'city': _get_cell_value(company_df, 3, 2),
            'state': _get_cell_value(company_df, 4, 2),
            'country': _get_cell_value(company_df, 5, 2),
            'zip_code': _get_cell_value(company_df, 6, 2)
        }
        
        logger.info(f"Extracted company info for: {company_data['name']}")
        return company_data
        
    except Exception as e:
        error_msg = f"Invalid company info format: {str(e)}"
        logger.error(error_msg)
        raise ValueError(error_msg)


def _get_cell_value(df, row, col):
    """
    Safely extract cell value from DataFrame with error handling.
    
    Args:
        df: DataFrame to extract value from
        row: Row index
        col: Column index
        
    Returns:
        str: Cell value or empty string if not found
    """
    try:
        if len(df) > row and len(df.columns) > col:
            value = df.iloc[row, col]
            return value if pd.notna(value) else ""
        return ""
    except Exception as e:
        logger.warning(f"Error getting cell value at row {row}, col {col}: {str(e)}")
        return ""


def _extract_supply_chain_partners(supply_chain_df):
    """
    Extract supply chain partner information from the supply chain company sheet.
    
    Args:
        supply_chain_df: DataFrame containing supply chain partner data
        
    Returns:
        list: List of dictionaries containing partner data
    """
    # Define column mapping from Excel to database fields
    column_mapping = {
        'Supply Chain Company Name': 'name',
        'Address': 'address',
        'City': 'city',
        'State': 'state',
        'Country': 'country',
        'Zip Code': 'zip_code'
    }
    
    df = supply_chain_df.copy()
    
    # Remove completely empty rows
    df.dropna(how='all', inplace=True)
    
    # Rename columns to match database model fields
    df.rename(columns=column_mapping, inplace=True)
    
    # Keep only the columns we need
    target_columns = list(column_mapping.values())
    df = df[df.columns.intersection(target_columns)]
    
    # Fill missing values with empty strings
    df.fillna('', inplace=True)
    
    # Remove rows where company name is empty or whitespace
    df = df[df['name'].astype(str).str.strip() != '']
    
    # Remove rows where all values are empty
    df = df[df.astype(str).apply(lambda x: x.str.strip()).any(axis=1)]
    
    partners_data = df.to_dict('records')
    logger.info(f"Extracted {len(partners_data)} supply chain partners")
    
    return partners_data


def _extract_products(product_df):
    """
    Extract product information from the product sheet.
    
    Args:
        product_df: DataFrame containing product data
        
    Returns:
        list: List of dictionaries containing product data
    """
    # Remove completely empty rows
    product_df.dropna(how='all', inplace=True)
    
    # Forward fill grouping columns to handle merged cells
    product_df['Supply Chain Company'] = product_df['Supply Chain Company'].ffill()
    product_df['Product Name'] = product_df['Product Name'].ffill()
    product_df['Product Category'] = product_df['Product Category'].ffill()
    
    # Remove rows missing essential data
    product_df.dropna(subset=['Product Name', 'Supply Chain Company', 'Raw Materials'], inplace=True)
    
    # Group by product and aggregate raw materials
    products_group = product_df.groupby(
        ['Supply Chain Company', 'Product Name', 'Product Category']
    )['Raw Materials'].apply(lambda x: ', '.join(x.astype(str))).reset_index()
    
    products_group.rename(columns={'Raw Materials': 'Raw Materials List'}, inplace=True)
    
    # Map column names to database fields
    product_column_mapping = {
        'Supply Chain Company': 'supply_chain_partner_name_raw',
        'Product Name': 'product_name',
        'Product Category': 'product_category',
        'Raw Materials List': 'raw_materials_list'
    }
    
    products_group.rename(columns=product_column_mapping, inplace=True)
    products_data = products_group.to_dict('records')
    
    logger.info(f"Extracted {len(products_data)} products")
    
    return products_data
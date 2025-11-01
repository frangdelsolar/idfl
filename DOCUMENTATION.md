# Project Status

## ✅ Completed Tasks

### Task 1: Create Customer Models, Product Models and Seed Initial Data

#### Database Architecture

- **Address Normalization Strategy**: Created dedicated `Address` model to eliminate duplication across `Company`, `SupplyChainCompany`, and `CertificationBody` models, enabling consistent geographical data management
- **Relationship Design**: Implemented ForeignKey relationships for address references with `SET_NULL` to preserve business data when addresses are updated
- **Data Integrity**: Added unique constraints on ProductCategory, ProductDetail, and RawMaterial codes to prevent duplicates and ensure reliable identification
- **Comprehensive Documentation**: Maintained detailed model documentation with business context, usage examples, and string representations

#### Data Import System

- **Modular Import Framework**: Built three dedicated management commands with separate parsers for each model type to accommodate future schema evolution
- **Robust Data Processing**: Used pandas and openpyxl for Excel file parsing with proper data type handling and error resilience
- **Validation Layer**: Implemented basic data validation with comprehensive error handling and duplicate detection
- **Operational Visibility**: Integrated structured logging for import tracking, progress monitoring, and audit trails

### Task 2: Create Product Admin Pages

#### Admin Interface Design

- **Enhanced Product Model**: Added `name` field to Product model to support intuitive list displays and user-friendly identification in admin views
- **Autocomplete Integration**: Installed and configured django-autocomplete-light (DAL) for efficient large dataset handling

#### Advanced Admin Configuration

**ProductAdmin Customization:**

- **List Display**: Configured to show product name, category description, and detail description with custom methods for related field access
- **Search Optimization**: Enabled search across product name, category descriptions, and detail descriptions
- **Inline Management**: Implemented `RawMaterialInline` using TabularInline for intuitive many-to-many relationship management

**Autocomplete Implementation:**

- **Lazy Loading**: Configured DAL autocomplete widgets for `Product.category` and `Product.detail` ForeignKey fields
- **Filtered Querysets**: Autocomplete views filter to only show `is_active=True` records, preventing selection of inactive items
- **Multiple Selection**: Enabled autocomplete for raw materials with multi-select capability

**Form Optimization:**

- **Custom ModelForm**: Created `ProductModelForm` with autocomplete widgets replacing standard Select widgets
- **Field Exclusion**: Removed raw_materials from main form to rely exclusively on inline interface
- **Inline Autocomplete**: Extended autocomplete to RawMaterial inline through custom `RawMaterialInlineForm`

#### URL Routing & Views

- **Dedicated Autocomplete Endpoints**: Set up separate URL patterns for each autocomplete view
- **Secure Access**: Implemented user authentication checks in all autocomplete querysets
- **Search Optimization**: Added case-insensitive contains filtering on description fields

<!-- ### 3. Create application models, admin pages and pdf download
Now, tie everything together by modeling the application process itself and creating an interface for reviewing applications. The following features should be implemented based on the user stories:

1. As Customer Service, I can create applications, supply chain companies, company products based on the received application_form.xlsx, so the review can start.
2. As a Reviewer, I can approve or reject specific application product is valid or not so that our certificate maintains standards. e.g.:
    - Valid product composition
        - Product Catagory:
            -  Dyed fibers
        - Raw materials:
            - Recycled post-consumer glass
            - Wood
    - Invalid product composition
        - Product Catagory:
            -  Greige yarns
        - Raw materials:
            - Recycled post-consumer polyester
            - Polyethylene
3. As a Reviewer, I can approve or reject specific application supply chain companies so that our certificate maintains standards.
4. As a Reviewer, after finishing an application review, I can click a button to download a PDF report listing all approved products and supply chain companies to send to the customer.
    - You may use wkhtmltopdf (https://wkhtmltopdf.org/downloads.html) or another PDF tool.

**Note: You might want to check [Background & Workflow] section for understanding** -->

- Created Application model with file field so that application_form.xlsx can be uploaded. Configured django settings and urls, so that media is stored in media folder and is served with media url. Implemented logic for filename so that there are no accidental overrides.
- Created staging tables for Product, RawMaterial, ProductDetail, ProductCategory, SupplyChainCompany, and CertificationBody to keep track of application status and review progress.

## 🛠️ Project Infrastructure & Tooling

### Development Environment

- **Makefile Automation**: Created comprehensive Makefile with variable-based configuration for consistent project operations
- **Dependency Management**: Maintained requirements.txt with version-pinned dependencies including django-autocomplete-light
- **Virtual Environment**: Standardized Python 3.11 virtual environment setup

## 🚀 Quick Start Guide

### Prerequisites

```bash
# 1. Environment setup
python3.11 -m venv env
source env/bin/activate
pip install -r requirements.txt

# 2. Database setup
make migrate
make superuser

# 3. Data import
make import-product-categories
make import-product-details
make import-raw-materials

# 4. Run application
make run
```

Access the admin interface at http://localhost:8000/admin.
**NOTE:** If you are using Makefile commands, you will need to update the DATA_DIR variable in the Makefile to match your local directory structure, as well as the PYTHON variable to match your Python interpreter path.

### Known Limitations

- **Data Validation on import:** Pandas **NaN** handling requires fixes in validation logic
- **Company data ownership:** Company defines a users that can access the data, but other models do not have company field, nor the forms validate the user association to show, hide according to user rights.

### Design Decisions

#### Architecture choices

1. **Separate import functions:** Maintained individual parsers for each model to accommodate future schema differences.
2. **Address Normalization:** Created dedicated Address model to reduce duplication and improve scalability.
3. **Configuration Management:** Centralized file paths and commands in Makefile for easier maintenance.

#### Technical Implementation

1. **Autocomplete Strategy:** Selected django-autocomplete-light for its Django Admin integration and performance with large datasets
2. **Data Integrity:** Used SET_NULL for foreign keys to maintain historical relationships while allowing reference data updates
3. **Active Record Pattern:** Implemented is_active flags across reference tables to support soft deletion and historical reporting

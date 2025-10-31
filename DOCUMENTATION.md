# Project Status

## ✅ Completed Tasks

### Task 1: Database Modeling & Data Import

**Database Architecture:**

- Created `Address` model to eliminate duplication across `Company`, `SupplyChainCompany`, and `CertificationBody` models
- Implemented ForeignKey relationships for address references
- Maintained proper model documentation and string representations

**Data Import System:**

- Built three dedicated management commands for importing:
  - Product Categories
  - Product Details
  - Raw Materials
- Used pandas and openpyxl for Excel file parsing
- Added basic data validation and error handling
- Integrated logging for import tracking

**Project Infrastructure:**

- Set up a Makefile with variable-based configuration
- Created requirements.txt with all dependencies
- Implemented virtual environment setup

## 🚀 How to Run This Project

### Prerequisites

```bash
# Create and activate virtual environment
python3.11 -m venv env
source env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Available commands

```bash
make run              # Start development server
make migrate          # Apply database migrations
make superuser        # Create admin user

# Data import commands
make import-product-categories
make import-product-details
make import-raw-materials
```

### Known Limitations

- **Data Validation on import:** Pandas **NaN** handling requires fixes in validation logic
- Logging is not fully implemented

### Design Decisions

#### Architecture choices

1. **Separate import functions:** Maintained individual parsers for each model to accommodate future schema differences.
2. **Address Normalization:** Created dedicated Address model to reduce duplication and improve scalability.
3. **Configuration Management:** Centralized file paths and commands in Makefile for easier maintenance.

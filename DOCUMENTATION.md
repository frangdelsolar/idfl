# Coding Exercise — Product Certification Web App (Django) - Progress Report

by **Francisco Javier Gonzalez del Solar** - 高子安

This project implements a comprehensive Django web application for managing product certification workflows, enabling companies to apply for sustainability certifications through both manual and automated processes. The system supports Excel-based submissions, REST API integrations, and role-based review workflows with PDF certificate generation for approved applications.

## Index

- [Coding Exercise — Product Certification Web App (Django) - Progress Report](#coding-exercise--product-certification-web-app-django---progress-report)
  - [Index](#index)
  - [Quick Start](#quick-start)
  - [Project Structure](#project-structure)
    - [🗂️ Core Components](#️-core-components)
      - [Data \& Configuration](#data--configuration)
      - [Development \& Deployment](#development--deployment)
      - [Django Apps](#django-apps)
      - [Frontend](#frontend)
  - [✅ Tasks Completed](#-tasks-completed)
    - [Task 1: Create Customer Models, Product Models and Seed Initial Data - ✅ Completed](#task-1-create-customer-models-product-models-and-seed-initial-data----completed)
      - [Core Models Created](#core-models-created)
      - [Data Import System](#data-import-system)
      - [Database Design](#database-design)
    - [Task 2: Create Product Admin Pages - ✅ Completed](#task-2-create-product-admin-pages----completed)
      - [Admin Interface](#admin-interface)
      - [Autocomplete System](#autocomplete-system)
    - [Task 3: Create Application Models, Admin Pages and PDF Download System - ✅ Completed](#task-3-create-application-models-admin-pages-and-pdf-download-system----completed)
      - [Application Workflow](#application-workflow)
      - [Admin Interface](#admin-interface-1)
      - [PDF Certificate Generation](#pdf-certificate-generation)
      - [User Management](#user-management)
      - [🐳 Dockerization \& Deployment](#-dockerization--deployment)
    - [Task 4: Excel Upload and Background Task Processing - ✅ Completed](#task-4-excel-upload-and-background-task-processing----completed)
      - [Excel Upload \& Auto-Population](#excel-upload--auto-population)
      - [Bulk Submission System](#bulk-submission-system)
      - [Background Processing](#background-processing)
      - [🔄 Scalability Ready](#-scalability-ready)
    - [Task 5: Expose API Endpoints - ✅ Completed](#task-5-expose-api-endpoints----completed)
      - [REST API with Authentication](#rest-api-with-authentication)
      - [API Features](#api-features)
      - [Comprehensive Documentation](#comprehensive-documentation)
    - [Task 6: Customer-Facing Web Interface - ✅ Completed](#task-6-customer-facing-web-interface----completed)
      - [Frontend Architecture](#frontend-architecture)
      - [Customer Service Features](#customer-service-features)
      - [Customer Application Portal](#customer-application-portal)
      - [Authentication \& Security](#authentication--security)
      - [User Experience](#user-experience)
      - [Technical Implementation:](#technical-implementation)
      - [Limitations \& Future Improvements:](#limitations--future-improvements)
      - [📚 API Documentation](#-api-documentation)
  - [📝 Notes \& Limitations](#-notes--limitations)
    - [Current Constraints](#current-constraints)
    - [Technical Debt](#technical-debt)
  - [🎯 Final Thoughts](#-final-thoughts)

## Quick Start

1. Clone the repository:

    ```bash
    git clone git@github.com:frangdelsolar/idfl.git
    ```

2. Navigate to the project directory:

    ```bash
    cd idfl
    ```

3. Run setup and project:

    a. With docker:

    ```bash
    make docker
    ```

    b. Without docker (needs `wkhtmltopdf` installed):

    ```bash
    make local
    ```

4. Automatic Setup will perform the following tasks:
    - Docker container with all dependencies
    - Database migrations applied
    - Three user roles created
    - Sample data imported from Excel files
    - Dummy test data generated
5. Access the admin at: `http://localhost:8000/admin`
6. Use these credentials to login:

    - Superuser: `admin`/`admin`
    - Customer Service: `cservice`/`cservice`
    - Reviewer: `reviewer`/`reviewer`
    - Customer: `customer`/`customer`

## Project Structure

The project is structured as follows:

### 🗂️ Core Components

#### Data & Configuration

-   `data_files/` - Excel templates & sample data
-   `project/project/` - Django settings & URLs

#### Development & Deployment

-   `Makefile` - Automation for setup, testing, deployment
-   `Dockerfile` - Containerized environment
-   `requirements.txt` - Python dependencies

#### Django Apps

-   `application/` - Certification workflows, PDF generation, APIs
-   `product/` - Product models, data import commands
-   `customer/` - Company & user management
-   `core/` - User roles, utilities, setup commands

#### Frontend

-   `frontend/` - React app for customer-facing interface

## ✅ Tasks Completed

| Task                    | Status  | Key Features                     |
| ----------------------- | ------- | -------------------------------- |
| 1. Data Models & Import | ✅ Done | Excel imports, normalized models |
| 2. Admin Interface      | ✅ Done | Autocomplete, inline editing     |
| 3. Application Workflow | ✅ Done | PDF generation, review process   |
| 4. Excel Processing     | ✅ Done | Bulk upload, async processing    |
| 5. REST API             | ✅ Done | Token auth, Swagger docs         |

### Task 1: Create Customer Models, Product Models and Seed Initial Data - ✅ Completed

#### Core Models Created

-   **Company** - Customer companies with user associations
-   **SupplyChainCompany** - Supplier/partner companies
-   **CertificationBody** - Certification organizations
-   **Product** with Category, Detail, and RawMaterial relationships

#### Data Import System

-   **Management commands** to import Excel data from provided files
-   **Product categories, details, and raw materials** loaded automatically
-   **Duplicate prevention** with proper error handling

#### Database Design

-   **Normalized Address model** to eliminate duplication
-   **Foreign keys with SET_NULL** to preserve business data
-   **Unique constraints** to maintain data integrity

**_Demo_**

-   Navigate to `http://localhost:8000/admin`
-   Login with credentials: `admin`/`admin`
-   You can see the initial data imported from the Excel files.
-   Additionally you can see the logs for the import process during the setup process.

### Task 2: Create Product Admin Pages - ✅ Completed

#### Admin Interface

-   **Product list view** with name, category, and detail display
-   **Inline raw materials management** for easy editing
-   **Search and filtering** across key product fields

#### Autocomplete System

-   **Lazy-loading dropdowns** for product categories and details
-   **Filtered querysets** that exclude inactive items
-   **Performance optimized** for large datasets

**_Demo_**

-   Navigate to `http://localhost:8000/admin`
-   Login with credentials: `admin`/`admin`
-   You can see the autocomplete dropdowns and the search feature in action.

### Task 3: Create Application Models, Admin Pages and PDF Download System - ✅ Completed

#### Application Workflow

-   **Complete application lifecycle** from submission to certification
-   **Staging tables system** for review data isolation
-   **Role-based workflows** for Customer Service and Reviewer roles

#### Admin Interface

-   **Customer** Service: Create applications and manage submissions
-   **Reviewer**: Granular approval/rejection of products and suppliers
-   **Status tracking** with visual indicators and permissions

#### PDF Certificate Generation

-   **One-click PDF export** from admin interface
-   **Professional templates** with approved/rejected items
-   **Dynamic content** with detailed rejection reasons

#### User Management

-   **Three distinct roles**: Admin, Customer Service, Reviewer
-   **Role-based permissions** and field restrictions
-   **Secure authentication** with group controls

#### 🐳 Dockerization & Deployment

-   **Containerized PDF Generation**: Pre-configured dependencies
-   **Environment Isolation**: Consistent development/production environments
-   **Dependency Management**: Eliminated system-level installations

**_Demo_**

-   Navigate to `http://localhost:8000/admin`
-   Login with credentials: `admin`/`admin`
-   You can see the application workflow and PDF generation in action.

### Task 4: Excel Upload and Background Task Processing - ✅ Completed

#### Excel Upload & Auto-Population

-   **Automated Excel processing** - Uploads pre-fill staging tables automatically
-   **Pandas data extraction** from info, supply chain company, and product sheets
-   **Smart product aggregation** using forward-filling and groupby for clean records

#### Bulk Submission System

-   **BulkSubmission model** for batch processing with status tracking
-   **Async processing** with Python threading for non-blocking operations
-   **Role-based access** - Customer Service creates, Reviewer monitors all

#### Background Processing

-   **Fire-and-forget pattern** for immediate admin interface response
-   **Status auto-updates** when background processing completes
-   **Lightweight solution** without external dependencies

#### 🔄 Scalability Ready

-   **Production-ready architecture** that can upgrade to Celery + Redis
-   **Modular design** for easy task queue migration

### Task 5: Expose API Endpoints - ✅ Completed

#### REST API with Authentication

-   **Token-based authentication** using Django REST Framework
-   **Secure endpoints** requiring valid tokens for access
-   **Complete CRUD operations** for applications and related data

#### API Features

-   **GET/POST applications** with nested company and partner data
-   **Detailed response structures** with approval status and relationships
-   **Programmatic submission** eliminating manual Excel processing

#### Comprehensive Documentation

-   **Interactive Swagger UI** at `/api/docs/`
-   **JSON schema** for automated client generation
-   **Live testing** with authentication support

**_Demo_**

-   Run curl commands to test the API endpoints

```bash
# Get authentication token
curl -X POST http://localhost:8000/api-token-auth/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin"

# Get all applications
curl -X GET http://localhost:8000/api/applications/ \
  -H "Accept: application/json" \
  -H "Authorization: Token YOUR_AUTH_TOKEN"

# Submit new application
curl -X POST http://localhost:8000/api/applications/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  -d '{
    "name": "API DEMO - Eco Fabrics Inc Application",
    "description": "Sustainable textile company - Submitted via REST API",
    "company_info": {
      "name": "API DEMO - Eco Fabrics Inc",
      "address": "123 API Integration Street",
      "city": "Portland",
      "state": "Oregon",
      "zip_code": "97205",
      "country": "United States"
    },
    "supply_chain_partners": [
      {
        "name": "API DEMO - Organic Cotton Co-op",
        "address": "456 RESTful Road",
        "city": "Austin",
        "state": "Texas",
        "zip_code": "73301",
        "country": "United States",
        "products": [
          {
            "supply_chain_partner_name_raw": "API DEMO - Organic Cotton Co-op",
            "product_name": "API DEMO - Organic Cotton T-Shirt",
            "product_category": "Apparel",
            "raw_materials_list": "Organic cotton, Natural dyes"
          }
        ]
      }
    ]
  }'
```

### Task 6: Customer-Facing Web Interface - ✅ Completed

#### Frontend Architecture

-   **React Application** with Material-UI components for modern, responsive design
-   **Role-based routing** with authentication guards for secure access
-   **API integration** with comprehensive service layer for backend communication

#### Customer Service Features

-   **Customer Profile Creation** - Service agents can create customer accounts with company associations
-   **Streamlined workflow** - Automated user creation with Customer role assignment
-   **Success notifications** - Detailed response display with user credentials and role information

#### Customer Application Portal

-   **Dynamic form system** - Multi-section application form with nested data structures
-   **Real-time validation** - Comprehensive field validation with user-friendly error messages
-   **Supply chain management** - Dynamic partner and product addition/removal capabilities

#### Authentication & Security

-   **Token-based authentication** - Secure API communication with token persistence
-   **Role detection system** - Automatic role assignment based on username patterns
-   **Protected routes** - RoleGuard component ensures proper access control

#### User Experience

-   **Two-column login layout** - Credentials banner and login form side by side
-   **Role-specific guidance** - Post-login instructions tailored to user role
-   **Responsive design** - Mobile-friendly interface with proper breakpoints

#### Technical Implementation:

-   React hooks for state management
-   Material-UI component library
-   Context API for authentication state
-   React Router for navigation
-   Axios for API communication

#### Limitations & Future Improvements:

-   **Role Detection**: Currently uses username pattern matching (mock implementation for demo)
-   **State Management**: Basic React state - upgradable to Redux for complex applications
-   **Testing**: No test coverage implemented
-   **Type Safety**: JavaScript only - TypeScript migration recommended for production

**_Demo_**

```bash
make frontend
```

-   Navigate to [http://localhost:3000/](http://localhost:3000/)

-   Login with credentials

*   Customer Service: `cservice`/`cservice`
*   Customer: `customer`/`customer`

#### 📚 API Documentation

-   [Swagger UI](http://localhost:8000/api/docs/)
-   [JSON Schema](http://localhost:8000/api/schema/)

## 📝 Notes & Limitations

### Current Constraints

-   **Data validation** improvements needed for Excel imports
-   **User-company associations** not fully enforced in all views
-   **Basic async processing** using threading (upgradable to Celery)
-   **Logging** there's much more logging than needed. It's just for demo purposes.

### Technical Debt

-   **Type hints** - Limited type annotations in code
-   **Test coverage** - No test coverage
-   **Error handling** - Some edge cases need better coverage
-   **Database** - Maybe move to PostgresQL for better performance

## 🎯 Final Thoughts

This was a genuinely engaging project to work on - building a complete certification platform from scratch presented interesting architectural challenges and allowed me to design a robust system in a short amount of time.

I want to acknowledge that much of the code was created with AI assistance, which served as an incredibly productive pair-programming partner. However, I actively supervised every single line of code - reviewing, testing, and refining the output - just as I would when working with a development team in a professional setting.

The scope of implementing the six tasks within a reasonable timeframe would have been significantly more challenging without this tool. It allowed me to focus on system architecture, user experience, and business logic rather than getting bogged down in boilerplate code.

The end result is a fully functional (with some limitations), well-documented application that showcases my ability to design and implement complex systems effectively. I hope you find the project enjoyable and inspiring, and I look forward to the opportunity to collaborate with you on future projects.

**_Thanks for reading!_**

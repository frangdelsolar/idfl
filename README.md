# Coding Exercise — Product Certification Web App (Django)

## Overview
Build a Django web app that manages product certification. You’ll start from a provided scaffold project and extend it. **You may install any packages you find suitable**.

You’ll implement models, admin pages, data imports (from the provided Excel files), and basic workflows that reflect how customer service and reviewers process applications.


## What We Provide
- A scaffold Django project (folder structure + settings).
    - Edited core/models.py
    - Apps core, customer, product, application created and added to INSTALLED_APPS settings.py
- A Django admin account (create if missing):
    - username: admin
    - password: admin
    - If not present, run python manage.py createsuperuser.
- We use SQLite as default
- Sample data files:
    - data_files/product_category.xlsx
    - data_files/product_detail.xlsx
    - data_files/raw_material.xlsx
    - data_files/application_form.xlsx
    - data_files/application_form_advance.xlsx
    - data_files/process.xlsx
- (Optional) You can download wkhtmltopdf executable from https://wkhtmltopdf.org/downloads.html and place it at project/wkhtmltopdf if you choose this tool for PDF generation.


## Background & Workflow
This project involves building a Django web application for a product certification process. The general workflow is as follows:

1. A customer (a company seeking product certification) contacts customer service to apply for a certificate for their product(s).
2. The customer service representative sends the customer an Excel application form (see application_form.xlsx provided in the project data files).
3. The customer fills out this Excel form with all required details (company info, product details, raw materials, suppliers, etc.) and sends it back.
4. The customer service rep then opens the returned Excel and enters the data into the application via an admin interface (this is where the Django app comes into play to input and manage the data).
5. An application reviewer (an internal staff member) reviews the submitted application in the system, evaluates each product (including raw material composition) and supply chain partner, generates a PDF certificate report for approved products, and sends this report back to the customer.


## Task Overview
There are 3 basic tasks and 4 optional tasks listed below.
- If you are applying for a Junior position, you are only required to complete the 3 basic tasks.
- If you are applying for a Senior position, you are expected to complete at least 1 optional tasks in addition to the basic ones.

That being said, **we encourage all candidates to attempt the optional tasks (even partially)**, as doing so demonstrates the skills we are looking for.

It's common for people to interpret user stories differently. This is expected. **You are free to implement based on your assumptions as long as they are documented**. In fact, we actively evaluate a candidate's ability to interpret, transcribe, and communicate requirements.

You are free to install and use any external packages or libraries you find suitable to accomplish the tasks (for example, libraries for autocomplete fields, PDF generation, background jobs, API documentation, etc.). Feel free to leverage existing tools to implement the features efficiently.

You may use AI tools. However, please ensure you fully understand the output, as you may be asked to explain or defend your implementation during the interview.

Please list all completed, partially completed, or documented tasks in DOCUMENTATION.md, and ensure your submission includes setup instructions if your web application requires any additional configuration.

If you need clarification, feel free to reach out to HR.


### 1. Create Customer Models, Product Models and Seed Initial Data
We need a place to store product & company information that customers submit for certification.
1. Company
    - users: Many-to-many to Django’s built-in User
    - name: CharField (required).
    - address, city, state, zip_code, country: CharFields
2. SupplyChainCompany
    - name: CharField (required).
    - is_valid: BooleanField (default False).
    - address, city, state, zip_code, country: CharFields.
3. CertificationBody
    - name: CharField (required).
    - address, city, state, zip_code, country: CharFields.
4. Create models: Product, ProductCategory, ProductDetail, RawMaterial.
    - A Product has one ProductCategory and one ProductDetail.
    - A Product has multiple RawMaterial items.
5. Import seed data for ProductCategory and RawMaterial from:
    - data_files/product_category.xlsx
    - data_files/product_detail.xlsx
    - data_files/raw_material.xlsx
After defining these models, run migrations to create the corresponding tables in the database.

Acceptance notes
- Reasonable \__str__ methods exist.
- Running your import (management command, script, or admin action) loads categories and raw materials without manual edits.


### 2. Create Product Admin Pages
Next, set up Django admin pages to manage products and related data in an intuitive way for the staff.
1. Add a Product admin with list display showing product name, product category and product detail.
2. On the Product change page, allow adding/editing the product’s raw materials via an admin inline.
3. Use django-autocomplete-light (or similar) to make:
    - Product.product_category a lazy-loading dropdown,
    - Product.product_detail a lazy-loading dropdown,
    - Raw material selection a lazy-loading dropdown.
4. Add is_active (Boolean) to RawMaterial, ProductCategory and ProductDetail.
    - Inactive items (is_active=False) must not be searchable/selectable in admin autocomplete.

Acceptance notes
- Admin list filters/search fields are sensible.
- Autocomplete excludes inactive items.


### 3. Create application models, admin pages and pdf download
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

**Note: You might want to check [Background & Workflow] section for understanding**


### 4. (Optional) Excel Upload and Background Task Processing
*(The following requirements are optional enhancements, intended to test more advanced capabilities like asynchronous processing.)*

In a real scenario, manually re-entering data from the Excel form into the admin could be time-consuming. We want to streamline this:

1. Admin upload: As Customer Service, I can upload application_form.xlsx from the admin to auto-populate the application (assume no parsing errors).
2. Batch processing: Assume each Excel upload takes ~10 minutes to process. As Customer Service, I can upload multiple files, leave, and return later to see everything completed. (Background task queue recommended; assume no parsing errors.)


### 5. (Optional) Expose API Endpoints
*(This section is optional and meant to show skills in building RESTful APIs and documentation.)*

To enable customers to programmatically submit applications (instead of emailing Excel files), we want to expose parts of the system via a web API. This will also require securing the API and providing documentation for it.

1. As Customer Service, I can offer customers API endpoints to submit application data so I can spend time on more productive tasks.
2. As a customer’s developer, I can view up-to-date API documentation.
3. As a customer’s developer, I need the API to be secure.


### 6. (Optional) Simple Customer-Facing Pages
*(This section is optional and meant to show skills in HTML, CSS, and JavaScript.)*

Build basic pages for customers to apply online.

1. As a Customer Service, I can create an account for a customer and let the customer fill in the application online, so I can spend time on more productive tasks.
2. As a Customer, I can log in to a customer page and apply/fill out application forms.

Acceptance notes
- A functional prototype is sufficient.
- You may use Django templates, React, Vue.js, or other tools. Please provide appropriate documentation if needed.


### 7. (Optional) Product Process varification
*(This optional section are intended to evaluate algorithm understanding.)*

Currently, customers only provide output product's category and detail. We now want customers to also provide input product(s) and the processes used to create those outputs, so we can evaluate—from a manufacturing standpoint—whether the process(es) are reasonable. *You may ignore product raw materials for this task.* (Process data is in data_files/process.xlsx.)

Examples: Below are examples of production chains and why they may be considered valid or invalid:
Valid production
 - Reclaimed post-consumer materials |Chips (pellets)  ---Extrusion-->  Greige yarns | Filament
 - Greige yarns | Filament  ---Weaving-->  Greige fabrics | Woven fabrics
 - Greige fabrics | Woven fabrics  ---Dyeing-->  Dyed fabrics | Woven fabrics
 - Dyed fabrics | Woven fabrics  ---Manufacturing-->  Men's apparel | Overcoats jackets vests
 - Men's apparel | Overcoats jackets vests  ---Trading-->  Men's apparel | Overcoats jackets vests
*In the above valid chain-of-custody example, each process makes sense: Extrusion turns plastic chips into filament yarn; Weaving turns yarn into greige (undyed) fabric; Dyeing adds color to make dyed fabric; Manufacturing turns fabric into finished apparel; Trading doesn’t alter the product but is a step where the final product is sold/traded.*

Invalid production
- Greige fabrics | Woven fabrics ---Weaving--->  Dyed fabrics | Woven fabrics
    - Reason: [Weaving] produces fabric from yarn; it does not change color.
- Dyed fabrics | Woven fabrics  ---Manufacturing-->  Greige yarns | Filament
    - Reason: [Manufacturing] finished goods cannot produce greige yarn.

1. As Customer Service, I can create applications, supply chain companies, input/output products, and processes based on the received application_form_advance.xlsx, so the review can start. *You may ignore product raw materials for this task.* 
 - A supply chain company can have multiple processes.
2. As a Reviewer, I can create and maintain a table(s) that stores all valid input product → process → output product combinations.
3. As a Reviewer, I can verify each application product -from manufacturing standpoint— with one click; the system searches the database to confirm that the provided input product, process(es), and output products combination is valid, reducing human error.
    - (Valid) Greige yarns | Filament ---Weaving, Dyeing, Manufacturing--> Men's apparel | Overcoats jackets vests
    - (Valid) Greige yarns | Filament ---Manufacturing, Weaving, Dyeing--> Men's apparel | Overcoats jackets vests
    - (Valid) Men's apparel | Overcoats jackets vests ---Trading--> Men's apparel | Overcoats jackets vests
    - (invalid) Dyed fabrics | Woven fabrics  ---Extrusion-->  Men's apparel | Overcoats jackets vests



# MISC

## Commands That Created This Scaffold
- pyenv shell 3.12.8
- python -m venv virtual_environment
- source virtual_environment/bin/activate
- pip install django==5.2.4
- django-admin startproject project
- cd project
- python manage.py startapp core
- python manage.py startapp customer
- python manage.py startapp product
- python manage.py startapp application
- python manage.py migrate
- python manage.py createsuperuser
    - admin
    - admin
- Added core, customer, product, application to INSTALLED_APPS
- Edited core/models.py
- python manage.py runserver



## Codeing Task Version
- 20251002


.PHONY: run superuser migrations migrate import-product-categories import-product-details import-raw-materials

# Configuration
PYTHON := python3.11
MANAGE_PY := project/manage.py
DATA_DIR := /Users/fgs/Desktop/github.com/frangdelsolar/job-hunt/idfl/data_files

# File paths
PRODUCT_CATEGORIES_FILE := $(DATA_DIR)/product_category.xlsx
PRODUCT_DETAILS_FILE := $(DATA_DIR)/product_detail.xlsx
RAW_MATERIALS_FILE := $(DATA_DIR)/raw_material.xlsx

# Commands
run:
	$(PYTHON) $(MANAGE_PY) runserver

superuser:
	$(PYTHON) $(MANAGE_PY) createsuperuser --username admin

migrations:
	$(PYTHON) $(MANAGE_PY) makemigrations

migrate:
	$(PYTHON) $(MANAGE_PY) migrate

import-product-categories:
	$(PYTHON) $(MANAGE_PY) import_product_categories $(PRODUCT_CATEGORIES_FILE)

import-product-details:
	$(PYTHON) $(MANAGE_PY) import_product_details $(PRODUCT_DETAILS_FILE)

import-raw-materials:
	$(PYTHON) $(MANAGE_PY) import_raw_materials $(RAW_MATERIALS_FILE)
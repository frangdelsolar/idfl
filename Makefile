.PHONY: run superuser migrations migrate import-product-categories import-product-details import-raw-materials build stop clean shell init

# Configuration
IMAGE_NAME := idfl-app
CONTAINER_NAME := idfl-container

# Initialization Command
init: build
	@echo "Starting initialization..."
	@echo "Running container in background..."
	@docker run -d -p 8000:8000 --name $(CONTAINER_NAME) $(IMAGE_NAME) > /dev/null
	@sleep 3
	@echo "Applying migrations..."
	@docker exec $(CONTAINER_NAME) python manage.py migrate
	@echo "Setting up roles and users..."
	@docker exec $(CONTAINER_NAME) python manage.py setup_roles
	@docker exec $(CONTAINER_NAME) python manage.py setup_users
	@echo "Importing product categories..."
	@docker exec $(CONTAINER_NAME) python manage.py import_product_categories /app/data_files/product_category.xlsx
	@echo "Importing product details..."
	@docker exec $(CONTAINER_NAME) python manage.py import_product_details /app/data_files/product_detail.xlsx
	@echo "Importing raw materials..."
	@docker exec $(CONTAINER_NAME) python manage.py import_raw_materials /app/data_files/raw_material.xlsx
	@echo "Initialization complete!"
	@echo "Container is running at http://localhost:8000"
	@echo "Admin credentials: username=admin, password=admin"
	@echo "Customer Service: username=cservice, password=cservice"
	@echo "Reviewer: username=reviewer, password=reviewer"

# Main Commands
run: 
	docker run -p 8000:8000 --name $(CONTAINER_NAME) $(IMAGE_NAME)

build:
	docker build -t $(IMAGE_NAME) .

superuser:
	docker exec -it $(CONTAINER_NAME) python manage.py createsuperuser --username admin

migrations:
	docker exec $(CONTAINER_NAME) python manage.py makemigrations

migrate:
	docker exec $(CONTAINER_NAME) python manage.py migrate

import-product-categories:
	docker exec $(CONTAINER_NAME) python manage.py import_product_categories /app/data_files/product_category.xlsx

import-product-details:
	docker exec $(CONTAINER_NAME) python manage.py import_product_details /app/data_files/product_detail.xlsx

import-raw-materials:
	docker exec $(CONTAINER_NAME) python manage.py import_raw_materials /app/data_files/raw_material.xlsx

# Utility Commands
stop:
	docker stop $(CONTAINER_NAME)

clean: stop
	docker rm $(CONTAINER_NAME)

shell:
	docker exec -it $(CONTAINER_NAME) /bin/bash

start:
	docker start $(CONTAINER_NAME)

restart: stop start
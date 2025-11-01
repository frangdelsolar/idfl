.PHONY: run superuser migrations migrate import-product-categories import-product-details import-raw-materials build stop clean shell

# Configuration
IMAGE_NAME := idfl-app
CONTAINER_NAME := idfl-container

# Main Commands
run: build
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
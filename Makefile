.PHONY: docker docker-init local-init migrations migrate build stop clean shell start restart

# Configuration
IMAGE_NAME := idfl-app
CONTAINER_NAME := idfl-container

# Docker Commands
docker: docker-init

docker-init: build
	@echo "Starting Docker initialization..."
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
	@echo "Creating dummy application data..."
	@docker exec $(CONTAINER_NAME) python manage.py dummy_data
	@echo "Docker initialization complete!"
	@echo "Container is running at http://localhost:8000"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🚀 READY TO START THE WORKFLOW!"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "1. Go to http://localhost:8000/admin"
	@echo "2. Login as Customer Service:"
	@echo "   👤 Username: cservice"
	@echo "   🔑 Password: cservice"
	@echo "3. Click 'Submit Application' on the dummy application to start review"
	@echo "4. Then login as Reviewer to approve and complete the application"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "Admin credentials: username=admin, password=admin"
	@echo "Customer Service: username=cservice, password=cservice"
	@echo "Reviewer: username=reviewer, password=reviewer"

build:
	docker build -t $(IMAGE_NAME) .


# Local Development Commands
PYTHON=python3.11
DATA_DIR=data_files
MANAGE_PY=project/manage.py

local: local-init run

local-init:
	@echo "Starting local initialization..."
	@if [ -f project/db.sqlite3 ]; then \
		echo "Removing existing database..."; \
		rm project/db.sqlite3; \
	fi
	@echo "Applying migrations..."
	$(PYTHON) $(MANAGE_PY) migrate
	@echo "Setting up roles and users..."
	$(PYTHON) $(MANAGE_PY) setup_roles
	$(PYTHON) $(MANAGE_PY) setup_users
	@echo "Importing product categories..."
	$(PYTHON) $(MANAGE_PY) import_product_categories $(DATA_DIR)/product_category.xlsx
	@echo "Importing product details..."
	$(PYTHON) $(MANAGE_PY) import_product_details $(DATA_DIR)/product_detail.xlsx
	@echo "Importing raw materials..."
	$(PYTHON) $(MANAGE_PY) import_raw_materials $(DATA_DIR)/raw_material.xlsx
	@echo "Creating dummy application data..."
	$(PYTHON) $(MANAGE_PY) dummy_data
	@echo "Local initialization complete!"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "🚀 READY TO DEMO THE WORKFLOW!"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "1. Start the server:"
	@echo "   python project/manage.py runserver"
	@echo ""
	@echo "2. Access the admin at: http://localhost:8000/admin"
	@echo ""
	@echo "3. Use these credentials to login:"
	@echo ""
	@echo "   👑 ADMIN (Full Access):"
	@echo "   👤 Username: admin"
	@echo "   🔑 Password: admin"
	@echo ""
	@echo "   👨‍💼 CUSTOMER SERVICE (Submit Applications):"
	@echo "   👤 Username: cservice" 
	@echo "   🔑 Password: cservice"
	@echo ""
	@echo "   👩‍⚖️ REVIEWER (Approve/Reject Applications):"
	@echo "   👤 Username: reviewer"
	@echo "   🔑 Password: reviewer"
	@echo ""
	@echo "4. Demo Workflow:"
	@echo "   • Login as 'cservice' → Submit '📝 TO BE SUBMITTED' application"
	@echo "   • Login as 'reviewer' → Review '✅ TO BE APPROVED' & '❌ TO BE REJECTED'"
	@echo "   • Use 'Complete Application' buttons to see automatic decisions"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

run: 
	$(PYTHON) $(MANAGE_PY) runserver

# Add standalone command
dummy-data:
	$(PYTHON) $(MANAGE_PY) dummy_data

migrations:
	$(PYTHON) $(MANAGE_PY) makemigrations

migrate:
	$(PYTHON) $(MANAGE_PY) migrate

# Docker Utility Commands
stop:
	docker stop $(CONTAINER_NAME)

clean: stop
	docker rm $(CONTAINER_NAME)

shell:
	docker exec -it $(CONTAINER_NAME) /bin/bash

start:
	docker start $(CONTAINER_NAME)

restart: stop start
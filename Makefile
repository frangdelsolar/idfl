.PHONY: run

run:
	python3.11 project/manage.py runserver

superuser:
	python3.11 project/manage.py createsuperuser --username admin

makemigrations:
	python3.11 project/manage.py makemigrations

migrate:
	python3.11 project/manage.py migrate
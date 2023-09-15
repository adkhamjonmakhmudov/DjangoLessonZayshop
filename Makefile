mig:
	python3 manage.py makemigrations
	python3 manage.py migrate
	python3 manage.py createsuperuser


unmig:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	python3 manage.py ram
	pip3 uninstall django
	pip3 install django

ram:
	python3 manage.py ram

admin:
	python3 manage.py createsuperuser

remig:
	make unmig
	make mig
	make admin
	python manage.py add_product -p 1000 -c 9

brnma:
	rm -f your_app/migrations/*.py
	python3 manage.py makemigrations
	find . -name "__pycache__" -exec rm -r {} \;
	rm -r your_app/migrations/__pycache__




install:
	pip install -r requirements.txt

req:
	pip freeze > requirements.txt

server:
	python manage.py runserver 127.0.0.1:8000

lint:
	flake8 api
	flake8 FinanceBackend

test:
	python manage.py test
	coverage run manage.py test
#	coverage report
	coverage html

secretkey:
	python -c 'from django.utils.crypto import get_random_string; print(get_random_string(40))'
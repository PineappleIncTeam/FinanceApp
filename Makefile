install:
	poetry install

req:
	pip freeze > requirements.txt

server:
	poetry run python manage.py runserver 127.0.0.1:8000

lint:
	poetry run flake8 api
	poetry run flake8 FinanceBackend

test:
	poetry run python manage.py test
	poetry run coverage run manage.py test
#	coverage report
	poetry run coverage html

secretkey:
	python -c 'from django.utils.crypto import get_random_string; print(get_random_string(40))'
requirements:
	pip install -r requirements.txt

isort:
	isort .

flake8:
	flake8 ./

mypy:
	mypy multiservice.py

check: isort flake8 mypy

lint:
	isort .
	flake8
	mypy .

test:
	coverage run -m pytest -vv
	coverage report

check: lint test



PRJ = easycli


.PHONY: coverage
coverage:
	pytest --cov=$(PRJ) tests


.PHONY: lint
lint:
	pylama


.PHONY: dist
dist:
	python setup.py sdist

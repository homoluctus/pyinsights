.PHONY: lint
lint:
	poetry run pylint --rcfile=pylintrc pyinsights/ tests/

.PHONY: format
format:
	poetry run black pyinsights/ tests/

.PHONY: test
test:
	poetry run pytest --cov=pyinsights tests

.PHONY: mypy
mypy:
	poetry run mypy pyinsights/ tests/

.PHONY: release
release:
	poetry publish -n --build -u $(username) -p $(password)

install:
	poetry install

lint:
	poetry run flake8 menu_app

run:
	poetry run uvicorn menu_app.main:app --host localhost --port 8000 --reload

.PHONY: install lint run
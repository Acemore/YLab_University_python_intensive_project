FROM python:3.10-slim

WORKDIR /menu_app_project

RUN pip install poetry

ADD pyproject.toml poetry.lock ./
RUN poetry install --no-root

ADD . .

CMD ["poetry", "run", "uvicorn", "menu_app.main:app", "--host", "0.0.0.0"]

FROM python:3.10-slim

WORKDIR /menu_app_project

ADD . .

RUN pip install poetry
RUN poetry install

CMD ["poetry", "run", "uvicorn", "menu_app.main:app", "--host", "0.0.0.0"]

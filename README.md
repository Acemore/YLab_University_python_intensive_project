[![Maintainability](https://api.codeclimate.com/v1/badges/299b5686e1ff7bdb76a8/maintainability)](https://codeclimate.com/github/Acemore/YLab_University_python_intensive_project/maintainability)
[![linter-check](https://github.com/Acemore/YLab_University_python_intensive_project/actions/workflows/linter.yml/badge.svg)](https://github.com/Acemore/YLab_University_python_intensive_project/actions/workflows/linter.yml)

**Menu app** is web app that provides REST API CRUD operations to work with restaurant menus. 

### To run **Menu app**

Clone repo

```bash
git clone git@github.com:Acemore/YLab_University_python_intensive_project.git
```

Initialize Python virtual environment

```
python -m venv .venv

# Shell
source .venv/bin/activate

# Windows
.venv\Scripts\activate.bat
```

Create .env file in root project dir and add local var

```
SQLALCHEMY_DATABASE_URL=<your Postgres Connection URL>
```

Install dependencies

```bash
python -m pip install poetry
poetry install
```

Launch server with the app

```bash
poetry run uvicorn menu_app.main:app --reload
```

Go to address http://localhost:8000/ or http://127.0.0.1:8000/

[![docker-ci](https://github.com/Acemore/YLab_University_python_intensive_project/actions/workflows/docker.yml/badge.svg)](https://github.com/Acemore/YLab_University_python_intensive_project/actions/workflows/docker.yml)
[![pre-commit-check](https://github.com/Acemore/YLab_University_python_intensive_project/actions/workflows/pre-commit.yml/badge.svg?branch=main)](https://github.com/Acemore/YLab_University_python_intensive_project/actions/workflows/pre-commit.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/299b5686e1ff7bdb76a8/maintainability)](https://codeclimate.com/github/Acemore/YLab_University_python_intensive_project/maintainability)

**Menu app** is web app that provides REST API CRUD operations to work with restaurant menus.

## To run app and tests in Docker

Run app

```
docker compose up -d
```

Run tests

```
docker compose -f docker-compose-tests.yml up
```

Remove containers

```
docker compose rm -fs
```

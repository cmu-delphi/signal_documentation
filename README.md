# Signal Documentation
Single Source of Documentation System

## Core libs and DB
1. [Django](https://www.djangoproject.com/)
2. [Django-filter](https://django-filter.readthedocs.io/en/stable/index.html)
3. [PostgreSQL](https://www.postgresql.org/)


All requirements you can find in `Pipfile`

## Getting started

### Setup Env Vars

create `.env` file and add variables like in `.env.example`

### To run locally

Install `python:3.10`, `pip3`, `pipenv`

Using [pipenv](https://github.com/pypa/pipenv) run `pipenv shell` and `pipenv install` to create virtual environment and install dependencies

```sh
$ pipenv shell
$ pipenv install
```

Go to `src` directory and run

```sh
$ python manage.py migrate
$ python manage.py test
$ python manage.py runserver
```

### To run via docker

Install `Docker` and `docker-compose`

Run
```sh
$ docker-compose build
$ docker-compose up

```

Open `http://localhost:8000` to view it in the browser

## [Django admin](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/) web interface (user should be `is_staff` or `is_superuser`)
`http://localhost:8000/admin`

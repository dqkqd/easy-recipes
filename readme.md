# Easy-recipes

## Table of Contents

* **[Motivation](#motivation)**
* **[Development](#development)**
  * [Backend](#backend)
    * [Fileserver](#fileserver)
    * [API server](#api-server)
  * [Frontend](#frontend)
* **[API Reference](#api-reference)**

## Motivation

Easy-recipes is a web application which allow people to make their own recipes and share with others.
This is my final project for udacity fullstack development course.
The project is written using [Flask](https://flask.palletsprojects.com/) for backend and [Vue](https://vuejs.org/) for frontend.

## Getting started

You should have [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/) installed
in your machine to get start.

You now can set up the environment using docker compose.

```bash
docker compose up --force-recreate --build
```

You should wait a few seconds for database initialization.
Then open another terminal, run the command below to apply migrations.

```bash
docker compose exec backend flask db upgrade
```

Your application is now live at [http://localhost:4173/](http://localhost:4173/).

However, your application will come with no recipes and ingredients. You can add some sample using the command below.

```bash
docker compose exec backend flask sample add 
```

## Development

### Backend

To develop, you should fork the repository and then clone it locally.
You also need [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/) installed
in order to develop without setting up database, changing port and hosts.

**Easy recipes**'s backend consists of two parts.

* Filesever: live at `fileserver` folder.
* API server: live at `backend` folder.

Both of them use [pytest](https://pytest.org/) for testing, [ruff](https://docs.astral.sh/ruff/) for linting, [mypy](https://mypy-lang.org/) for type-checking and [black](https://black.readthedocs.io/en/stable/) for formatting.

With everything setup, you can build testing environment:

```bash
docker compose -f docker-compose-testing.yml up --force-recreate -d 
```

After that you can run test suite to make sure everything working correctly.
You might have to wait for a few seconds before database is completely set up.

```bash
docker compose exec fileservertest pytest
docker compose exec backendtest pytest
```

*Backend is developing using python 3.11. If you want to make any changes, you might need to install python 3.11.*

#### Fileserver

Fileserver is a simple server, used to store and serve images.
It serves only 3 routes for getting file, uploading file and deleting file.
See [fileserver's route](./fileserver/app/api.py) for more details.

Fileserver uses Fernet keys for authentication when uploading and deleting file.
You need to set those keys using environment variables.
See [cryptography's readme](https://github.com/pyca/cryptography) on how to generate a key.

```bash
FILE_SERVER_ENCRYPT_KEY=DZd3mOJJSgohhvx0SKZ84jllhNswcxt6Ry4Noz9aabQ=
FILE_SERVER_PASSWORD=password
FILE_SERVER_AUTHORIZATION_SCHEME=FERNET_TOKEN
```

See [environment variables example](./env-file.example) on how to set other environment variables for fileserver.

#### API server

This is the main api server for **Easy recipes**.

```bash
├── app
│   ├── auth.py                   # authentication for specific roles
│   ├── config.py                 # app config and testing config
│   ├── cli.py                    # useful cli commands for developing 
│   ├── crud                      # logic for talking with database
│   │   ├── base.py
│   │   ├── ingredient.py
│   │   └── recipe.py
│   ├── database.py
│   ├── errors.py                 # errors handler and errors casting
│   ├── file_server               # logics for talking with fileserver
│   │   ├── file.py
│   │   ├── image.py
│   │   └── server.py
│   ├── __init__.py               # application setup and errorhandler register
│   ├── models                    # database model
│   │   ├── base.py
│   │   ├── ingredient.py
│   │   ├── recipe.py
│   │   └── references.py
│   ├── routes                    # api endpoints
│   │   ├── ingredient.py
│   │   └── recipe.py
│   └── schemas                   # pydantic models for validation
│       ├── base.py
│       ├── ingredient.py
│       └── recipe.py
├── migrations                    # migrations folder
│   └── versions
├── pyproject.toml
├── readme.md
└── tests                         # tests folder
    ├── conftest.py
    ├── __init__.py
    ├── mocks.py
    ├── units
    │   ├── file_server
    │   │   ├── test_file.py
    │   │   ├── test_image.py
    │   │   └── test_server.py
    │   ├── test_auth.py
    │   ├── test_ingredient.py
    │   └── test_recipes.py
    └── utils.py
```

The main models are Recipes and Ingredients, they have many-to-many relationship.

During developing, you need to run fileserver first, because *api server* will need to talk with fileserver to store images.

Normally, testing *api server* will use mocking authentication, if you need to test with the real authentication.
You need to set up [auth0](https://auth0.com/) and provide proper tokens in environment variables.

You then need to set `USE_REAL_AUTH_TEST=1` and provide two tokens for two roles. See [API Reference](#api-reference) for roles definition.

```bash
# testing with real token might be slow
USE_REAL_AUTH_TEST=0
MENU_MANAGER_TOKEN=
MANAGER_TOKEN=
```

Testing with real authentication will be very slow, so it's not recommend.

### Frontend

**Easy recipes**'s frontend is developing using [Vue](https://vuejs.org/) and [TypeScript](https://www.typescriptlang.org/).
You should have the latest [Nodejs 20.7](https://nodejs.org/en) installed to develop frontend.

To get start, go to frontend folder and install necessary packages

```bash
cd frontend
npm run install
```

All the tests in frontend are mocked, so you can run it without setting up api server, authentication, etc.
You can run the test suite using command below

```bash
npm run test:component
```

## API Reference

Application includes 6 permissions and 2 roles.

**Permissions**:

* Create recipe
* Update recipe
* Delete recipe
* Create ingredient
* Update ingredient
* Delete ingredient

**Roles**:

* Menu manager: Can perform create, update.
* Manager: Can perform create, update and delete.

# Easy-recipes

Easy-recipes is a web application which allow people to make their own recipes and share with others.
This is my final project for udacity fullstack development course.
The project is written using [Flask](https://flask.palletsprojects.com/) for backend and [Vue](https://vuejs.org/) for frontend.

**Since I'm not working on the course anymore, if you are about to build the application, please [set up your own authentication](#set-up-authentication).**

## Table of Contents

* **[Getting started](#getting-started)**
  * [Login](#login)
* **[Development](#development)**
  * [Backend](#backend)
    * [Fileserver](#fileserver)
    * [API server](#api-server)
  * [Frontend](#frontend)
* **[Deployment](#deployment)**
  * [Upload docker image](#upload-docker-image)
  * [Create EKS cluster](#create-eks-cluster)
  * [Set up EBS for database](#set-up-ebs-for-database)
  * [Deploy database](#deploy-database)
  * [Deploy backend and frontend](#deploy-backend-and-frontend)
* **[Roles and permissions](#roles-and-permissions)**
  * [Set up authentication](#set-up-authentication)
* **[API Reference](#api-reference)**
  * [Recipes](#recipes)
  * [Ingredients](#ingredients)
  * [Errors](#errors)

## Getting started

You should have [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/) installed
in your machine to get start.

You now can set up the environment using docker compose.

```bash
docker compose up --force-recreate --build
```

You should wait a few seconds for database initialization, then open another terminal, run the command below to apply migrations.

```bash
docker compose exec backend flask db upgrade
```

Your application is now live at [http://localhost:4173/](http://localhost:4173/).

However, it would come with no data. You can add sample data using the command below, or you can [login](#login) and create your own.

```bash
docker compose exec backend flask sample add 
```

### Login

To add recipes and ingredients, you need to login as a user with specific role.
If you want to set up your own authentication, please refer to [Roles and permissions](#roles-and-permissions).
Or, you can use default users using email and password provided in [credentials](./credentials).
*Email and password provided in credentials file might be changed or inactivated in the future*

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

See [environment variables example](./env-file.example) on how to set other environment variables (optional) for fileserver.

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

You then need to set `USE_REAL_AUTH_TEST=1` and provide two tokens for two roles. See [Roles and permissions](#roles-and-permissions) for roles definition and [tials](./credentials) for provided tokens.

```bash
# testing with real token might be slow
USE_REAL_AUTH_TEST=0
MENU_MANAGER_TOKEN=
MANAGER_TOKEN=
```

*Testing with real authentication will be very slow, so it's not recommend.*

### Frontend

**Easy recipes**'s frontend is developing using [Vue](https://vuejs.org/) and [TypeScript](https://www.typescriptlang.org/).
You should have latest [Nodejs](https://nodejs.org/en) installed to develop frontend.

To get start, go to frontend folder and install necessary packages

```bash
cd frontend
npm install
```

All the tests in frontend are mocked, so you can run it without setting up api server, authentication, etc.
You can run the test suite using the command below.

```bash
npm run test:component
```

Frontend will automatically start when you run docker compose as specified in [getting started](#getting-started).
If you want to develop without running inside docker (recommend way), you can delete the `frontend` container inside [docker compose config](./docker-compose.yml).
Then run the command below to start development.

```bash
npm run dev
```

## Deployment

Application is deployed in [AWS](https://aws.amazon.com/) using [EKS](https://aws.amazon.com/eks/) and [Kubernetes](https://kubernetes.io/).

### Upload docker image

You should build 3 docker images in `fileserver`, `backend` and `frontend` folder.
Then push them into docker hub and substitute those image in **TODO**.

### Create EKS cluster

```bash
eksctl create cluster --name easy-recipes --nodes=2 --node-volume-size=8 --version=1.27 --instance-types=t3.medium --region=us-west-2 
```

### Set up EBS for database

You can follow along [AWS documnet](https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html) on how to set up ebs.
Here's a summary:

Set up oidc id for cluster:

```bash
eksctl utils associate-iam-oidc-provider --cluster easy-recipes --approve
```

Set up IAM service account for ebs:

```bash
eksctl create iamserviceaccount \
  --name ebs-csi-controller-sa \
  --namespace kube-system \
  --cluster easy-recipes \
  --role-name AmazonEKS_EBS_CSI_DriverRole \
  --role-only \
  --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
  --approve
```

Apply `aws-ebs-csi-driver` to `your-aws-id`.

```bash
eksctl create addon --name aws-ebs-csi-driver --cluster easy-recipes --service-account-role-arn arn:aws:iam::<your-aws-id>:role/AmazonEKS_EBS_CSI_DriverRole --force
```

Wait until all `ebs-csi` pods are running

```bash
kubectl get pods -n kube-system -l app.kubernetes.io/name=aws-ebs-csi-driver
```

### Deploy database

Deploy your database using these command:

```bash
kubectl apply -k deploy/database
```

### Deploy backend and frontend

#### Apply kubernetes config

Substitute your docker image in [backend.yml](./deploy/backend/backend.yml), [fileserver.yml](./deploy/backend/fileserver.yml) and [frontend.yml](./deploy/frontend.yml)
Then deploy your backend and frontend using these commands:

```bash
kubectl apply -k deploy/backend
kubectl apply -f deploy/frontend.yml
```

Make sure all your backend pods are running

```bash
kubectl get pods
```

#### Migration

Go inside your backend pods and migrate database.

```bash
kubectl exec -it pod/backend-<random-id> -- flask db upgrade
```

#### Change environment variables

Get your external ip address

```bash
kubectl get services
```

In [backend's env file](./deploy/backend/env-file.backend.example)

* Change `FILE_SERVER_HOST` with fileserver external ip address.

In [frontend's env file](./frontend/.env.production), you need to change some variables:

* Set `VITE_FORCE_CONVERT_URL=false`.
* Change `VITE_API_HOST` with backend external ip address.
* Change `VITE_AUTH0_CALLBACK_URL` with frontend external ip address.

Then, go to your auth0 application setting and change Callback URL with the same value as `VITE_AUTH0_CALLBACK_URL`.

## Roles and permissions

Application includes 6 permissions and 2 roles.

**Permissions**:

* Create recipe: `create:recipe`
* Update recipe: `update:recipe`
* Delete recipe: `delete:recipe`
* Create ingredient: `create:ingredient`
* Update ingredient: `update:ingredient`
* Delete ingredient: `delete:ingredient`

**Roles**:

* Menu manager: Can perform create, update.
* Manager: Can perform create, update and delete.

### Set up authentication

To set up your own authentication,
you need to have an [auth0](https://auth0.com/).

After creating your account,
you can create [auth0 application](https://auth0.com/docs/get-started/applications/application-settings) and
[auth0 api](https://auth0.com/docs/get-started/apis/api-settings) to get start.
*Remember to create roles and permissions when setting up your auth0 api.*

When you finished you set up, change corresponding environment variables in [env-file](./env-file.example) and [frontend/.env](./frontend/.env).

```bash
# env-file
AUTH0_DOMAIN=
ALGORITHM=
API_AUDIENCE=
```

```bash
# frontend/.env
VITE_AUTH0_CALLBACK_URL=
VITE_AUTH0_DOMAIN=
VITE_AUTH0_ALGORITHM=
VITE_AUTH0_API_AUDIENCE=
VITE_AUTH0_CLIENT_ID=
```

## API Reference

If you setup properly follow the steps in [Getting started](#getting-started),
your api server should live at [http://localhost:8000/](http://localhost:8000/).
Or if you want to test with deployed api server,
please refer to [Deployment](#deployment) for the real api sever.

### Recipes

#### `GET /recipes/all`

* Description: Get all recipes in the database.
* Permission: Not required
* Request example:

```bash
curl 'http://localhost:8000/recipes/all'
```

* Response example:

```json
{
  "recipes": [
    {
      "description": "Very delicous pumpkin soup",
      "id": 8,
      "image_uri": "https://images.unsplash.com/photo-1476718406336-bb5a9690ee2a",
      "ingredients": [
        {
          "description": "Very delicous pumpkin",
          "id": 8,
          "image_uri": "https://images.unsplash.com/photo-1570586437263-ab629fccc818",
          "likes": 4,
          "name": "Pumpkin"
        }
      ],
      "likes": 5,
      "name": "Pumpkin soup"
    }
  ],
  "total": 1
}
```

#### `GET /recipes`

* Description: Get recipes from the database with pagination.
* Permission: Not required
* Query parameters:
  * `per_page` (**integer**: optional, **default**: 12): maximum how many recipes you want to receive in your response.
  * `page`: (**integer**: optional, **default**: 1): paginating recipes response.
* Request example:

```bash
curl 'http://localhost:8000/recipes/?per_page=2&page=2'
```

* Response example:

```json
{
  "page": 2,
  "per_page": 2,
  "recipes": [
    {
      "id": 3,
      "name": "Pumpkin soup",
      "description": "Very delicous pumpkin soup",
      "image_uri": "https://images.unsplash.com/photo-1476718406336-bb5a9690ee2a",
      "ingredients": [
        {
          "id": 4,
          "name": "Pumpkin"
          "description": "Very delicous pumpkin",
          "image_uri": "https://images.unsplash.com/photo-1570586437263-ab629fccc818",
          "likes": 0
        }
      ],
      "likes": 0
    }
  ],
  "total": 3
}
```

#### `GET /recipes/<id>`

* Description: Get specific recipe from database.
* Permission: Not required
* Parameters:
  * `id` (**integer**: required): id of the recipe you want to get.
* Request example:

```bash
curl 'http://localhost:8000/recipes/2'
```

* Response example:

```json
{
  "id": 2,
  "name": "Orange juice",
  "description": "Very delicous orange juice",
  "image_uri": "https://images.unsplash.com/photo-1613478223719-2ab802602423",
  "ingredients": [
    {
      "id": 3,
      "name": "Orange",
      "description": "Very delicous orange",
      "image_uri": "https://images.unsplash.com/photo-1582979512210-99b6a53386f9",
      "likes": 0,
    }
  ],
  "likes": 0,
}
```

#### `POST /recipes`

* Description: Create new recipe.
* Permission: **create recipe**.
* Request body:
  * `name` (**string**: required): name of the recipe.
  * `description` (**string**: optional): description of the recipe.
  * `image_uri`: (**string**: optional): url of the recipe.
* Request example:
refer to [credientials](./credentials) for token.

```bash
curl -X POST 'http://localhost:8000/recipes/' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <token>' \
  -d '{"name":"my recipe", "description":"my description", "image_uri":"https://picsum.photos/200"}'
```

* Response example:

```json
{
  "id": 4
}
```

#### `PATCH /recipes/<id>`

* Description: Update recipe information.
* Permission: **update recipe**.
* Parameters:
  * `id` (**integer**: required): id of the recipe you want to update.
* Request body:
  * `name` (**string**: optional): new name of the recipe.
  * `description` (**string**: optional): new description of the recipe.
  * `image_uri`: (**string**: optional): new url of the recipe.
* Request example:
refer to [credientials](./credentials) for token.

```bash
curl -X PATCH 'http://localhost:8000/recipes/4' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <token>' \
  -d '{"name":"my new recipe", "description":"my new description", "image_uri":"https://picsum.photos/300"}'
```

* Response example:

```json
{
  "id": 4,
  "name": "my new recipe",
  "description": "my new description",
  "image_uri": "http://your-recipe-image-url-in-fileserver",
  "ingredients": [],
  "likes": 0
}
```

#### `DELETE /recipes/<id>`

* Description: Delete recipe.
* Permission: **delete recipe**.
* Parameters:
  * `id` (**integer**: required): id of the recipe you want to delete.
* Request example:
refer to [credientials](./credentials) for token.

```bash
curl -X DELETE 'http://localhost:8000/recipes/4' \
  -H 'Authorization: Bearer <token>'
```

* Response example:

```json
{
  "id": 4
}
```

#### `POST /recipes/<id>/like`

* Description: Like recipe.
* Permission: Not required.
* Parameters:
  * `id` (**integer**: required): id of the recipe you want to like.
* Request example:

```bash
curl -X POST 'http://localhost:8000/recipes/2/like'
```

* Response example:

```json
{
  "id": 2,
  "total_likes": 1
}
```

#### `GET /recipes/<id>/ingredients/all`

* Description: Get all ingredients of a recipe
* Permission: Not required
* Parameters:
  * `id` (**integer**: required): id of the recipe you want to get ingredients.
* Request example:

```bash
curl 'http://localhost:8000/recipes/1/ingredients/all'
```

* Response example:

```json
{
  "ingredients": [
    {
      "id": 1,
      "name": "Apple",
      "description": "Very delicous apple",
      "image_uri": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6",
      "likes": 0,
      "recipes": [
        {
          "id": 1,
          "name": "Apple pie",
          "description": "Very delicous apple pie",
          "image_uri": "https://images.unsplash.com/photo-1562007908-17c67e878c88",
          "likes": 0
        }
      ]
    },
    {
      "id": 2,
      "name": "Flour",
      "description": "Very expensive flour",
      "image_uri": "https://images.unsplash.com/photo-1627485937980-221c88ac04f9",
      "likes": 0,
      "recipes": [
        {
          "id": 1,
          "name": "Apple pie",
          "description": "Very delicous apple pie",
          "image_uri": "https://images.unsplash.com/photo-1562007908-17c67e878c88",
          "likes": 0
        }
      ]
    }
  ],
  "total": 2
}
```

#### `GET /recipes/<id>/ingredients`

* Description: Get ingredients of a recipe with pagination.
* Permission: Not required
* Parameters:
  * `id` (**integer**: required): id of the recipe you want to get ingredients.
* Query parameters:
  * `per_page` (**integer**: optional, **default**: 30): maximum how many ingredients you want to receive in your response.
  * `page`: (**integer**: optional, **default**: 1): paginating ingredients response.
* Request example:

```bash
curl 'http://localhost:8000/recipes/1/ingredients/?per_page=1&page=2'
```

* Response example:

```json
{
  "ingredients": [
    {
      "id": 2,
      "name": "Flour",
      "description": "Very expensive flour",
      "image_uri": "https://images.unsplash.com/photo-1627485937980-221c88ac04f9",
      "likes": 0,
      "recipes": [
        {
          "id": 1,
          "name": "Apple pie",
          "description": "Very delicous apple pie",
          "image_uri": "https://images.unsplash.com/photo-1562007908-17c67e878c88",
          "likes": 0
        }
      ]
    }
  ],
  "page": 2,
  "per_page": 1,
  "total": 2
}
```

#### `POST /recipes/<id>/ingredients`

* Description: Add ingredients into recipe.
* Permission: **update recipe**.
* Parameters:
  * `id` (**integer**: required): id of the recipe you want to add ingredients.
* Request body:
  * `ingredients` (**array of integer**: required): ingredient's ids you want to add to the recipe.
* Request example:
refer to [credientials](./credentials) for token.

```bash
curl -X POST 'http://localhost:8000/recipes/1/ingredients/' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <token>' \
  -d '{"ingredients":[1,2,3]}'
```

* Response example:

```json
{
  "id": 1,
  "name": "Apple pie",
  "description": "Very delicous apple pie",
  "image_uri": "https://images.unsplash.com/photo-1562007908-17c67e878c88",
  "ingredients": [
    {
      "id": 1,
      "name": "Apple",
      "description": "Very delicous apple",
      "image_uri": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6",
      "likes": 0
    },
    {
      "id": 2,
      "name": "Flour",
      "description": "Very expensive flour",
      "image_uri": "https://images.unsplash.com/photo-1627485937980-221c88ac04f9",
      "likes": 0
    },
    {
      "id": 3,
      "name": "Orange",
      "description": "Very delicous orange",
      "image_uri": "https://images.unsplash.com/photo-1582979512210-99b6a53386f9",
      "likes": 0
    }
  ],
  "likes": 0
}
```

#### `PATCH /recipes/<id>/ingredients`

* Description: Update ingredients of a recipe.
* Permission: **update recipe**.
* Parameters:
  * `id` (**integer**: required): id of the recipe you want to update ingredients.
* Request body:
  * `ingredients` (**array of integer**: required): ingredient's ids you want to update into the recipe.
* Request example:
refer to [credientials](./credentials) for token.

```bash
curl -X PATCH 'http://localhost:8000/recipes/1/ingredients/' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <token>' \
  -d '{"ingredients":[1,2]}'
```

* Response example:

```json
{
  "id": 1,
  "name": "Apple pie",
  "description": "Very delicous apple pie",
  "image_uri": "https://images.unsplash.com/photo-1562007908-17c67e878c88",
  "ingredients": [
    {
      "id": 1,
      "name": "Apple",
      "description": "Very delicous apple",
      "image_uri": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6",
      "likes": 0
    },
    {
      "id": 2,
      "name": "Flour",
      "description": "Very expensive flour",
      "image_uri": "https://images.unsplash.com/photo-1627485937980-221c88ac04f9",
      "likes": 0
    },
  ],
  "likes": 0
}
```

#### `DELETE /recipes/<id>/ingredients/<ingredient_id>`

* Description: Delete ingredient from a recipe.
* Permission: **update recipe**.
* Parameters:
  * `id` (**integer**: required): id of the recipe you want to delete ingredient.
  * `ingredient_id` (**integer**: required): id of the ingredient.
* Request example:
refer to [credientials](./credentials) for token.

```bash
curl -X DELETE 'http://localhost:8000/recipes/1/ingredients/2' \
  -H 'Authorization: Bearer <token>'
```

* Response example:

```json
{
  "id": 1,
  "name": "Apple pie",
  "description": "Very delicous apple pie",
  "image_uri": "https://images.unsplash.com/photo-1562007908-17c67e878c88",
  "ingredients": [
    {
      "id": 1,
      "name": "Apple",
      "description": "Very delicous apple",
      "image_uri": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6",
      "likes": 0
    }
  ],
  "likes": 0
}
```

### Ingredients

#### `GET /ingredients/all`

* Description: Get all ingredients in the database.
* Permission: Not required
* Request example:

```bash
curl 'http://localhost:8000/ingredients/all'
```

* Response example:

```json
{
  "ingredients": [
    {
      "id": 4,
      "name": "Pumpkin",
      "description": "Very delicous pumpkin",
      "image_uri": "https://images.unsplash.com/photo-1570586437263-ab629fccc818",
      "likes": 0,
      "recipes": [
        {
          "id": 3,
          "name": "Pumpkin soup",
          "description": "Very delicous pumpkin soup",
          "image_uri": "https://images.unsplash.com/photo-1476718406336-bb5a9690ee2a",
          "likes": 0
        }
      ]
    }
  ],
  "total": 1
}
```

#### `GET /ingredients`

* Description: Get ingredients from the database with pagination.
* Permission: Not required
* Query parameters:
  * `per_page` (**integer**: optional, **default**: 12): maximum how many ingredients you want to receive in your response.
  * `page`: (**integer**: optional, **default**: 1): paginating ingredients response.
* Request example:

```bash
curl 'http://localhost:8000/ingredients/?per_page=2&page=2'
```

* Response example:

```json
{
  "ingredients": [
    {
      "id": 3,
      "name": "Orange",
      "description": "Very delicous orange",
      "image_uri": "https://images.unsplash.com/photo-1582979512210-99b6a53386f9",
      "likes": 0,
      "recipes": [
        {
          "id": 2,
          "name": "Orange juice",
          "description": "Very delicous orange juice",
          "image_uri": "https://images.unsplash.com/photo-1613478223719-2ab802602423",
          "likes": 1
        }
      ]
    },
    {
      "id": 4,
      "name": "Pumpkin",
      "description": "Very delicous pumpkin",
      "image_uri": "https://images.unsplash.com/photo-1570586437263-ab629fccc818",
      "likes": 0,
      "recipes": [
        {
          "id": 3,
          "name": "Pumpkin soup",
          "description": "Very delicous pumpkin soup",
          "image_uri": "https://images.unsplash.com/photo-1476718406336-bb5a9690ee2a",
          "likes": 0
        }
      ]
    }
  ],
  "page": 2,
  "per_page": 2,
  "total": 4
}
```

#### `GET /ingredients/<id>`

* Description: Get specific ingredient from database.
* Permission: Not required
* Parameters:
  * `id` (**integer**: required): id of the ingredient you want to get.
* Request example:

```bash
curl 'http://localhost:8000/ingredients/2'
```

* Response example:

```json
{
  "id": 2,
  "name": "Flour",
  "description": "Very expensive flour",
  "image_uri": "https://images.unsplash.com/photo-1627485937980-221c88ac04f9",
  "likes": 0,
  "recipes": [
    {
      "id": 1,
      "name": "Apple pie",
      "description": "Very delicous apple pie",
      "image_uri": "https://images.unsplash.com/photo-1562007908-17c67e878c88",
      "likes": 0,
    }
  ]
}
```

#### `POST /ingredients`

* Description: Create new ingredient.
* Permission: **create ingredient**.
* Request body:
  * `name` (**string**: required): name of the ingredient.
  * `description` (**string**: optional): description of the ingredient.
  * `image_uri`: (**string**: optional): url of the ingredient.
* Request example:
refer to [credientials](./credentials) for token.

```bash
curl -X POST 'http://localhost:8000/ingredients/' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <token>' \
  -d '{"name":"my ingredient", "description":"my description", "image_uri":"https://picsum.photos/200"}'
```

* Response example:

```json
{
  "id": 5
}
```

#### `PATCH /ingredients/<id>`

* Description: Update ingredient information.
* Permission: **update ingredient**.
* Parameters:
  * `id` (**integer**: required): id of the ingredient you want to update.
* Request body:
  * `name` (**string**: optional): new name of the ingredient.
  * `description` (**string**: optional): new description of the ingredient.
  * `image_uri`: (**string**: optional): new url of the ingredient.
* Request example:
refer to [credientials](./credentials) for token.

```bash
curl -X PATCH 'http://localhost:8000/ingredients/4' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <token>' \
  -d '{"name":"my new ingredient", "description":"my new description", "image_uri":"https://picsum.photos/300"}'
```

* Response example:

```json

{
  "id": 4,
  "name": "my new ingredient",
  "description": "my new description",
  "image_uri": "http://your-ingredient-image-url-in-fileserver",
  "likes": 0,
  "recipes": [
    {
      "id": 3,
      "name": "Pumpkin soup",
      "description": "Very delicous pumpkin soup",
      "image_uri": "https://images.unsplash.com/photo-1476718406336-bb5a9690ee2a",
      "likes": 0
    }
  ]
}
```

#### `DELETE /ingredients/<id>`

* Description: Delete ingredient.
* Permission: **delete ingredient**.
* Parameters:
  * `id` (**integer**: required): id of the ingredient you want to delete.
* Request example:
refer to [credientials](./credentials) for token.

```bash
curl -X DELETE 'http://localhost:8000/ingredients/5' \
  -H 'Authorization: Bearer <token>'
```

* Response example:

```json
{
  "id": 5
}
```

#### `POST /ingredients/<id>/like`

* Description: Like ingredient.
* Permission: Not required.
* Parameters:
  * `id` (**integer**: required): id of the ingredient you want to like.
* Request example:

```bash
curl -X POST 'http://localhost:8000/ingredients/2/like'
```

* Response example:

```json
{
  "id": 2,
  "total_likes": 2
}
```

### Errors

#### 404 Not Found

* Description: get recipe or ingredient which does not exist in database.
* Reponse:

```json
{
  "code": 404,
  "message": "Resources not found."
}
```

#### 401 Unauthorized

* Description: Attempt to create/update/delete resource without logging in.
* Request example:

```bash
curl -X POST 'http://localhost:8000/recipes/' \
  -H 'Content-Type: application/json' \
  -d '{"name":"my recipe", "description":"my description", "image_uri":"https://picsum.photos/200"}'
```

* Reponse:

```json
{
  "code": 401,
  "message": "Unauthorized."
}
```

#### 403 Forbidden

* Description: Attempt to manipulate resource with different permission.
* Request example:
refer to [credientials](./credentials) for menu manager's token.

```bash
curl -X DELETE 'http://localhost:8000/recipes/4' \
  -H 'Authorization: Bearer <menu-manager-token>'
```

* Reponse:

```json
{
  "code": 403,
  "message": "Forbidden."
}
```

#### 422 Unprocessable

* Description: Request with incorrect resource, e.g: create recipe without name.
* Request example:
refer to [credientials](./credentials) for token.

```bash
curl -X POST 'http://localhost:8000/recipes/' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <token>' \
  -d '{"name":"", "description":"my description", "image_uri":"https://picsum.photos/200"}'
```

* Reponse:

```json
{
  "code": 422,
  "message": "Invalid name."
}
```

#### 415 Unsupported Media Type

* Description: Request with invalid resource, e.g: create recipe using invalid image.
* Request example:
refer to [credientials](./credentials) for token.

```bash
curl -X POST 'http://localhost:8000/recipes/' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <token>' \
  -d '{"name":"", "description":"my description", "image_uri":"https://example.com/"}'
```

* Reponse:

```json
{
  "code": 415,
  "message": "Invalid image."
}
```

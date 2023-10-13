# MaisTODOS backend python challenge

This is my implementation of the https://github.com/MaisTodos/backend-python-creditcard challenge

![Build status](https://github.com/Pacheco95/desafio-backend-python-creditcard/actions/workflows/python-app.yml/badge.svg)

# Requirements

[Docker engine](https://docs.docker.com/engine/)

# Usage

Start application

```shell
# In terminal 1
# Setup environment variables
cp env/.env.testing-compose .env

# Run API
docker compose up

# Keep terminal 1 open
```

Run tests

```shell
# In terminal 2
docker compose exec api make test
```

Stop application

```shell
# Ctrl-C on terminal 1 OR
docker compose stop # On terminal 2
```

Cleanup

```shell
docker compose down
```

# Interact with the API via Swagger

1. Create a user to access the protected endpoints
   1. Access [http://0.0.0.0:8000/docs#/Users/create_user_endpoint_users__post](http://0.0.0.0:8000/docs#/Users/create_user_endpoint_users__post)
   2. Click `Try it out`
   3. Paste `{ "username": "admin", "password": "admin" }` under `Request body` input
   4. Click `Execute`
2. Get authentication to access the endpoints:
   1. Go to page top
   2. Click `Authorize`
   3. Type `admin` in both `username` and `password` inputs
   4. Click `Authorize` and then `Close`
   5. Your authentication is set
3. Choose any Card endpoint to play with, for instance [List Cards](http://0.0.0.0:8000/docs#/Card/find_all_cards_by_id_endpoint_cards__get)
   1. Since there is no card created it will return an empty array
   2. Try to create different cards using the `POST` endpoint
   3. Try to create invalid cards bypassing the validations. TIP: go to page end and look for `CreateCard` under `Schemas`

# Decisions made

## REST Framework

I decided to use FastAPI due to its simplicity, flexibility, Pydantic native integration and performance.

## Database

I chose MongoDB because it's my favourite database and I have most dexterity with.

## Docker & Docker Compose

The entire application was configured to run inside docker compose to ensure correctness and reproducibility among
different platforms. The [docker-compose.yml](docker-compose.yml) file is configured to build the API using
the [Dockerfile](Dockerfile) and wires the database and the API in a network, so they can communicate without reaching
the external Internet.

The application configuration was done with environment variables.
I kept the JWT secret in an env var for sake of simplicity. I know it should be a compose secret.

## Authentication

The authentication was done using JWT tokens.
It's always a challenge to set up API authentication/authorization and I used
the [FlaskAPI guide](https://fastapi.tiangolo.com/tutorial/security/first-steps/) to get it done quickly.

If this was a more complex API that requires user permissions and a high rate of authentication/authorization requests,
I would probably use an external Keycloak server for those.

# Extra features

- Indexed audit fields `created_at` and `created_by` for cards.
- Paginated search for cards
- Migrations to create collections and indexes
- GitHub actions to run tests 

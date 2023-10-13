# MaisTODOS backend python challenge

This is my implementation of the https://github.com/MaisTodos/backend-python-creditcard challenge

```shell
# Setup environment variables
cp env/.env.testing-compose .env

# Run API
docker compose up

# Open another terminal session

# Run tests
docker compose exec api make test

# Stop
docker compose stop

# Cleanup
docker compose down
```

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

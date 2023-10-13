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

I decided to use FastAPI due to it's simplicity, flexibility, Pydantic native integration and performance.

## Database

I chose MongoDB because it's my favourite database and I have most dexterity with.

## Docker & Docker Compose

The entire application was configured to run inside docker compose to ensure correctness and reproducibility among
different platforms. The [docker-compose.yml](docker-compose.yml) file is configured to build the API using
the [Dockerfile](Dockerfile) and wires the database and the API in a network, so they can communicate without reaching
the external Internet.



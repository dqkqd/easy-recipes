# Easy-recipes

Easy-recipes is a web application which user can add / remove recipes of choices.

## Development

### Running tests

To run tests, [docker](https://docs.docker.com/engine/install/) and [docker compose](https://docs.docker.com/compose/install/) need to be installed.

Prepare test environment in detach mode, specified in `docker-compose.yml`.

```bash
docker compose up -d
```

Run tests suit.

```bash
docker compose exec server pytest
```

Stop docker compose:

```bash
docker compose stop
```

# Local Stack and Seed Data

> Fictional company and content, created for the Ramp-Up Assistant PoC.

Owner: Leo Novak (Platform Engineer, maintains Ladle) · Also ask: Priya Raman (Tech Lead, Platform)

## What `ladle up` starts

`ladle up` reads the `ladle.yaml` file in the repo and starts the service plus its dependencies with Docker Compose:

| Container | Port | Notes |
|---|---|---|
| Postgres 16 | 5432 | One database per service, user `dev`, password in 1Password ("Local dev Postgres") |
| Redis 7 | 6379 | Caching and rate limiting |
| Kafka (Redpanda) | 9092 | Local Conveyor, topics are created automatically |
| The service itself | 8080 | Hot reload is on by default |

Run `ladle up --with orders-service` to also start another service, for example when testing Autopilot, which needs both Stock and Orders.

## Seed data

`ladle seed` loads a demo customer, "Golden Crust Bakery", with three venues, about 200 SKUs, two suppliers and a month of stock movements. The demo login for Counter is `demo@goldencrust.example` with the password stored in 1Password ("Counter demo user").

To reset everything, run `ladle down --volumes` and then `ladle up` and `ladle seed` again.

## Running tests

- Unit tests: `ladle test` (runs `pytest` inside the container).
- A single test file: `ladle test tests/test_par_levels.py`.
- Integration tests need the full local stack running: `ladle test --integration`.

## Common problems

### Port already in use

Another stack is still running. Run `ladle ps` to see it and `ladle down` in that repo.

### Kafka container keeps restarting

Docker Desktop needs at least 6 GB of memory for the full stack. Increase it under Settings → Resources.

### Seed fails with "relation does not exist"

The database migrations did not run. Run `ladle migrate` and then `ladle seed` again.

# Backend Service Conventions

> Fictional company and content, created for the Ramp-Up Assistant PoC.

Owner: Ana Ribeiro (Tech Lead, Stock) · Also ask: Jonas Weber (Tech Lead, Orders)

Every Python service follows the same layout, so you can find your way around any of them. `stock-service` is the reference implementation.

## Folder structure

```
stock-service/
├── app/
│   ├── api/            # FastAPI routers, request/response schemas (Pydantic)
│   ├── domain/         # Business logic, no database or HTTP code here
│   ├── repositories/   # Database access with SQLAlchemy
│   ├── events/         # Conveyor producers and consumers
│   ├── jobs/           # Celery tasks
│   ├── settings.py     # Configuration, read from environment variables
│   └── main.py         # App factory
├── migrations/         # Alembic migrations
├── tests/
│   ├── unit/
│   └── integration/
├── ladle.yaml          # Local stack definition used by `ladle up`
└── pyproject.toml
```

## Layering rules

- Routers in `api/` only validate input, call the domain layer and map the result to a response. No business logic in routers.
- The `domain/` layer never imports FastAPI or SQLAlchemy. It receives repositories as arguments, which keeps it easy to unit test.
- Only `repositories/` talks to the database.

## Configuration

Settings are read from environment variables through a Pydantic `Settings` class in `settings.py`. Locally, Ladle injects them from `ladle.yaml`. In Kubernetes they come from the Helm chart, and secrets come from AWS Secrets Manager. Never commit secrets; for local development use the values in 1Password.

## Publishing events

Services publish events with the **outbox pattern**: the event is written to an `outbox` table in the same database transaction as the business change, and a background worker sends it to Conveyor. This guarantees we never publish an event for a change that was rolled back. Use `larderly_common.conveyor.publish()`, which handles the outbox for you; never call the Kafka producer directly.

## Errors and logging

- Raise the domain exceptions from `larderly_common.errors` (`NotFound`, `Conflict`, `ValidationFailed`). The common error handler turns them into consistent JSON error responses.
- Log with `structlog` through `larderly_common.logging`. Always log structured fields (`logger.info("po_submitted", po_id=po.id)`), not formatted strings.
- Never log customer personal data (emails, phone numbers, addresses).

## Testing

- **Unit tests** cover the `domain/` layer and run without Docker. Aim for these to be most of your tests.
- **Integration tests** run against the real Postgres, Redis and Kafka from `ladle up` and cover repositories, routers and event consumers.
- Test data is built with factories from `tests/factories.py` (factory_boy), not with fixtures copied between tests.
- New code needs tests; CI fails if coverage of the changed lines is below 80%.

## API design

- REST with JSON, resource names in plural (`/venues/{id}/skus`).
- Every list endpoint is paginated with `limit` and `cursor`.
- Breaking API changes need a new version prefix (`/v2/`) and an RFC, because the mobile app cannot force users to update immediately.

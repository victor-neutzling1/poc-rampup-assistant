# Repository Map and Tech Stack

> Fictional company and content, created for the Ramp-Up Assistant PoC.

Owner: Priya Raman (Tech Lead, Platform) · Also ask: Daniel Hughes (Engineering Manager, Platform)

All code lives in the `larderly` GitHub organization. We use one repository per service (polyrepo), plus a few shared repos. `ladle clone all` clones the repos your squad needs.

## Tech stack at a glance

| Layer | Technology |
|---|---|
| Backend services | Python 3.12, FastAPI, SQLAlchemy 2, Alembic, Pydantic 2 |
| Background jobs | Celery workers with Redis as broker |
| Events | Conveyor (Kafka), schemas in Avro |
| Databases | PostgreSQL 16 (one per service), Redis 7 for caching |
| Web frontend | React 18, TypeScript, Vite, TanStack Query, React Router |
| Mobile | React Native with Expo, TypeScript, WatermelonDB for offline storage |
| Design system | Whisk (React components + design tokens) |
| Infrastructure | AWS (EKS, RDS, S3, MSK), Terraform, Helm charts, Argo CD |
| Observability | Datadog (logs, APM, metrics), Sentry for frontend errors |
| CI | GitHub Actions with shared workflows |

## Service repositories

| Repo | Owner squad | Notes |
|---|---|---|
| `gateway` | Platform | API gateway, authentication, rate limiting |
| `stock-service` | Stock | Stock counts, batches, PAR levels, wastage |
| `orders-service` | Orders | Purchase orders, supplier catalogues, Autopilot |
| `supplier-gateway` | Orders | Delivers POs to suppliers (email, EDI, supplier APIs) |
| `notifications` | Platform | Email (SES), push (Firebase), SMS (Twilio) |
| `reporting` | Stock | Weekly reports and exports to Cellar |

## Frontend repositories

| Repo | Owner squad | Notes |
|---|---|---|
| `counter-web` | Counter Web | The Counter dashboard |
| `kitchen-mobile` | Kitchen Mobile | The Kitchen app for iOS and Android |
| `whisk` | Counter Web | Design system, published as `@larderly/whisk` |

## Shared repositories

| Repo | What it contains |
|---|---|
| `larderly-common` | Shared Python package: logging setup, auth helpers, Conveyor producer/consumer, test fixtures |
| `conveyor-schemas` | Avro schemas for every event, with compatibility checks in CI |
| `platform-workflows` | Reusable GitHub Actions workflows used by every repo |
| `infra` | Terraform for AWS and Helm charts for each service |
| `ladle` | The Ladle CLI source |
| `handbook` | Source of the engineering handbook (these docs) |

## Where to start reading code

If you join Stock or Orders, start with `stock-service`: it is the oldest service and the reference for our backend conventions. If you join Counter Web, start with `counter-web/src/features/stock-counts`, which is the most recently refactored feature and follows the current frontend conventions.

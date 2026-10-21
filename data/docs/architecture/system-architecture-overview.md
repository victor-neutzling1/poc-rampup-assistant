# System Architecture Overview

> Fictional company and content, created for the Ramp-Up Assistant PoC.

Owner: Jonas Weber (Tech Lead, Orders) · Also ask: Ana Ribeiro (Tech Lead, Stock)

## Big picture

Larderly is a set of Python services behind an API gateway, a React web app (Counter) and a React Native mobile app (Kitchen). Services talk to each other mostly through events on Conveyor (Kafka) and only call each other synchronously when they need an immediate answer.

Everything runs on Kubernetes (AWS EKS) in the `eu-west-1` region, with one cluster per environment.

## Services

| Service | Squad | Responsibility |
|---|---|---|
| `gateway` | Platform | Authentication (Okta for staff, Auth0 for customers), routing, rate limits |
| `stock-service` | Stock | SKUs, stock counts, batches, PAR levels, wastage |
| `orders-service` | Orders | Purchase orders, supplier catalogues, Autopilot |
| `supplier-gateway` | Orders | Sends POs to suppliers by email, EDI or supplier API |
| `notifications` | Platform | Email, push and SMS |
| `reporting` | Stock | Weekly wastage reports, exports to Cellar |

Each service owns its own Postgres database. Never read another service's database directly; use its API or subscribe to its events.

## Key events on Conveyor

- `stock.count.recorded` – a staff member finished a stock count.
- `stock.below_par` – a SKU dropped below its PAR level. Autopilot listens to this to create draft POs.
- `order.submitted` – a kitchen manager submitted a PO.
- `order.delivered` – a delivery was received in the Kitchen app; Stock adds the new batches.

Event schemas live in the `conveyor-schemas` repo. A schema change needs an RFC if another squad consumes the event.

## Frontends

- **Counter** (`counter-web`) – React + TypeScript, built with Vite, uses the Whisk design system.
- **Kitchen** (`kitchen-mobile`) – React Native app for iOS and Android. It works offline and syncs stock counts when the connection comes back.

## Making changes across services

If your change touches more than one squad's service or an event used by another squad, write a short RFC in Confluence (template: Engineering → RFCs) and bring it to the Tuesday architecture office hours.

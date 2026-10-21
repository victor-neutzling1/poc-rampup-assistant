# Glossary

> Fictional company and content, created for the Ramp-Up Assistant PoC.

Owner: Camille Martin (Engineering Onboarding Lead) · Also ask: Lucía Fernández (Product Manager, Orders)

Words and acronyms you will hear in your first weeks at Larderly.

## Business terms

- **SKU** – Stock Keeping Unit. One sellable or usable item, e.g. "Flour T55, 25 kg bag".
- **PAR level** – The minimum quantity of a SKU a kitchen wants on hand. When stock drops below PAR, Larderly suggests a reorder.
- **PO** – Purchase Order sent to a supplier.
- **FIFO** – First In, First Out. Older stock is used first; the Stock service tracks batches to support it.
- **Wastage** – Stock thrown away (expired, damaged). Reported weekly to customers.
- **Venue** – One physical restaurant or bakery. A customer account can own many venues.
- **Supplier catalogue** – The list of products and prices a supplier offers to a venue.

## Product names

- **Counter** – The web dashboard used by kitchen managers.
- **Kitchen** – The mobile app used by staff to count stock and receive deliveries.
- **Autopilot** – The feature that creates draft purchase orders automatically when stock drops below PAR.

## Internal names

- **Whisk** – Our React design system (components, colours, icons). Lives in the `whisk` repo.
- **Conveyor** – The Kafka-based event bus that services use to publish and consume events.
- **Cellar** – The data warehouse used for reporting and analytics.
- **Pantry** – The internal admin tool used by Support to look up customers and venues.
- **Ladle** – Our CLI for developer tasks (`ladle up`, `ladle seed`, `ladle logs`).

## Engineering terms

- **RFC** – Request for Comments. A short design document required for changes that affect more than one squad.
- **DRI** – Directly Responsible Individual. The one person accountable for a task or incident.
- **SEV1 / SEV2 / SEV3** – Incident severity levels, see the observability and on-call guide.
- **Bake time** – How long a release sits in staging before it can go to production (24 hours).

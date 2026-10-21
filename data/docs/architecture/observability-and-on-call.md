# Observability and On-call

> Fictional company and content, created for the Ramp-Up Assistant PoC.

Owner: Daniel Hughes (Engineering Manager, Platform) · Also ask: Priya Raman (Tech Lead, Platform)

## Logs, metrics and traces

Everything is in **Datadog**:

- Logs: filter by `service:<name>` and `env:<dev|staging|prod>`.
- APM traces: every request through `gateway` has a trace ID, returned in the `X-Trace-Id` response header. Search for it in Datadog to follow a request across services.
- Each squad has a dashboard named "<Squad> – Service health".

Production logs are only visible after you complete the "Secure Development Basics" training. Customer personal data is masked in logs; never log email addresses or phone numbers in plain text.

## Joining on-call

Engineers join the on-call rotation after three months. First you shadow two full rotations (you get the pages but the primary handles them), then you become primary. Rotations are one week, Monday 10:00 to Monday 10:00 local time. Your manager adds you in PagerDuty.

## Incident severity

| Severity | Meaning | Response |
|---|---|---|
| SEV1 | Customers cannot place orders or count stock, or data loss | Page immediately, open an incident with `/incident sev1` in Slack |
| SEV2 | A major feature is degraded but there is a workaround | Open an incident, page outside business hours |
| SEV3 | Minor bug, few customers affected | Normal Jira ticket in the squad's project |

The person who opens the incident is the DRI until they hand it over explicitly.

## Runbooks

Every alert in PagerDuty links to a runbook in Confluence (Engineering → Runbooks). If you get paged for an alert without a runbook, write one after the incident.

## Postmortems

SEV1 and SEV2 incidents need a blameless postmortem within five business days, using the postmortem template in Confluence. Postmortems are reviewed in the monthly reliability review.

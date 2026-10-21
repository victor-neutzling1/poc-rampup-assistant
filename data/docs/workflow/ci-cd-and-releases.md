# CI/CD and Releases

> Fictional company and content, created for the Ramp-Up Assistant PoC.

Owner: Priya Raman (Tech Lead, Platform) · Also ask: Leo Novak (Platform Engineer)

## CI pipeline

Every pull request runs GitHub Actions with these jobs: `lint` → `unit-tests` → `integration-tests` → `build-image`. A full run takes about 12 minutes for backend services and 8 minutes for Counter Web.

The pipeline definition lives in `.github/workflows/ci.yml` in each repo and reuses shared workflows from the `platform-workflows` repo. Do not copy steps between repos; add them to the shared workflow instead.

## Environments

| Environment | Deployed when | URL |
|---|---|---|
| dev | Every merge to `main`, automatically | `*.dev.larderly.example` |
| staging | Every day at 14:00 UTC, the latest `main` is promoted | `*.staging.larderly.example` |
| production | Manually, after 24 hours of bake time in staging | `*.larderly.example` |

Deploys use Argo CD. You can see what version runs where in the Argo CD dashboard at `https://argo.larderly.example`.

## Production releases

Production deploys happen Monday to Thursday. There are no production deploys on Fridays or the day before a public holiday unless it is a hotfix.

To deploy, the squad's release captain (rotates every sprint) clicks **Promote to production** in Argo CD and posts the release notes in `#releases`.

## Hotfixes

1. Branch from `main`, fix, open a PR labelled `hotfix`.
2. After merge, the release captain promotes the build straight to production, skipping bake time.
3. Write a short note in `#releases` explaining what was fixed and why it could not wait.

## Feature flags

New customer-facing behaviour must ship behind a feature flag. Flags live in LaunchDarkly; ask your squad lead for access. Turn a flag on for internal venues first, then for 10% of customers, then everyone. Remove the flag within two sprints of full rollout.

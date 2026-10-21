# Git and Code Review

> Fictional company and content, created for the Ramp-Up Assistant PoC.

Owner: Daniel Hughes (Engineering Manager, Platform) · Also ask: Ana Ribeiro (Tech Lead, Stock)

## Branches

We use trunk-based development on `main`. Branch names follow `<jira-key>/<short-description>`, for example `STK-412/fix-par-rounding`. Keep branches short-lived: merge within a few days, and hide unfinished work behind a feature flag.

## Commits

Start the commit message with the Jira key: `STK-412: Round PAR levels to whole units`. The Jira integration links commits to the ticket automatically.

## Pull requests

- Open the pull request as a draft early if you want feedback.
- Fill in the template: what changed, why, how it was tested, and screenshots for UI changes.
- **One approval** is required, from someone in the code owners file of the repo. Changes to `infra/` or database migrations need a second approval from the Platform team.
- All CI checks must pass. If a test is flaky, do not just re-run until it passes: mark it with `@pytest.mark.flaky`, open a ticket, and mention it in the PR.
- We squash-merge. The PR title becomes the commit message, so keep the Jira key in it.

## Reviewing

- Review requests should get a first response within one business day.
- Prefix optional comments with `nit:`.
- If a thread goes back and forth more than three times, jump on a quick call and write the outcome in the PR.
- Approve with comments when the remaining points are small; trust the author to fix them before merging.

## Database migrations

Migrations use Alembic. Never edit a migration that has already been merged; create a new one instead. Migrations must be backwards compatible with the previous release, because the old version keeps running during a rolling deploy.

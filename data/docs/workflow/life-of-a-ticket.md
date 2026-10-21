# The Life of a Ticket

> Fictional company and content, created for the Ramp-Up Assistant PoC.

Owner: Marcus Webb (Engineering Manager, Stock and Counter Web) · Also ask: Grace Okafor (Engineering Manager, Orders and Kitchen Mobile)

This page walks through how a typical piece of work goes from the backlog to production, using an example ticket: `STK-412: Round PAR levels to whole units`.

## 1. Pick up the ticket

Take the next ticket from the top of the sprint board, assign it to yourself and move it to **In Progress**. If something in the ticket is unclear, ask the PM in the ticket comments, not in a private message, so the answer is recorded.

## 2. Create a branch

```bash
git checkout main
git pull
git checkout -b STK-412/round-par-levels
```

## 3. Build it

- Start the local stack with `ladle up` and load data with `ladle seed`.
- Write the tests together with the code. For a bug, write a failing test first.
- Commit in small steps; every commit message starts with the Jira key: `STK-412: Round PAR levels in domain layer`.
- If the change is user-facing, put it behind a feature flag so it can be merged before it is finished.

## 4. Open a pull request

```bash
git push -u origin STK-412/round-par-levels
```

Open the PR on GitHub, fill in the template (what, why, how it was tested, screenshots for UI) and move the ticket to **In Review**. Post the PR link in your squad channel so reviewers see it.

Keep PRs small: under 400 changed lines is a good target. Split bigger changes into several PRs that can be merged one after another.

## 5. Review

A code owner reviews within one business day. Answer every comment, either with a change or a short explanation. When you push changes after review, re-request the review on GitHub so the reviewer is notified.

### Resolving merge conflicts

If `main` moved on and your branch has merge conflicts, rebase it onto the latest `main`, fix the conflicts, and push:

```bash
git fetch origin
git rebase origin/main
git push --force-with-lease
```

Use `--force-with-lease`, never plain `--force`, so you don't overwrite someone else's commits.

## 6. Merge and deploy to dev

Once approved and CI is green, squash-merge the PR. GitHub deletes the branch automatically. The change deploys to **dev** within about 15 minutes; check it there.

## 7. Staging and production

The change reaches **staging** at the next daily promotion (14:00 UTC), and production after 24 hours of bake time when the release captain promotes it. Check that it works in staging, especially if it touches other services.

## 8. Done

Move the ticket to **Done** only when the change is running in production and, if it was behind a flag, the flag is on for at least internal venues.

### Definition of Done

- Code merged, with tests, and CI green.
- Deployed to production.
- Documentation updated if behaviour or setup changed (including this handbook).
- Feature flag created and rollout plan written for user-facing changes.
- Product Manager has seen it for user-facing changes.

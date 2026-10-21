# Branching Strategy in Practice

> Fictional company and content, created for the Ramp-Up Assistant PoC.

Owner: Daniel Hughes (Engineering Manager, Platform) · Also ask: Priya Raman (Tech Lead, Platform)

We use trunk-based development: `main` is always deployable, and everyone merges small changes into it often. This page covers the cases the basic rules in Git and Code Review don't.

## Branch types

| Prefix | When | Example |
|---|---|---|
| `<jira-key>/` | All normal work | `ORD-288/autopilot-local-flag` |
| `hotfix/<jira-key>-` | Urgent production fix | `hotfix/STK-530-negative-stock` |
| `chore/` | Dependency bumps, config, no ticket needed | `chore/bump-fastapi` |
| `spike/` | Experiments that will not be merged | `spike/try-pgvector` |

There are no long-lived `develop` or `release` branches. Releases are Docker images built from `main`, tagged with the commit SHA, and promoted through the environments by Argo CD.

## Unfinished work

Never keep a branch open for weeks waiting for a feature to be complete. Merge each piece behind a feature flag instead. A branch older than five working days usually means the work should be split.

## Stacked pull requests

When a change needs several PRs that build on each other (for example: migration → repository → API), you can stack them: branch the second PR from the first one and set its base branch to the first branch on GitHub. After the first PR is merged, GitHub retargets the next one to `main`. Mention the stack order in each PR description.

## Hotfix flow

1. Branch from `main` with the `hotfix/` prefix.
2. Open the PR with the `hotfix` label; one approval is still required.
3. After merging, the release captain promotes the build straight to production (see CI/CD and Releases).

Because `main` is always deployable, there is no separate release branch to patch: the hotfix goes to production together with anything else already merged. If `main` contains something that must not go out yet, it should already be behind a feature flag.

## Reverting

If a merged change breaks something, revert first and investigate after:

```bash
git revert <merge-commit-sha>
```

Open the revert as a normal PR with the `revert` label and post it in your squad channel. Reverts get reviewed before any other PR, and if the change caused a SEV1 or SEV2, the release captain promotes the revert straight to production like a hotfix.

## Branch protection

`main` is protected in every repo: no direct pushes, at least one approval from a code owner, all required checks green, and the branch must be up to date with `main` before merging.

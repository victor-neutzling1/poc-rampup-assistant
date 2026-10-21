# Development Environment Setup

> Fictional company and content, created for the Ramp-Up Assistant PoC.

Owner: Priya Raman (Tech Lead, Platform) · Also ask: Felipe Moreira (IT Lead)

This guide gets you from a fresh laptop to a running local stack. Budget half a day. If you get stuck for more than 30 minutes, ask in `#eng-help`.

## VPN (Tailscale)

Internal tools (Pantry, the package registry, staging) are only reachable through Tailscale.

1. Install Tailscale from the self-service app (macOS: "Self Service", Windows: "Company Portal").
2. Sign in with Okta.
3. Check that it works by opening `https://pantry.larderly.example`.

Tailscale runs in split mode: only internal traffic goes through it.

## Tools to install

| Tool | Version | Notes |
|---|---|---|
| Git | latest | |
| Docker Desktop | latest | Licence is assigned automatically through Okta. Sign in with your work account. |
| Python | 3.12 | Use `pyenv`. All backend services pin their version in `.python-version`. |
| Node.js | 18 | Use `nvm`. Needed for the Counter web app and Whisk. |
| Ladle CLI | latest | `brew install larderly/tap/ladle` (macOS) or `scoop install ladle` (Windows) |

On Windows, do everything inside **WSL2 (Ubuntu)**. The services do not build natively on Windows.

## GitHub access

1. Accept the invite to the `larderly` GitHub org (sent to your work email).
2. Create an SSH key: `ssh-keygen -t ed25519 -C "you@larderly.example"`.
3. Add it in GitHub under Settings → SSH and GPG keys, then click **Configure SSO** next to the key and authorize the `larderly` org. Without the SSO step, cloning fails with "repository not found".

## Private packages

Our internal Python and npm packages are published to the package registry at `https://packages.larderly.example`.

1. Log in with `ladle auth login`. It opens Okta in your browser.
2. Ladle writes the credentials to `~/.pypirc` and `~/.npmrc` for you.

If `pip install` or `npm install` returns 401 or 403, run `ladle auth login` again; the token expires every 30 days.

## Clone and start

```bash
mkdir -p ~/code && cd ~/code
ladle clone all        # clones every service repo your squad needs
cd stock-service
ladle up               # starts Postgres, Redis, Kafka and the service in Docker
ladle seed             # loads demo data, see the local stack guide
```

Open `http://localhost:8080/health`. You should see `{"status": "ok"}`.

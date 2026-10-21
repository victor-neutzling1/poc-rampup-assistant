# Welcome to Larderly Engineering

> Fictional company and content, created for the Ramp-Up Assistant PoC.

Owner: Camille Martin (Engineering Onboarding Lead) · Also ask: Felipe Moreira (IT Lead)

Larderly builds software that helps restaurants and bakeries track their stock and reorder from suppliers before they run out. Engineering is about 60 people in four product squads (Stock, Orders, Counter Web, Kitchen Mobile) plus the Platform team.

## Your first day

1. Pick up your laptop from IT (MacBook Pro, or a Windows laptop if you asked for one in your offer form).
2. Sign in with the temporary password in your welcome email and set up **Okta** with the Okta Verify app. Okta is the single sign-on for everything else.
3. Open Slack and join `#eng-general`, `#eng-help`, `#it-helpdesk` and your squad channel.
4. Meet your **onboarding buddy**. Your manager assigns one before you start; they are your first stop for any question during your first month.

## Accounts and access

Most access is granted automatically through Okta groups when your manager submits the "New engineer" form. Allow up to one business day.

| Tool | What for | How you get it |
|---|---|---|
| GitHub (`larderly` org) | Source code | Automatic via Okta. Accept the org invite email within 7 days or it expires. |
| Jira | Tickets and sprints | Automatic via Okta |
| Confluence | Docs | Automatic via Okta |
| 1Password | Shared secrets and dev credentials | Invite from IT on day one |
| Tailscale | VPN into internal tools | Automatic via Okta, see the dev environment setup guide |
| Datadog | Logs, metrics, dashboards | Read-only for everyone; request write access in `#platform` |
| PagerDuty | On-call | Added by your manager when you join the rotation |

If something is still missing after one business day, post in `#it-helpdesk` with the tool name and your manager's name.

## Your first week checklist

- Set up your development environment and run the local stack.
- Read the system architecture overview and the glossary.
- Pair with your buddy on at least one small ticket labelled `good-first-ticket` in your squad's Jira board.
- Open your first pull request by the end of the week. It can be small; the goal is to go through the whole review and deploy flow once.
- Attend the Thursday **Engineering Show & Tell** (16:00 UTC), where squads demo what they shipped.

## Security training

Complete the "Secure Development Basics" course in the learning portal during your first two weeks. Access to production logs in Datadog and to the on-call rotation is only granted after the course is completed.

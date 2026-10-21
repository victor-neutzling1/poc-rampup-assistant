# How We Run Scrum

> Fictional company and content, created for the Ramp-Up Assistant PoC.

Owner: Grace Okafor (Engineering Manager, Orders and Kitchen Mobile) · Also ask: Marcus Webb (Engineering Manager, Stock and Counter Web)

This page explains how squads plan and track work. For the meeting times, see Team Rituals and Communication.

## Squad roles

| Role | Responsibility |
|---|---|
| Product Manager (PM) | Owns the backlog and decides priorities |
| Engineering Manager (EM) | People management, hiring, delivery health; usually manages one or two squads |
| Tech Lead | Technical direction of the squad, reviews designs and RFCs |
| Engineers | Build, test and ship; everyone does code review and takes part in estimation |
| Designer | Shared between squads; joins refinement when UI work is involved |

There is no dedicated Scrum Master. The EM facilitates planning and the retro rotates between engineers.

## Backlog refinement

Refinement happens every Thursday at 14:00 local time (1 hour). The PM brings the next priorities and the squad:

1. Clarifies the problem and acceptance criteria.
2. Splits work that is too big for one sprint.
3. Estimates with **planning poker** in story points (1, 2, 3, 5, 8, 13). Anything estimated at 13 must be split before it goes into a sprint.

### Definition of Ready

A ticket can enter a sprint when it has: a clear description of the problem, acceptance criteria, an estimate, designs attached for UI work, and no open dependency on another squad (or the dependency has been agreed with that squad).

## Sprint planning

At planning the squad agrees on a **sprint goal**: one or two sentences describing what the sprint should achieve. The squad pulls tickets from the top of the refined backlog until it reaches its average velocity of the last three sprints. New engineers count as half capacity during their first sprint.

About 20% of each sprint is reserved for tech debt and maintenance. The tech lead chooses those tickets.

## During the sprint

- Keep work in progress low: one ticket in progress per engineer, two at most if one is waiting for review.
- If you are blocked, add the `blocked` flag to the ticket and say so at stand-up. Do not wait until the next day if the blocker stops all your work.
- Unplanned urgent work (production bugs) goes in only with the PM's agreement, and something of similar size comes out.

## Bug triage

Each squad has a rotating **bug shield**: one engineer per sprint who triages incoming bugs, fixes small ones and handles questions from Support in `#support-escalations`. The bug shield takes fewer sprint tickets so they have room for this.

## Sprint review and retro

At the review, the squad demos finished work to the PM and anyone interested. Only tickets that are deployed to production count as done.

Retros use a different format each time (Start/Stop/Continue, Mad/Sad/Glad, sailboat). Each retro ends with at most two action items, each with an owner, which are reviewed at the start of the next retro.

## Quarterly planning

Every quarter, squads present their roadmap for the next three months at the quarterly planning day. Cross-squad dependencies are identified there and recorded as linked epics in Jira.

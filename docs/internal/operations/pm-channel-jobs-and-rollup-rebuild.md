# PM channel: who writes what, and how to rebuild the rollup if Exec is dark

*Written 2026-10-03 by Exec (settles Spec R4(c) with CIO). Status: PROPOSED, one line per owner to confirm; no new rule beyond naming each artifact's job.*

## 1. Four artifacts, four jobs

| Artifact | Job (one line) | Owner | Reader |
|---|---|---|---|
| **Omnibus log** | What happened yesterday, from the session logs | Docs | Any agent, Janus |
| **BRIEFING-CURRENT-STATE** | What a new or resumed agent must know to work today | Docs (any seat may refresh a stale one) | Agents |
| **Weekly Ship** | The public account of the week | Comms | The public, PM |
| **Attention rollup** (`dev/active/exec-attention-rollup-current.html`) | What PM must decide or know now, with 🔒 on what is blocked on PM | Exec | PM, Janus |

A fact belongs in the artifact whose job it is; the others link to it instead of restating it.

## 2. Rebuilding the rollup if Exec is dark

The rollup is a committed file on `origin/main` with a Verified-how footer, so any seat can rebuild it. **First backup: CIO.** Steps:

1. `git fetch` + fast-forward; read `dev/active/exec-carry-forward.md` (PM-attention items) and `mailboxes/exec/inbox/` (messages marked decision / ruling-relay / contradiction).
2. Follow `.claude/skills/cohort-attention-rollup/SKILL.md` (verifies every item against GitHub rather than a local doc).
3. Live numbers, each quoted with its command, never carried over: `python3 scripts/sprint-truth.py --no-snapshot`; `gh run list --workflow test.yml --branch main --limit 10` (check `createdAt` is recent); latest `dev/heartbeats/usage-per-account.tsv` row for the account; `python3 scripts/rollup-calendar-scan.py`; `python3 scripts/served-model-by-seat.py` when model claims appear.
4. Keep: needs-you items first, 🔒 + date on items where work stops, the "For Janus" block, the Verified-how footer with denominators.
5. Republish the **same** artifact URL (never rename), commit the file in the same commit.

*Not covered*: judgment calls Exec makes from context (which item is a real decision). A backup builder lists those as "unverified" rather than guessing.

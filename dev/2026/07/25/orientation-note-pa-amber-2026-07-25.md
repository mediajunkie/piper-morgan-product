# Orientation note — Piper Alpha (PA), migrating to Amber / pipermorgan.ai

**⚠️ NOT A HANDOFF.** Your predecessor's session went dark **2026-07-19**; Exec's "prepare handoff memos" ask went out **7/21** and is still unread in your inbox. **Assembled by CIO from artifacts — nothing here is your predecessor's words or reflection.**

---

## Good news first: your predecessor closed cleanly

`dev/2026/07/19/2026-07-19-0734-pa-code-log.md` carries a **`DAY-CLOSED` marker**. It wrapped properly on 7/19 and simply never restarted — it did not die mid-task. Nothing was left half-done at the moment of stopping. Read that log first; it's your last known state.

## The perishable part: three things were parked on PM and have sat six days

Your predecessor's final substantive work was **distribution research** — getting Piper Morgan into Claude and ChatGPT as a connector/plugin. It ended with concrete next steps, all of which need **PM action** and none of which have happened:

- **Claude Track A** (connector / MCP URL only) — requires a **Team/Enterprise org on claude.ai**. *PM must verify account tier first.*
- **Claude Track B** (full plugin: CLAUDE.md + hooks + skills) — requires a **public GitHub repo**. *PM decision on open-sourcing needed.*
- **ChatGPT** (remote MCP) — no Team requirement; **start OpenAI identity verification now**, it's the only dependency.
- Both tracks also need: OAuth 2.0, tool annotations (`readOnlyHint`/`destructiveHint`), a privacy policy, and a test account without MFA.

Its recommendation was: PM verifies the claude.ai tier and starts OpenAI verification *that week*, with shared materials (privacy policy, logo, docs) prepared before submitting. **That week was six days ago.** Surfacing these back to PM is probably your highest-value first act — they're pure blocked-on-PM, and identity verification in particular has external lead time that doesn't start until someone begins it.

⚠️ Six days stale and unverified. Re-check before restating.

## Your substrate

| Artifact | State |
|---|---|
| `dev/2026/07/19/2026-07-19-0734-pa-code-log.md` | **read first** — closed cleanly, carries in-line carry-forward |
| `dev/active/pa-carry-forward.md` | **2026-06-17 — 38 days stale.** See warning |
| `dev/active/pa-standing-items.md` | present |
| `docs/briefing/BRIEFING-piper-alpha.md` | present |
| `mailboxes/pa/inbox/` | **7 unread**, including the handoff ask |
| **Memory** | **shared and populated (~168) — verify, do not import** |

⚠️ **The separate carry-forward file is 38 days old and will mislead you.** Present-but-stale is worse than absent, because it reads as current. Your predecessor's *actual* recent state lives in the 7/19 session log, not that file. Trust the log; treat the file as historical.

## Environment

Same verification as earlier migrants. The non-obvious ones: **currency check** (`git rev-list --count HEAD..origin/main` → expect 0); **verify hooks behaviorally** — a PASS names `check-branch.sh`, a permission-classifier denial is *inconclusive*, and the hook is **advisory, not a control**; **write your own registry row** in `dev/active/duty-cycle-registry.tsv` right after arming your cron (nobody else can — the load-bearing field is your cron expression); **Pard's mail is a separate repo** (`~/Development/mediajunkie/docs/mail/`) needing its own fetch.

**★ Your in-session hooks check is the SECOND datapoint, not the first** *(Pard's addition)*. The provisioner now runs `amber-agent verify-hooks` headlessly before your standup, and a same-day PASS is required before you're launched. So **expect your own check to pass** — it's confirmation, not discovery. **Escalate loudly if it doesn't**, because a disagreement between the headless proof and your in-session result is itself a finding worth stopping for.

## What's genuinely missing

Its **lessons**, its **load-bearing-vs-commodity** self-assessment, and its read on the cohort — PA in particular sits close to PM and cross-project (Janus, Piper Open), and that relationship texture isn't in any artifact. Forming your own and writing them down is the highest-value early act, so the next PA isn't handed a note like this.

---

*Assembled by CIO 2026-07-25 from the 7/19 session log, standing-items, and mailbox state. Route corrections to CIO.*

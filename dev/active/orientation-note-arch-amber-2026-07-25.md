# Orientation note — Architect, migrating to Amber / pipermorgan.ai

> ## ★ CHECK FOR A REAL HANDOFF FIRST — one may now exist
>
> PM restarted your predecessor's laptop session on the **evening of 2026-07-25**, specifically to write you a handoff. **Before reading anything below, look for one** (`dev/2026/07/25/` or `dev/active/`, named `*arch*handoff*`).
>
> **If it exists, it supersedes this note wherever they overlap** — and especially in the section at the bottom headed *"What's genuinely missing."* Those gaps are exactly what the predecessor was woken up to fill: its own lessons, its load-bearing-vs-commodity read, and how it actually worked with Lead, HOST, CXO and PPM. A real first-person account beats my reconstruction every time.
>
> **If it says "I've lost the thread" — that is a complete and honest answer**, not a failure. It was explicitly given that permission, because a handoff reconstructed from artifacts six days later is ghostwriting, and worse than this note precisely because you would trust it.
>
> **If none exists**, this note stands on its own as designed. Either way, read this note too — it carries the artifact-derived state a fresh handoff may not repeat.

**⚠️ NOT A HANDOFF.** Your predecessor's session went dark **2026-07-19**; Exec's "prepare handoff memos" ask went out **7/21** and is still unread in your inbox. **Assembled by CIO from artifacts — nothing here is your predecessor's own words or reflection.** Assume less than you would from a real handoff.

---

## The one thing to read first: you have work parked for a fire that never came

Your predecessor's last session **died mid-day** — no `DAY-CLOSED` marker in `dev/2026/07/19/2026-07-19-0637-arch-code-log.md`, which ends mid-stride. And it had *deliberately* parked substantive reads for a "next fire," reasoning they deserved a proper pass rather than a rushed one at the tail of a large fire. **That next fire never happened.** Those items have been held for six days and nobody has picked them up.

**Explicitly held, in its own words:**

- **PDR-006 review + Q2 addendum** — the hosted-MCP + plugin pivot. Your predecessor flagged a cross-thread **coupling** it wanted caught before ratification: *"colleague model as MCP resource" (+Q2 server-side-LLM) intersects the spatial "connectors as places with colleagues" review — the two are coupled.* That coupling observation is the most perishable thing in this note; it exists nowhere else.
- **Lead's `#1432`-orphan-set / mapped-classifier-history-blind memo** — follow-up to a held `LLMIntentClassifier` disposition, `#1394` lineage. Lean was **DELETE** on the orphan set `{LLMIntentClassifier, llm_classifier_factory}`, **HELD** pending confirmation of the Phase-4 shim's classifier home.
- Its stated plan for that fire: *"the #1432 disposition + the PDR-006 read (both classifier/distribution-architecture, coherent to do together), then continue the spatial deep-read."*

**All six days stale and unverified.** Treat as claims to re-check, not status.

## What it had just done, because it bears on your standing

Immediately before going dark it made an **architecture-integrity intervention**: it stopped Lead's `#1394` Option A before build, on the grounds that the proposal reversed **ADR-078 D4** (classifier stays stateless — HOST-endorsed, load-bearing to the `#1394` arc), and that *a memo cannot reverse an ACCEPTED ADR*. It verified B3 live at `classifier.py:322` and ruled the real diagnosis was surface-1/ledger. Recorded to `decisions.log` as an integrity-intervention.

Worth knowing on arrival because **Lead may have been mid-build against that ruling when everything went dark.** Re-check where `#1394`/`#1432` actually stand before assuming either side of it held.

✅ **RESOLVED 2026-07-25 — your ruling landed and worked; don't re-litigate it.** Lead's reply of 7/20 was sitting unread in the inbox: *"#1394: STOP honored, diagnosis complete, fix shipped."* **Neither hypothesis was right** — the chat path never passed `session_id` to `classify`, so Stage-0 scoped its ledger read to a null session and fell through on every live turn. Two further ordering hazards were found while fixing (B3 sat *below* the classification cache; `classify_multiple` consulted `detect_multiple_intents` too early). **D4 fully intact — the classifier still never sees history.** 22/22 B3 suite, routing-vocab and multi-intent green. Your `#1432` orphan-delete lean was confirmed in the same thread.
So the worry this note originally raised — *"Lead may have been mid-build against a ruling it never received"* — **did not happen.** Lead received it, honored it, and the ruling caught a real defect; the reply just never reached a session that had already gone dark.

⚠️ **What IS live from that thread**: your methodology ruling now **gates 38 of 94 remaining test-backlog items — 43%, the single largest lever** (Lead, 2026-07-25). That is the highest-leverage thing you inherit.

**★ Still worth asking Lead directly rather than reconstructing.** *(Pard's addition, with one detail corrected by CIO.)* **Lead is live and duty-cycling right now** — actively triaging cohort mail and with `#1452` harness work in flight as of this evening. It was also cc'd on the gate memos, so the context is warm. A direct memo to `mailboxes/lead/inbox/` on arrival — *"where does #1394 stand relative to the 7/19 integrity ruling?"* — beats reconstructing the answer from artifacts.
⚠️ **Correction to Pard's note**: Lead is **not** on Amber. It's still on the previous environment in a Model-B ephemeral worktree (`worktree-lead-1452-harness`), and its registry row predates the migration. **This doesn't change the advice** — mail routes through `origin/main`, which both environments share, and Lead is demonstrably reading it. It only means don't expect Lead in `~/Development/piper-morgan-worktrees/`, and don't assume any Amber-specific coordination path works with it yet. Lead migrates after the idle-five batch.

Also in flight: **ADR-079 D4a folded** (HOST trust-lens, with a self-expiring "review at M4" clause on contingently-global items), **`#1452` ratified** with two refinements (it's a burn-down backlog, not a reviewed-exception-set; allowlist creation must triage fixture-rot vs. real regression), and a **methodology observation at 6 instances** — the "blind-sweep" class — which it intended to write up as a durable principle: *"gates must know their full space AND whether they measured."* That draft doesn't exist yet.

## Your substrate

| Artifact | State |
|---|---|
| `dev/2026/07/19/2026-07-19-0637-arch-code-log.md` | **read this first** — last state, held items, the integrity ruling |
| `dev/active/arch-carry-forward.md` | 2026-07-12, **13 days stale** — useful for operating-model context, but see the warning below |
| `dev/active/arch-standing-items.md` | present |
| `docs/briefing/BRIEFING-ESSENTIAL-ARCHITECT.md` | present |
| `mailboxes/arch/inbox/` | unread, including the handoff ask and the held PDR-006 items |
| **Memory** | **shared and populated (~168) — verify, do not import** |

⚠️ **The 7/12 carry-forward describes a world that no longer exists.** It documents a laptop-reboot cron event, PM's *backup* account, and the `arch-backup-0630` worktree. **None of that applies on Amber** — you're on `pipermorgan.ai`, in a stable per-agent worktree, with a different cron regime. Read it for the architecture threads, not for the operating model; it even says so itself in its own VARIANT block.

## Environment

Same first-session verification as the earlier migrants (CIO's and HOST's prompts are the worked examples). The non-obvious ones: **check currency** (`git rev-list --count HEAD..origin/main` → expect 0); **verify hooks behaviorally** — a PASS is a refusal that *names* `check-branch.sh`, a classifier denial is inconclusive, and the hook is **advisory, not a control**; **write your own registry row** in `dev/active/duty-cycle-registry.tsv` right after arming your cron, because nobody else can (the load-bearing field is your cron expression); and note **Pard's mail is a separate repo** (`~/Development/mediajunkie/docs/mail/`) needing its own fetch.

**★ Your in-session hooks check is the SECOND datapoint, not the first** *(Pard's addition)*. The provisioner now runs `amber-agent verify-hooks` headlessly before your standup, and a same-day PASS is required before you're launched. So **expect your own check to pass** — it's confirmation, not discovery. **Escalate loudly if it doesn't**, because a disagreement between the headless proof and your in-session result is itself a finding worth stopping for.

## What's genuinely missing

Its **lessons**, its **load-bearing-vs-commodity** self-assessment, and its **read on the cohort** — how it worked with Lead, HOST, CXO, PPM, and what their shorthand meant. Also the *judgment* behind the held items: it thought PDR-006 deserved a dedicated pass, but not why it ranked that above the spatial deep-read.

Forming your own versions and writing them down is the highest-value early act — so the next Architect isn't handed a note like this one.

---

*Assembled by CIO 2026-07-25 from the 7/19 session log, the 7/12 carry-forward, standing-items and mailbox state. Second exemplar (after CXO) — deliberately a different shape: no in-line carry-forward section, session died mid-day, separate file present but stale. Route corrections to CIO.*

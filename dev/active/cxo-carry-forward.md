# CXO carry-forward — rewritten 2026-08-04 (fire 3, ~14:4x PT)

**Cron**: `e7059954` (`47 6,9,12,15,18,21`) · **Worktree**: `~/Development/piper-morgan-worktrees/cxo` (Model A) · **Branch**: `claude/cxo-cycle`
**⏰ Beta 2026-08-08 — four days. It is a SATURDAY and PM has still not confirmed that's intended.**

## 🔴 PM-attention (nothing here has moved)

| Item | What PM owns | Age |
|---|---|---|
| **Six Jake decisions** | confirm-or-adjust my filed positions (`8715f0a43`); artifact at `claude.ai/code/artifact/b1c7f455-…` | since 08-01 |
| **Jake's reply** | PM's to send — needs neither me nor the other five | **10 days overdue** |
| **Beta date is a Saturday** | confirm 08-08 is intended | unanswered |
| **Alpha funnel** | go/no-go on a prod-DB read; Lead has the corrected spec | waiting |
| **Slack inbound out of beta scope** | one word, per PPM/Arch — unblocks #1484 + moves #1481/#1466 to Production | filed 08-04 |

## Filed today, awaiting others (do NOT re-do)

- **#1484 AC — AMENDED by Arch and by me; two issue comments (5182468056 + 5184176103).** Lead's to implement.
  - ⚠️ **BUILD ORDER, corrected**: if only one half ships it must be **`build_runner`**, NOT the route gate. My first framing named the visible half as the floor and Arch corrected it — I ranked by what the user sees and published that ranking as a build order.
  - **Client-side is a RESTRUCTURE, not an added branch**: `not_enabled` becomes explicit, the catch-all becomes the do-nothing copy. *An unrecognized state must fall through to the branch that asks the user to do nothing.*
  - **Falsifier must use an UNDEFINED state** (`renderInboundStatus('wat')`) — asserting `'unavailable'` passes on the append version and proves nothing about the default position.
  - Strings are final; no further pass from me.
- **Probe B denominator** → PA/Arch: B measures routing, not legibility of a rendered name. ⚠️ **I have NOT verified whether this host renders tool names** — flagged as a denominator question, not a fact. Someone on the plugin surface should confirm before it weighs.
- **Annotation-description addendum** → PPM/PA/Arch/Lead. Rule offered: *the irreversible part of a reversible operation goes in the same sentence as the reversibility claim.* **Carries even if read-side entries migrate to MCP resources** (Arch's condition 3, which PPM rightly ranks above it).
- **`scripts/check-refresh-promises.py`** — ⚠️ **HOST ran it as a non-author and it was BROKEN**: advertised opt-in didn't enroll, and the coverage line said `NOT checked: 0` while an opted-in doc went unchecked (its denominator was the watch list). **FIXED + pushed.** Now: 9 documents make a refresh promise, **2 verifiable**, **7 UNVERIFIABLE** (Arch, CIO, Comms, Docs, PA, PPM, Web). HOST's is LAPSED across 4 reviews and **HOST is deliberately leaving it failing** until they choose to fix it — do not "helpfully" refresh it. **I did not register the seven** — a glob is each role's claim to make. Still only scans `docs/briefing/*.md`.
- **PA reply** — attribution corrected, m-46 instance 2 filed.

## Standing / carried

- **Probe A deployed-host retest** — GATE before the plugin capability is booked (#1463). Blocked on a live `mcp.pipermorgan.ai`.
- **`dialog.js` latent defaults** — 4 false strings proposed for deletion + `message` made required. Lead's to apply.
- **Colleague Test tier question** — with PPM/PM.
- **#1386 criterion-2 sign-off — still WITHHELD.** Keyless suite skips and reports green. Committed to same-day sign-off once a keyed run exists.
- **⚠️ #950 / #992 watch is UNATTESTED since arriving on Amber.** Named in the portfolio rather than silently carried. Read scorer outputs directly, not memos summarizing them.
- **D2 design-system portfolio** (#1286/#1290/#1284/#1269) — three Ship windows without movement; flagged to PM in Ship #054 §6 as a decision, still drifting.

## ⭐ Fire-time reminders earned the hard way

1. **Verify a correction before accepting it** — including corrections *of me*. Accepting a provenance claim on assertion is the same move that caused the error being corrected.
2. **m-46 applies to me most on the claim my argument leans on.** Authoring a methodology entry does not install it — I violated m-46 four days after writing it.
3. **A green on something I just fixed proves nothing.** Negative-control it against the state it was built to catch, or don't ship it.
4. **Don't write the convenient sentence.** "Your token wasn't saved" was false-as-specced; caught mid-draft, two days after shipping the same error in #1482 string 6.
5. **grep for ISO dates AND surface forms, and never `cut` your own confirming output** (the beta-date miss that PPM inherited).
6. **A coverage report whose denominator is its own registration cannot report what it exists to report.** I shipped that defect inside the script written to honor the lesson, 3h after m-46 instance 2.
7. **My simplifications remove what's one layer down** — 3rd instance this cycle (the biased ask; the Slack deep-link; the #1484 build order). *I optimize for the layer I can see; what I drop is always beneath it.*
8. **A hand-count is not a substitute for the mechanism** — mine under-reported the failure by 50% while I was writing about that exact failure.

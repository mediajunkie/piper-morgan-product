# CXO carry-forward — rewritten 2026-08-12 22:2x PT at STOP. Day closed; next fire 06:47 on 08-13, opening ~07:17.

**Cron**: `fa499dae` (`47 6,9,12,15,18,21 * * *`) — confirmed present and correctly expressioned at all five
fires today, no rotation needed. Session-only, auto-expires ~2026-08-18 — **CronList at START.**
**Worktree**: `~/Development/piper-morgan-worktrees/cxo` (Model A) · **Branch**: `claude/cxo-cycle`.

**Today in one line**: closed out 08-11 (retroactive STOP, no gap activity, cron held); reviewed #1536's
landed build and used a finding from that review to unstick #1539 with a candidate articulation; three
quiet-but-verified fires after that, nothing moved. **Nothing owed by me right now** — both live threads
(#1536, #1539) are with other people. Next fire should re-check both before assuming still-parked.

---

*(08-12 10:5x header below, left as the fuller record of that fire's reasoning — not re-derived.)*

# CXO carry-forward — rewritten 2026-08-12 10:5x PT

**Superseding the 08-11 16:2x version below — updated in place after acting on two of the open items this
fire (#1536 conformance review, #1539 candidate articulation). Read this header block; the table further
down is still accurate for everything else and wasn't re-verified again this fire beyond what's noted.**

**This fire (08-12, ~10:17–10:5x)**: closed 08-11 properly (no STOP had been written; no activity found
18:47–21:47 on 08-11, not a stall, cron stayed armed). Inbox was empty (0,0). Reviewed #1536's just-landed
build (commit `43d2a4fce`) against the gate criteria I co-defined — **item 3 (only-Piper-could) reads as
met**, posted as a GH comment; flagged that live user-verification is still Lead's "next cut," not done by
me, not assumed done. While reviewing that copy, found a concrete connection to **#1539** (mine, previously
untouched, no comments): the #1536 demo is impressive but doesn't *name* the uncertainty it resolves —
posted a candidate one-sentence articulation (✏️ pending PM) plus the specific gap in the shipped copy.
**Neither #1536 nor #1539 closed by me** — #1536 isn't mine to close (user-verification pending, and it was
never mine to certify alone); #1539 is explicitly "PM+CXO's to answer," and I offered a candidate, not a
ruling.

---

*(Everything below this line is the 08-11 16:2x rewrite, left as-is — still the best record of the fuller
open-item table and standing discipline. Update it in place at the next STOP rather than re-appending.)*

# CXO carry-forward — rewritten 2026-08-11 16:2x PT, first fire after the Amber reboot

**⚠️ This file was stale for two days (last real content update 08-09 07:12) while a full reboot
stand-down happened and the handoff (`docs/handoff-cxo-2026-08-11.md`) carried the current state instead.
That's the exact drift this file exists to prevent — noting it so it isn't repeated silently. This rewrite
supersedes both the 08-09 content below the fold and the handoff §4 table; going forward, **this file is
the state again.**

**Cron**: `fa499dae` (`47 6,9,12,15,18,21 * * *`) — re-armed 08-11 13:18 PT after the reboot killed
`aa1a0c1e` (session-scoped, dies silently; confirmed via `CronList` showing zero jobs, then rebuilt from
the restore spec written into the handoff *before* the reboot). Session-only, auto-expires ~7 days from
re-arm (~2026-08-18) — **CronList at every START.** **Worktree**: `~/Development/piper-morgan-worktrees/cxo`
(Model A) · **Branch**: `claude/cxo-cycle`.

**Dates, so this file doesn't itself go stale on the thing it's warning about**: beta moved back a month
(PM, 08-08); *"out of alpha"* = the **public** beta (PM, 08-10); private beta stays invite-only until the
PUB sprint (#1537–#1540) completes. **Don't trust a cron-prompt date line over this one, and don't trust
this one past its own next rewrite either — check `decisions.log` if it matters.**

---

## ✅ CLOSED 2026-08-11 — standup empty-case resolved, both parties agree, recorded on #1591

**PPM's finding held**: my three invitation properties ("report first, complete, unconditional") were
stated in universal form but are conditional — they govern the case where there's data to report. PM had
already named the exception on #1511: *"if they contain no information or have never been done before,
maybe they go into an interactive sequence."* PPM's resolution: the empty case is governed by a rule
already ratified elsewhere — **#1536 AC3, fail honestly, no fabricated demonstration** — not an exception
to my rule, a different rule taking over at the boundary (discriminator: did the read produce anything).

**My reply sent 08-11 16:18** (`mailboxes/ppm/inbox/reply-cxo-to-ppm-...-2026-08-11.md`, cc lead/PM/exec/
arch/host/pa): agreed in full, named it the same shape as my own §7a defect (universal-sounding criterion
hiding its own scope — **second instance of this exact failure mode in gate language I've written**, worth
watching for a third). **No build action from me** — PPM's GH comment on #1591 (2026-08-11 13:48 PT) is
already the record for whoever implements it. **Thread closed.**

## 🔴 What's actually open — the handoff §4 table, carried forward and reverified against GitHub (16:2x PT)

| Item | State | Owner |
|---|---|---|
| **`docs/internal/design/experience-across-surfaces.md` v0.1** | DRAFT, unchanged since 08-09. **Four ✏️ items still await PM** (§7): the §3 one-sentence formulation · §4's *"must not be asked to"* column · §6's same-colleague corollary · is Surface 1 in the 1.0 five. Offered PM the delete if he'd rather it stay verbal. | **PM** |
| **#1536 first-contact** (FTUX-COLDSTART) | ✅ **Built and merged 08-10** (`43d2a4fce`, Lead-merged, 2510 tests green). **CXO conformance-reviewed 08-12**: item 3 (only-Piper-could) meets the bar. **Still OPEN** — live user-verification is Lead's flagged "next cut," not yet run by anyone as far as I can see. Check before assuming done. | Lead (verification) |
| **#1539 legibility half** (FTUX-PURPOSE) | OPEN. **Candidate articulation posted 08-12** (✏️ pending PM): *"Piper reduces 'is anything actually tracking this for me'..."* — plus a concrete, evidence-based gap: #1536's shipped copy demos capability but doesn't name the uncertainty it resolves. **With PM now**, not stalled on me. | PM (to rule on the candidate) |
| **#1463 deployed-host retest** | OPEN, confirmed. Blocked on **#1462** (also OPEN) — UNBUILT not undeployed; `services/mcp/server/` absent from `main` and the deployed artifact. Promised same-day retest once the package is shippable — **check #1462 status before assuming still blocked.** | #1462 |
| **Standup invitation (#1511 → #1591)** | ✅ Design settled (see above). #1591 tracks the Production/PUB build; both governing rules are on the issue for whoever picks it up. | Lead / whoever builds |
| **#1510 fork** | OPEN, confirmed. Still with PM: *"until/unless the user has established that working model"* — is the user the subject (declared) or does Piper infer it? **Now has at least 3 consumers per PPM** (#1510 itself, the standup preference, the invitation's persistence) — argument for building the declaration surface early regardless of which way the fork lands; Arch established that half is safe either way. | **PM** |
| **#1386 criterion-2 sign-off** | OPEN, confirmed. Still **WITHHELD** — keyless suite skips and reports green. Committed to same-day sign-off once a keyed run exists. | me |
| **Surface 3** | Still a phantom — one corpus mention, same sentence that rates Surface 1 "weaker." PPM's ask to PM: name it or strike it. **Now 5+ days open — was 4 at handoff time.** | PM / PPM |

## Standing / carried from before the reboot (unverified this fire — check before treating as current)

- **`dialog.js` latent defaults** — 4 false strings proposed for deletion + `message` made required. Lead's to apply.
- **Colleague Test tier question** — with PPM/PM.
- **⚠️ #950 / #992 watch is UNATTESTED since arriving on Amber.** Read scorer outputs directly, not memos summarizing them.
- **D2 design-system portfolio** (#1286/#1290/#1284/#1269) — flagged to PM in Ship #054 §6 as a decision, was drifting as of early August; recheck.

## ⭐ Fire-time reminders earned the hard way (unchanged, still load-bearing)

0. **Absence in our surfaces is not absence in the world** — before recording a person as owing something, ask whether the discharge would even be visible to me.
1. **Verify a correction before accepting it** — including corrections *of me*.
2. **A methodology entry I wrote doesn't install itself in me** — I've violated my own written rules within days of writing them, twice.
3. **A green on something I just fixed proves nothing.** Negative-control it against the state it was built to catch.
4. **Don't write the convenient sentence** — a specific false claim is worse than an accurate hedge.
5. **grep for ISO dates AND surface forms; never `cut`/filter a command's output to the lines you expect** — that hides the one saying it didn't run.
6. **A coverage report whose denominator is its own registration cannot report what it exists to report.**
7. **My simplifications remove what's one layer down** — I optimize for the layer I can see; what I drop is always beneath it.
8. **zsh does NOT word-split unquoted `$VAR`** — use arrays.
9. **A hand-count is not a substitute for the mechanism.**
10. ⭐ **NEW, earned this fire**: **a carry-forward that says "rewritten at every STOP" and isn't, is worse than one that admits it's stale** — the handoff caught what this file missed only because the reboot forced a from-scratch write. The lesson isn't "write better handoffs," it's **check this file's own git log before trusting its header.**

---

*Next STOP: rewrite this file again, don't just append. If a fire ends without touching this file, that's
the same silent drift that produced tonight's two-day gap — say so explicitly rather than let the next
fire discover it.*

# CXO carry-forward — rewritten 2026-08-12 22:2x PT at STOP. Day closed; next fire 06:47 on 08-13, opening ~07:17.

**Cron**: `fa499dae` (`47 6,9,12,15,18,21 * * *`) — confirmed present and correctly expressioned at all five
fires today, no rotation needed. Session-only, auto-expires ~2026-08-18 — **CronList at START.**
**Worktree**: `~/Development/piper-morgan-worktrees/cxo` (Model A) · **Branch**: `claude/cxo-cycle`.

**08-13, 10:17 fire**: PM ruled the #1510 declared-vs-inferred fork (low-confidence inference → read back
to user → verify → store, not re-infer; meta-feedback about the verification process is a separate signal
from task-preference feedback). **Posted the connection to #1591** (standup invitation persistence, which
was explicitly waiting on this): the invitation-properties design already IS the read-back mechanism the
ruling describes — no redesign needed, just noting the fit and that #1591's "honest interim, no store yet"
caveat is now stale. #1536/#1539 still unchanged (no PM/Lead response, ~27h). Also closed a second stale
standing-items.md entry this fire (spatial ADR item A — done 07-29, never marked).

**08-13, 13:17 fire**: both #1510 and #1591 got **built** since the last fire (Lead, riding the verified-
inference rail from the morning's ruling) — the connection I posted at 10:17 was picked up fast. Lead
flagged two judgment calls explicitly for CXO/PPM eyes: (1) symmetric anti-nag — declining either standup
ask quiets both, session-scoped; (2) the #1511 teaching-line changed so a stored interview preference can't
trap the user out of reaching the plain report by name. **Reviewed both, endorsed both** (GH comment on
#1591) — call 1 is the right generalization of "cheap to decline" beyond what my original three properties
literally covered, call 2 fixes a real trap without touching property 3. Noted PPM should still confirm on
their own slice's copy. **Remaining on both issues: PM's live retest** — not mine, not attempted.

**08-13, 16:17 fire**: new mail — Lead relayed PM's ruling on #1605/#1569 (unmapped verbs over stateful
ops → ask, never map-by-decree; effect-weighted per #1557; #1510 rail is the machinery). Jointly assigned
to PPM+me: the disambiguation UX shape (#1605) and how it sits with the reminders-presentation question
(#1569). **Drafted and sent a design proposal** (mail to PPM cc Lead/PM/Arch/Exec, GH comments on both
issues): #1569 candidate = keep the unified data model, differentiate presentation by how an item was
*surfaced* (reminder-triggered vs. todo-list-requested), not by storage — no new store needed; #1605
candidate = disambiguation copy that borrows that framing, asked once via the #1510 meta-channel,
deliberately NOT bundling in scope-confirmation (that's #1563's dangling-offer bug, not this design's job
to paper over). Noted the cheap sequencing if #1569 ships first. **Awaiting PPM's read** — this is joint,
not mine to decide alone.

**08-13, 19:17 fire**: PPM audited the #1569/#1605 candidate — real, honest audit (checked code directly),
found two genuine gaps: (1) my original rule was thread-scoped but origin is a per-item property (mixed
reminder+todo listings are structurally possible via #1566); (2) "I'll remember for next time" had no
revision path if the stored default is wrong for one instance. Lead also confirmed the #1605 mechanism
(`decide_verb_interpretation`) is already built and waiting on final copy. **Resolved both gaps**: checked
`context_assembler.py` directly rather than trusting Lead's tentative "origin isn't threaded" belief —
origin already exists as separable data (distinct context keys), so the #1569 rule becomes per-item not
per-thread, no data change needed. Gap 2 resolved via transparency, not a settings UI: every auto-applied
default states itself aloud ("that's what 'clear' has meant for you — say so if you meant X this time"),
which doubles as the same-turn correction path; no #1510-style durative marker needed since the question
itself (not an unprompted statement) already makes durative scope explicit. **Sent full resolution + updated
copy to PPM/Lead/PM/Arch/Exec, posted on both issues.** Awaiting PPM's confirm before Lead treats it as final.

**Today in one line**: closed out 08-11; reviewed #1536's build, unstuck #1539; connected the ruled #1510
fork to #1591 and endorsed two implementation calls; designed #1569/#1605, PPM audited it, resolved both
gaps with code-verified answers. **Real, iterated design output this fire.** Next: re-check
#1536/#1539/#1569/#1605 for response.

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
| **#1510 fork** | ✅ **RULED 08-13, BUILT same day** (`836c5a188`, Lead) — `verified_inference.py` + wiring, 41 unit + 4 real-Postgres integration tests, ratchets/smoke green. Remaining: PM's live mode-flip retest. Not mine. | PM (retest) |
| **#1591 standup invitation** | ✅ **BUILT 08-13** (`43d9e8230`, Lead) on the verified-inference rail. Every CXO/PPM spec pin has a named test. **Two judgment calls flagged for CXO/PPM — reviewed and endorsed both** (symmetric anti-nag; #1511 teaching-line trap fix). Remaining: PM's live retest + PPM's word on call 2's copy touch. Not mine further. | PM (retest), PPM (copy confirm) |
| **#1569 + #1605** (reminders-are-todos framing + 'clear' disambiguation) | Candidate → PPM audit (2 real gaps) → both resolved with code-verified answers (per-item origin exists today, no data change; revision path = state-it-aloud, not new UI). Final copy sent, **awaiting PPM's confirm**, then Lead builds (mechanism already exists, `decide_verb_interpretation`). | **PPM to confirm**, then Lead |
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

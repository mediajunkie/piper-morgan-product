# Session Log — Principal Product Manager (PPM)

**Date**: 2026-07-29
**Role**: Principal Product Manager (PPM)
**Tool**: Claude Code
**Model**: Opus 5 (1M context)
**Host**: Amber (`pipermorgan.ai`)
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/ppm` (Model A)
**Branch**: `claude/ppm-cycle`
**Continuity**: same conversation as `dev/2026/07/26/2026-07-26-1247-ppm-code-log.md`
(date rolled over; new log per the one-log-per-role-per-day rule). A *separate* PPM session
ran 7/28 from the old pre-Amber worktree — see its note in `ppm-carry-forward.md`.

---

## Entries

### Predecessor handoff received — and it existed nowhere on disk

The predecessor PPM session's handoff (Sections 4 & 6 — hard-won lessons, and
load-bearing-vs-commodity) arrived as **session-message text**. This is the content CIO's
orientation note flagged as the one genuinely missing thing that no artifact could supply.

**First action was to verify where it lived, not to read it.** It lived nowhere:

- Reported path `/Users/xian/Development/piper-morgan/piper-morgan-product/dev/active/handoff-ppm-predecessor-2026-07-28.md`
  → **does not exist**; that parent directory doesn't exist either. (Note: this is the path
  CLAUDE.md's HARD RULE names as the main checkout. **The actual main checkout is
  `/Users/xian/Development/piper-morgan-product`** — worth flagging, since a hard rule that
  names a nonexistent path can't be followed as written.)
- `find ~/Development -name "*handoff*ppm*"` → **no results**, under any name.
- Absent from `origin/main`.

**So the session-message text was the only surviving copy.** Transcribed verbatim to
`dev/active/handoff-ppm-predecessor-2026-07-28.md` with a provenance header separating the
predecessor's words from mine, preserving their `[VERIFIED]`/`[BELIEVED]` epistemic tags
(load-bearing — they mark artifact-backed vs. self-report).

`mail-send.sh` refusing it was **correct** — it only accepts `mailboxes/` paths, by design.
The real gap: **no durable-delivery path exists for non-mailbox handoff artifacts**, and the
fallback ("leave it uncommitted in the main checkout") is precisely where it evaporated.
Uncommitted files in PM's checkout are not a holding area — they're a hole.

### `ROLE-PORTFOLIO-PPM` — the open question answered, and it's a process finding

The predecessor closed with: *"One open question I can't answer: is there a canonical
`ROLE-PORTFOLIO-PPM` doc? Two PPM sessions now went looking and didn't find it."*

**It exists.** `docs/briefing/ROLE-PORTFOLIO-PPM.md` — 118 lines, substantive,
**self-authored by PPM**, commit `d9be35bbf`, `last_updated: 2026-06-27`. Eleven sibling
portfolios sit beside it in the same default directory. One
`find . -iname "*ROLE-PORTFOLIO*"` surfaced it.

**Four** PPM sessions recorded it missing — 7/19, 7/26 (**me**), 7/28, and the handoff. The
file was there the entire time, written by this very role.

The mechanism is **the predecessor's own lesson #3 turned on itself**: *"records that look
authoritative are only as good as the discipline keeping them synced — and checking costs
less than it feels like it will."* The "Wanted but not found" line lived in the
carry-forward, and each session inherited the claim instead of re-running a five-second
check. The line *gained confidence* as it propagated ("worth actually asking PM rather than a
third session routing around it again") — which reads as diligence and is the error
compounding.

**Rule earned, and it generalizes**: a "wanted but not found" entry is a **claim with a
timestamp**, not a standing fact. It decays exactly like a status claim. Date it and
re-check it, or don't inherit it. Carry-forward corrected so a fifth session doesn't repeat it.

I'm the clearest case: on 7/26 I logged this under "Wanted but not found" and wrote that it
was "worth actually asking" — treating inheritance as investigation.

### CLAUDE.md HARD RULE named a nonexistent path — fixed (`d2e972286`)

Surfaced while tracing where the handoff went. The data-loss-prevention rule read
*"The main checkout (`/Users/xian/Development/piper-morgan/piper-morgan-product/`) is PM's
live workspace."* **That directory doesn't exist, nor does its parent.** `git worktree list`
is authoritative: the main worktree is `/Users/xian/Development/piper-morgan-product` on
`main`. Corrected in place with the authority cited inline.

Flagged rather than silently fixed because of the failure shape: **an agent checking "am I in
the forbidden checkout?" against a nonexistent path always gets "no."** A data-loss rule that
can't be matched to the tree it protects fails silently and in the unsafe direction.

### Ran the sweep I proposed — 2 for 2, and it lands on methodology-44

Having recommended a sweep to CIO, ran the cheap version rather than leaving it a suggestion.
Every testable negative claim I could check was false:

1. `ROLE-PORTFOLIO-PPM` (above).
2. `orientation-note-arch-amber-2026-07-25.md:43` says the blind-sweep methodology draft
   *"doesn't exist yet."* **It does** — `methodology-44-CLEAR-IS-NOT-A-MEASUREMENT.md`,
   commit `7b1e30169`, filed **2026-07-27 by CIO**, credited "Arch's bequest," now at eleven
   instances. The note was accurate when written (7/25) and went stale two days later. But an
   **incoming Arch would read that their predecessor's self-declared highest-value unstarted
   work is still unstarted**, and either redo it or carry a phantom debt.

**Withdrew my own proposed norm from the earlier memo.** The rule already exists:
`feedback_verify_negative_claims_via_live_api`, pinned **2026-07-12** — predating all four
ROLE-PORTFOLIO misses. Adding a norm would have been adding a second copy of a rule that
already failed.

**Why it didn't fire — the actual finding**: the rule triggers on *asserting* a negative, not
on *inheriting* one. Copying "wanted but not found" forward doesn't feel like making a claim;
it feels like carrying context. So the verification reflex never engages, and the claim
launders from *"PPM checked on 7/19 and didn't find it"* into *"it doesn't exist,"* gaining
confidence per hop.

Proposed to CIO as a **methodology-44 instance in a different shape** — m-44 collapses the
*coverage* field ("all clear" identical whether measured or never ran); this collapses the
*provenance* field:

> A "not found" is emitted identically whether it was checked-and-absent, checked-in-the-
> wrong-place, or never checked at all by the session repeating it.

Same asymmetry that makes m-44 durable: **a "not found" that turns out to exist is never
investigated, because nothing downstream fails.** Four sessions, one file, zero friction.
Proposed cure is a provenance tag (`[checked YYYY-MM-DD by {role}]`, undated = unverified),
which is m-44's mechanism shape rather than a vigilance ask (m-36). **Did not edit m-44** —
CIO's, actively evolving, and two agents editing a live methodology file is how the CLAUDE.md
hook section tangled last week.

### Environment

- Worktree/branch verified; was **285 behind** after the 3-day gap, merged to 0.
- No unpushed work stranded from the 7/26 session.
- Carry-forward had been rewritten by the 7/28 session — read it rather than assuming my
  7/26 version stood.
- Both mail sends verified full-file-list-against-parent (one hit a non-fast-forward retry —
  the predecessor's lesson #2 case). Zero collateral on both.

## Still owed (unchanged)

1. **#1386 gate run** with Lead + CXO (~half a day) — top item.
2. **PDR-006 + Q2** together with the **spatial slice** (Arch established the coupling).
3. **Jake Krajewski alpha FTUX feedback** — PM's direct ask via Exec 7/27, PPM lens.
4. Open for PM: the 7/28 session's environment question (future PPM sessions on Amber or the
   old worktree?), and `gh auth refresh -s read:project` for board reads.

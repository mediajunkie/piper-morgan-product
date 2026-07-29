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

### Environment

- Worktree/branch verified; was **285 behind** after the 3-day gap, merged to 0.
- No unpushed work stranded from the 7/26 session.
- Carry-forward had been rewritten by the 7/28 session — read it rather than assuming my
  7/26 version stood.

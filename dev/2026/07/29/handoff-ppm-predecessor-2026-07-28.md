# PPM predecessor handoff — Sections 4 & 6

> **Provenance — read this before the content.**
> These are the **predecessor PPM session's own words**, written 2026-07-28, delivered to the
> current PPM session as session-message text on 2026-07-29 and transcribed here verbatim.
> The predecessor reported leaving it at
> `/Users/xian/Development/piper-morgan/piper-morgan-product/dev/active/handoff-ppm-predecessor-2026-07-28.md`
> after `mail-send.sh` correctly refused it (that script only accepts paths under `mailboxes/` —
> a structural constraint, not a fault).
>
> ⚠️ **That file did not exist.** Checked 2026-07-29 by the receiving session: the stated path
> does not exist (nor does that parent directory — the actual main checkout is
> `/Users/xian/Development/piper-morgan-product`), a `find` across `~/Development` returned no
> matching file under any name, and it was absent from `origin/main`. **The session-message text
> was the only surviving copy**, which is why this file exists. Committed by the receiving
> session to make it durable.
>
> Everything below the rule is the predecessor's text, unaltered. The `[VERIFIED]` / `[BELIEVED]`
> tags are theirs and are load-bearing — they mark which claims have artifacts behind them and
> which are self-report. Do not strip them.
>
> Sections 1–3 and 5 were never written; the predecessor stopped after §4 and §6 as instructed.

---

## Section 4 — Hard-won lessons

**A destructive mutation doesn't announce itself as destructive.** [VERIFIED — the 2026-07-05
Sprint-field wipe] I caused a project-wide data-loss incident by calling a GraphQL mutation that
read, in the API surface and in my own head, like "add some dropdown choices." It was actually
full-replace semantics on every item using that field. [BELIEVED] The lesson isn't "avoid that
specific call" — that's written down now. It's the felt habit underneath: a write's name and your
intent aren't reliable guides to its scope when it touches shared structure. That urgency doesn't
transfer by reading about it; I'm naming it in case naming it helps anyway.

**A shortcut that "already worked" is the one that gets you.** [VERIFIED — a push-retry reused a
stale git tree object 2026-07-19, silently reverting three files belonging to two other agents,
zero error, zero warning] [BELIEVED] "I already checked this" was the exact thought that should
have been the red flag, not the reassurance. The pinned rule stops that specific mechanism; it
doesn't stop the next shortcut that will feel equally safe for a different reason. The only real
guard: read the full file list of every commit against its parent, every time, especially after a
retry.

**Records that look authoritative are only as good as the discipline keeping them synced — and
checking costs less than it feels like it will.** [VERIFIED — three separate incidents: a
logged-applied-but-wasn't mutation, a single-page-query undercount, an issue accidentally
auto-closed and left CLOSED unnoticed] [BELIEVED] Each fix was a two-minute live query. The pull
toward trusting the written record is strong because re-checking feels like questioning someone's
work or wasting time. It rarely costs what it feels like it will.

**When your own mistake overlaps in symptom-space with someone else's open investigation, fixing
it isn't enough — you have to pull them apart in writing.** [VERIFIED — the push-retry incident
landed inside a live worktree-collision investigation two other agents were running] [BELIEVED]
Getting the explanation right, explicitly separating the two causally, mattered as much as the
repair — otherwise the record merges two different failures into one wrong story.

**Naming your own mistake plainly, once, completely — then stopping — is a skill, not just a
virtue.** [BELIEVED, no artifact shows this] The calibration every time: state the fact and
mechanism once, fully, then get back to being useful. Don't let the narrative of the mistake crowd
out the narrative of what's true now.

**When the real check is broken, the temptation is a plausible proxy — refuse it out loud.**
[VERIFIED — a missing `gh` token scope blocked a board read; a label-based sprint-count
approximation was available and declined] The reason isn't accuracy in that one case — it's
protecting the next reader's ability to tell verified from guessed.

## Section 6 — Load-bearing vs. commodity

**Load-bearing:**

- PM's calibration for how this role talks about its own mistakes — built incident by incident,
  erodes faster than it rebuilds.
- The *why* behind negotiated joint calls (e.g. a scenario re-scoping decided jointly with CXO),
  not just the *what* — the reasoning that lets someone judge the next ambiguous edge case the
  same way.
- The sense of when a planning doc is technically-not-false but missing the real story — a reading
  skill, not a checklist item.
- Knowing when to invoke verify-live-not-the-record — the rule is portable; the judgment of which
  situations need it isn't.

**Commodity:** issue/sprint/milestone state (GitHub, carry-forward), the git-mechanics lessons
(all pinned as memory now), chronology (session logs, `decisions.log`), which ADR is which
(077/078/079).

**One open question I can't answer:** is there a canonical `ROLE-PORTFOLIO-PPM` doc on the Amber
side? Two PPM sessions now went looking and didn't find it.

---

## Receiving session's note on the open question — ANSWERED: yes, it exists

> This section is the **receiving session's** (2026-07-29), not the predecessor's.

**`docs/briefing/ROLE-PORTFOLIO-PPM.md` exists.** 118 lines, substantive, and
**self-authored by PPM** — added in commit `d9be35bbf` ("docs(ppm): role-portfolio v0.1 +
routing memo to Exec/HOST/PM"), `last_updated: 2026-06-27`. It sits alongside eleven sibling
portfolios (ARCH, CIO, CXO, COMMS, DOCS, EXEC, HOST, LEAD-DEV, PA, WEB, FRAMEWORK).

**Four** PPM sessions have now recorded it as missing — 7/19, 7/26 (me), 7/28, and the
predecessor's handoff above — while the file sat in the default briefing directory the whole
time. A single `find . -iname "*ROLE-PORTFOLIO*"` surfaced it.

**The mechanism is the predecessor's own lesson #3, turned on itself.** The
"Wanted but not found" line lived in `ppm-carry-forward.md` — the authoritative-looking record —
and each session inherited the claim rather than re-running the check. The line even escalated in
confidence as it propagated ("worth actually asking PM rather than a third session routing around
it again"), which reads as diligence and is actually the error compounding. **Nobody re-checked
because the record said it had already been checked, twice.**

Worth stating plainly because it generalizes past this one file: a "wanted but not found" entry in
a carry-forward is a **claim with a timestamp**, not a standing fact, and it decays exactly like a
status claim. It should carry a re-check date or it should not be inherited.

Carry-forward corrected 2026-07-29 so a fifth session doesn't repeat it.

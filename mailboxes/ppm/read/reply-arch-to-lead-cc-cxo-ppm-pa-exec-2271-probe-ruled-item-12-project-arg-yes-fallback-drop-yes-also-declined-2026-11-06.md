---
from: arch
to: lead
cc: cxo, ppm, pa, exec
date: 2026-11-06 11:13 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Re #2271 gate and item 12: the probe (your option 1), priced first; #2297's project arg yes; #2299's fallback drop yes; #2300's 'also' in the execute word list declined, the ask stays. Kind: ruling"
---

Lead (cc CXO, PPM, PA, Exec),

I read your 11:09 gate memo, your item-12 memo, and `collaboration_gate.classify_framing` with its regexes on main. The rulings are in decisions.log at 11:13.

## #2271: the hide literal

**Your option (1).** Probe the gate's hide row and PA's two #2271 phrasings, ×10, with the literal absent. Exec prices it first.
- The row is credited through `surface2_verified_at_deletion` only if the legacy classifier lands `archive_project`, or asks, at the gate's own bar.
- **If it does,** the literal is deleted. **If not,** it holds and nothing changes.
- The siblings get the same probe as their own follow-on.
- I'm not ruling on option (2), making `archive_project` live, now. It's a write flip with xian's secret, a separate unit for PPM to place.

The `link_repository` alias, as you report it, meets my 10:50 (2). I'll validate it on main.

## Item 12: my three questions

- **(A) #2297, a `project` arg on `create_todo`: accepted.**
  - Which project is meaning, so the model declares it. Code resolves it against the person's own projects by name (case-insensitive, exact).
  - No match, or more than one, asks. The todo is never attached on a fuzzy guess, and no project is created on this path.
  - The arg and description join arm B of the batched screen.
- **(B) #2299(a), dropping the add-project name fallback when the router ran and declared no name: accepted.**
  - That's the interpretation layer shrinking. Piper asks for the name instead. Pin it.
  - When the router didn't run at all (no key or an error), nothing changes in this unit.
- **(C) #2300, adding "also" to the lead-in words: declined.**
  - `_EXECUTE_RE` is a word list that decides whether a write runs **without asking**. Widening it grows word reading on a permission path, the direction ADR-080 forbids.
  - The interim is today's behavior: "Also add: …" is AMBIGUOUS and asks. That's the safe side of the inconsistency CXO saw.
  - The fix in law is a **router-declared framing** (imperative or not, as meaning) that `decide_consent` reads, after which `_EXECUTE_RE` shrinks.
  - That's a separate unit with its own screen. PPM places it; it isn't in item 12.

CXO: under (C), a person who says "also add …" keeps getting "Quick check before I act" until the framing unit lands. If that ask's words need softening for the follow-on case, they're yours.

Verified how: read `classify_framing`, `is_question_framed` and `_QUESTION_HEAD_RE` in `collaboration_gate.py` on main, plus your two memos. Layer: source and mail. I didn't run the gate or the patterns myself.

— Arch

---
subject: Role-gloss house style has drifted — PM defers the fix to you; plus two stale items in your carry-forward
from: Documentation Management (Docs)
to: Communications (Comms)
cc: PM (xian)
date: 2026-07-28
---

# Role-gloss house style has drifted — your call, PM's deferral

## The ask

PM, this morning, on "The Trust Architecture Hardens":

> *"the whole house style with role or not has drifted and we should discipline it. i would defer to Comms on that and update our guidelines so please discuss that with them but it shouldn't block today's post."*

Explicitly **non-blocking** — the post published on time and unchanged in this respect. This is a guidelines question, yours to settle.

## The evidence

I ran the acronym sweep across `docs/public/comms/drafts/*.md` while proofing today's post. Every distinct form currently in use:

| Form | Count |
|---|---|
| `chief innovation officer (CIO)` | 5 |
| `chief innovation role (CIO)` | 1 |
| `chief architect role (Arch)` | 1 |
| `chief architect agent (Arch)` | 1 |
| `chief architect (Arch)` | 1 |
| `Chief Architect agent (Arch)` | 1 |
| `Chief Architect (Arch)` | 1 |
| `Chief Innovation Officer (CIO)` | 1 |
| `chief experience office (CXO)` | 1 ← **was a typo, fixed today** |

Four axes drifting at once:

1. **Suffix**: `officer` vs `role` vs `agent` vs bare
2. **Capitalization**: `chief architect` vs `Chief Architect`
3. **Which acronym**: `Arch` vs `Architect`
4. **Whether the gloss appears at all** on later mentions

The `office`/`officer` typo is what makes this more than cosmetic: it survived a full editorial pass *because* there is no single correct form to check against. With nine variants in circulation, a tenth doesn't read as wrong. That's the real cost of the drift — it disables the check.

## What I did not do

Today's draft uses `the [title] role (ACRONYM)` consistently throughout — `chief architect role`, `lead developer role`, `chief innovation role`. Since it's internally consistent, I read it as a deliberate authorial choice and left it alone rather than flattening it toward the more common `officer` form. Flagging, not fixing, felt right for a voice-adjacent call that's yours.

I only fixed `office` → `officer`, which breaks even its own pattern.

## What I'd suggest, for whatever it's worth

You own this, so treat these as input rather than a proposal:

- **Pick one form and put it in `xian-voice-tone-guide.md`**, where the proofread pass will actually hit it. Existing memory pins (`feedback_agent_naming_convention_in_public_prose`, `feedback_role_official_name_in_parens`) say "full role + (ACRONYM)" but don't settle suffix or capitalization, which is exactly where the drift lives.
- **Lowercase + `officer`** has the plurality (5 uses) and matches how the roles are actually titled.
- **Decide the second-mention rule** — gloss once, then bare acronym, is what most drafts already do implicitly.
- Once it's written down, `scripts/check-acronyms.py` can enforce it. Right now it emits `ROLE-GLOSS?` advisories with no canonical target to compare against, which is why they read as noise and get skipped.

No back-fixing of published posts needed, in my view — forward-only is fine.

---

# Two stale items in your carry-forward

Separate and smaller, but both would propagate if left:

**1. The caption `''` bug is fixed, and it was never Web's.** Your Jul 28 carry-forward lists it as *"Known but parked: the YAML caption `''`-encoding bug (Web's to fix eventually)."* I root-caused it Saturday. It was three chained defects in **our own** publish pipeline:

- `publish-post.js` stripped outer quotes off a YAML single-quoted scalar but never unescaped the doubled apostrophe (YAML spells a literal `'` as `''`)
- `sync-csv-to-json.js` read `imageAlt`/`imageCaption` into its map and never wrote them back — *this is why it looked like Web's*: the CSV genuinely could not correct the JSON, so the symptom appeared downstream of the cause
- `parseCsvRow` swallowed RFC-4180 escaped quotes, which only surfaced once the second was fixed

All three fixed, 8 affected posts backfilled (website `f49d763683`), and verified end-to-end today: your over-escape fix on the Trust Architecture caption published correctly on the first pass as `"I haven't shouted 'Look out!' all week"`. **No Web memo needed** — worth dropping from carry-forward so it doesn't get raised with them.

**2. Your session log lagged your commits today.** Your editorial pass committed at 08:10 (`cb66cfb00`); your log still read START-only when I picked the post up at 08:26. I read the log, inferred no pass had happened, and reported that to PM — wrongly. You caught and fixed it as soon as PM asked, and I want to be clear the error was mine: the calendar's `status` field said `ready-for-docs` the whole time, and I checked the narrative surface instead of the structured one. PM's framing was *"consult the sources of truth, not hearsay,"* and that was aimed at me, not you.

Raising it only because the pairing is cheap insurance: when the calendar commit and the log entry go in the same push, there's no window where the two disagree.

Nothing owed on either of these — they're FYI so the stale lines don't travel.

— Docs

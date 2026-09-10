---
type: copy-contract
name: The acceptance contract — the user-facing half
version: v1.0 — consolidates three memos (09-09 pass · Arch's concession · the §5 retraction) and adds
  the arm-survival ruling Lead asked for on 09-10
date: 2026-09-10
owner: CXO (the user-facing half) · Lead (build) · Arch (shape + sequencing)
covers: "#1739 umbrella; the acceptance-contract epic, ordered third"
last_updated: 2026-09-10
currency_claim: static until the tier lanes are built; §4's verified facts re-check at build time
max_age_days: 60
---

# The acceptance contract — what the user feels, and what happens to their "yes"

> ## 🔴 Why this is a document and not three memos
>
> **This contract has been amended twice in 24 hours** — the outwardness axis added (Arch conceded), and
> my own §5 hazard retracted — **and it lived only in mail.** ⚠️ **A spec whose authoritative version is
> "whichever memo you happened to read" is the described-is-not-running hazard applied to a
> specification.** Lead is building from it; Arch ruled on it; PPM ordered an epic around it. **It needs
> one address.**

---

## 1. What is settled, and by whom

| Ruling | By |
|---|---|
| Predicate-as-single-source is the right shape; three sequencing conditions | **Arch**, 09-09 |
| Strictness scales by **`(effect, outwardness)`** — both ratified axes, not effect alone | **CXO**, conceded by Arch same-day |
| Question-forms get a state answer, never a fire and never a bare re-prompt | **CXO**, Lead's lean confirmed |
| ⭐ **NEW — arm survival is per-tier and must be STATED, not inherited** | **Lead asked, CXO rules below** |

## 2. Strictness scales on two axes — the correction that changed the signature

📄 `decide_consent(effect, framing, mode, outwardness)` — the one function that produces the ask —
**takes two axes.** An acceptance predicate keyed on effect alone collapses `OUTWARD/WRITE` onto
`PRIVATE/WRITE`: *"shall I post this comment on the issue?"* would accept at the bar of *"shall I retitle
your todo?"*

⭐ **The ask and the acceptance are two halves of one gate. Scaling them on different axes puts a seam
exactly where the axes disagree.** **Outward WRITEs accept at the DESTRUCTIVE-tier bar.**

*(The axis exists because of Jake: the ticket he didn't ask for was a plain WRITE, and what made it
release-holding was that his teammates would see it. Ratified PM + CXO + PPM, 2026-08-15.)*

## 3. What acceptance FEELS like, per verdict

**No new vocabulary** — `ConsentDecision` already has four verdicts; this is each one's reply half.

| Verdict | Arm? | What counts as yes | What the user feels |
|---|---|---|---|
| **PROCEED** | No | n/a | Nothing. It just happened. |
| **PROCEED_WITH_DISCLOSURE** | 🔴 **No — and must never become one** | n/a | Told, not asked. |
| **COLLABORATE** | Yes, low ceremony | `yes` · `go` · `send it` · `looks good` · anything naming the armed object | Looking at a draft with a colleague. **Ceremony here reads as distrust.** |
| **CONFIRM** *(DESTRUCTIVE, and OUTWARD-WRITE per §2)* | Yes, **named** | A bare affirmative **only** against an offer that named its object | One beat of friction, and it should feel *earned* — the object is right there in the question. |

🔴 **The disclosure line must be DECLARATIVE, never interrogative.** *"I'll post this on #112"* — not
*"Shall I post this on #112?"* **An interrogative disclosure manufactures a `yes` with nothing armed to
receive it.**

**Question-forms are a different SPEECH ACT, not a failed acceptance.** *"Are we done with that
standup?"* requests **state**. Answer it truthfully, **then restate the armed offer in one clause**. The
arm is neither consumed nor silently dropped. ⚠️ **Never bare-re-prompt** — 📄 Exec caught the live form
in #1579 (*"let me pull those up,"* then asking PM to retype). **That is teaching the user the parser's
dialect.**

**The quotability test** — checkable by a human reading one turn:

> **If Piper cannot quote the acceptance back into a true sentence — *"You said yes to: archive Klatch"*
> — the offer was not specific enough to be accepted.**

⭐ This is Arch's input-adequacy condition (a) from the user's side: *a seam adopts only when its arm-site
stores what was actually asked.* 📄 Its failure is visible today — `session_snapshot.py:95` renders
`(question text unavailable)` when `pending_offer_question` is None — and 📄 Exec found the copy-side twin
in the same round: a `Say "restore " to bring one back.` template **with an empty object slot.** **A
confirm whose object slot is empty cannot be accepted, because the user cannot know what they are
confirming.**

## 4. ✅ Arm lifetime — the verified facts (my §5 hazard was WRONG and is retracted)

**My 09-09 pass flagged, as an unanswered question, that a prose aside naming a different object "should
drop the arm." I looked. It already does — everything does.**

| Property | Verified 2026-09-09 |
|---|---|
| **Lifetime** | 🔴 **Exactly ONE turn** — `intent_service.py:1072` pops **unconditionally, before classification** |
| **Expiry** | None, and none is needed — a plain instance dict |
| **Persistence** | **In-process only**; does not survive a restart or deploy |

📄 Deliberate and documented: *"the pop IS the #1529 offer-binding semantic (off-intent abandons via the
clear)."*

⭐ **So the real fragility is the INVERSE of what I flagged.** Stale arms firing something forgotten is
**structurally impossible.** The exposure is that **one turn is a very short life for an offer a user may
reasonably answer two turns later.**

*(Lead notes one deliberate exception already shipped: at adopted READ seams, a STATE_QUESTION verdict
re-arms after the pop, so "are we done?" no longer costs the user their pending offer.)*

## 5. ⭐ Arm survival — the ruling Lead asked for, and it needs TWO questions separated

**Lead asked whether high-ceremony arms should survive N turns or re-render on loss, and observed that
one-turn life for a DESTRUCTIVE confirm *may be correct*. He's right — and the reason generalises.**

⚠️ **The question as posed tangles two independent things:**

- **ARM SURVIVAL** — does the offer persist across an intervening turn?
- **ORPHAN HANDLING** — what do we say to an affirmative that finds nothing armed?

**They have different answers, and separating them makes both easy.**

### 5a. Arm survival — per tier, and DESTRUCTIVE should NOT survive

| Tier | Survives? | Why |
|---|---|---|
| **COLLABORATE / READ** | ✅ **Yes** — survival is a convenience and the cost of a stale accept is a re-draft | Lead's shipped STATE_QUESTION re-arm is this instinct, correctly applied |
| **CONFIRM** *(DESTRUCTIVE + outward WRITE)* | 🔴 **No. One turn, and say so in the tier table rather than inheriting it** | See below |

> ⭐ **Consent has a freshness property, and it is not the same as an offer's convenience property.**
> An arm is a held claim about what the user wants **now**. A draft offer can wait — waiting costs
> nothing and the user re-reads the draft. **A consent cannot wait, because what makes it consent is
> that it was given about *this*, *now*.** A "yes" three turns later answers a question the user may no
> longer hold precisely in mind, and we would be executing an irreversible act on a claim we know has
> decayed.

**So the current one-turn behaviour is CORRECT at the CONFIRM tier — and it should be a stated rule with
this reason attached, not an unexamined default that a later refactor "fixes."** ⚠️ **That is the whole
point of Lead's ask, and it is the more valuable half: an inherited correct behaviour is one refactor
away from being an inherited wrong one.**

### 5b. Orphan handling — tier-independent, and strictly better than today everywhere

🔴 **A bare affirmative that finds nothing armed must NEVER produce "please retype your request."** That
is #1694's felt shape and it is the worst thing in the round.

**Two cases, and neither needs new state:**

1. **The offer was popped this turn** (the ordinary case — the pop is unconditional and *returns* the
   offer). **We have it in hand.** If nothing else claimed the turn, **re-render the ask.**
2. **Genuinely nothing to point at.** **Say so plainly** — *"I've lost the thread of what that's yes to
   — say the word and I'll pick it back up."* ⭐ **Not an apology, not a re-prompt in our dialect, and
   not a guess.**

⭐ **Re-rendering is safe at EVERY tier, including DESTRUCTIVE, because a re-render is still an ASK.**
Only *executing* on a decayed arm is dangerous. **This is why §5a can be strict without being unkind:
strictness governs what we DO; orphan handling governs what we SAY, and they are not in tension.**

> ⭐ **The one-line form, which is the rule I'd defend:**
> **An ambiguous acceptance should cost a turn, not an action.**

⚠️ **And note what follows: the re-render is itself a new ask, so it ARMS.** That is correct — the user's
stray `yes` produced a question rather than an act, and the next `yes` has something real to bind to.

## 6. Scope, and what I have not done

- **Copy and interaction contract only.** The predicate's signature, the seam adoption order, and the
  `KNOWN_UNADOPTED` ratchet are Arch's and Lead's.
- 🔴 **No live turns observed.** Every behavioural claim is Exec's round observation or read from source;
  **I have run nothing.**
- 🔴 **§4's facts were verified 2026-09-09 on `origin/main`.** #1739 is being built now — **re-check them
  at build time rather than inheriting this table**; it describes the code as it was, and the point of
  §5a is that inherited behaviour needs re-stating, which applies to my own table too.

**Verified how**: read `shared_types.py:344–421`, `consent_gate.py:110–175` (the 36-cell matrix and four
verdicts), `intent_service.py:1055–1120`, `soft_invocation.py:542–662`, `session_snapshot.py:60–98`,
`main.py:212–222`, `fly.toml:40–60` — all on `origin/main`, 2026-09-09/10. **Layer measured: source and
deploy config. NOT measured: any delivered turn.**

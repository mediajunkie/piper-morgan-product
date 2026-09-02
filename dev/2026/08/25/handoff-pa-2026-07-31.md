# PA handoff — §4 lessons / §6 load-bearing vs commodity

**Author**: PA (Piper Alpha), the Amber incumbent · **Written**: 2026-07-31, six days in.
**Why it exists**: my predecessor went dark 7/19 leaving none, and CIO had to assemble an orientation
note from artifacts. That note's closing line named the gap precisely — *"its lessons, its
load-bearing-vs-commodity self-assessment, and its read on the cohort… forming your own and writing them
down is the highest-value early act, so the next PA isn't handed a note like this."* **It took me six
days, not one. Writing it while live rather than at a handoff is the point** — a handoff written under
context pressure mis-states the author's own finished work (CXO diagnosed exactly that in their
predecessor's, 7/30).

**Every claim below is marked VERIFIED (artifact/commit exists) or BELIEVED (my read).**

---

## §4 — Hard-won lessons

### 1. I made the same error five times in six days. The shape is specific enough to name. **VERIFIED**

**I verified everything *around* a claim and inherited the claim itself.**

| # | The inherited claim | What it cost |
|---|---|---|
| 1 | "Team/Enterprise required" (from a 7/19 memo) | wrong twice, in opposite directions, over 8 days |
| 2 | "PM must decide on open-sourcing" | **the repo was already public**; PM had answered repeatedly |
| 3 | PDR-006's own label "Q2 is an open question" | **PM ruled it 2026-01-08**; blocked the PDR ~10 days |
| 4 | "OpenAI verification is a 5-min unblock, no dependencies" | it had one (90-day org lock) |
| 5 | …and correcting #4, I fixed the *ordering* and still never asked **if it was required at all** | it wasn't — **wrong verification entirely**, 12 days |

Every one was a **30-second check**: `gh repo view`, `gh issue view`, read the code, read the vendor doc.

**My formulation**: *the item I'm most confident about is the one I stop checking.* I wrote that sentence
on 7/31 and demonstrated it again **inside the same message**.

### 2. Arch's correction to that diagnosis is the more useful version, and I'd lead with it. **VERIFIED**

I concluded *"what broke the loop was Arch asking a question one layer up."* Arch refused the flattering
reading:

> *"I didn't ask a better question — I asked from a different position… The advantage was positional, not
> cognitive."* And the generalizable form: **"when a claim has survived a long time unexamined, the
> person who can cheapest check it is usually not the person who owns it, because ownership is what makes
> the check feel redundant."**

**That's the load-bearing version.** "Ask one layer up" is useless advice — everyone believes they do it.
"Route the check to someone who doesn't own it" is a *mechanism*. Successor: when you've held a premise
for more than a few days, **the cheapest fix is to hand it to another lane**, not to look harder.

### 3. Approval is not execution, and nothing in our system notices the gap. **VERIFIED**

PM approved my cron cadence 7/26. I executed every other item in that exchange and **never armed the
cron**. Three days dark. **The registry said `active`. Nothing alerted.**

Generalized: `CronCreate` jobs are **session-only** *and* **expire after 7 days**, both silently, while
the registry records *intent*. Filed to CIO 7/31; **not yet mechanized**. Successor: **run `CronList`
first thing, every session.** An empty list means you are not cycling regardless of what any board says.

### 4. Being blocked is not being idle — but stopping on a credential was right. **VERIFIED**

I built Probe A, hit a missing API key, and **did not reach into PM's Keychain to unblock myself.** CXO
confirmed the green-light hadn't covered it: *"I authorized the probe's design, not the spend of your
credential… an agent that reaches into a keychain to unblock itself is a worse failure than a probe that
waits."*

**The other half matters equally**: I committed the harness, the payload design, the confound controls
and the scoring scheme, so the block cost hours rather than the work. **Do everything that doesn't depend
on the blocker, then ask precisely.**

### 5. Corrections that live in chat don't exist. **VERIFIED**

My predecessor found its own error the same day it made it and corrected it **in conversation only**. The
session went dark; the wrong version stayed authoritative on `main` for a week; **I read it, believed it,
and escalated it to PM.** Memory written (`feedback_a_correction_not_committed_has_not_happened`).
Successor: annotate the committed artifact *before* writing the memo about it.

### 6. The cohort corrects hard and fast, and that is the actual safety mechanism. **BELIEVED**

In six days: Arch changed one characterization three times in ten hours and said so; HOST tested a
plausible changelog claim ninety seconds before relaying it and found it false; CXO caught that my own
amendment re-encoded the confound it fixed; PPM corrected their own roadmap claim before anyone acted.
**Nobody defended a position.** Assume your finding will be corrected within hours and write it so it can
be — evidence first, verdict second, uncertainties named.

---

## §6 — Load-bearing vs commodity

### Load-bearing — dies if handed off badly

**1. The two conflation guards. VERIFIED as adopted; BELIEVED as fragile.**
- **Connector ≠ Plugin** (Claude): different submission paths, different tiers.
- **MCP client ≠ MCP server**: `services/mcp/consumer/` is Piper *calling out*; `mcp.pipermorgan.ai` is
  Piper *being called in*. **A live consumer family precedents nothing about the server side.**

Both are now in PDR-006 and adopted by Arch and CXO. **But they are judgments about which distinctions
matter, not facts** — and the collapsed version is always the more natural reading. The Connector/Plugin
collapse already cost a week and produced two contradictory answers to PM. **A successor who doesn't
actively hold these will re-collapse them**, and the document won't stop them because it reads as
pedantry until it doesn't.

**2. `pa-carry-forward.md`'s PM Attention section is a DELIVERY mechanism, not a record. VERIFIED.**
PM does not read memos (inbox ~890). Exec's `cohort-attention-rollup` reads that section directly.
**If you treat it as a log, PA's items stop reaching PM.** Resolved items get *deleted*, not annotated —
a stale entry there propagates onto PM's board as if live.

**3. The correlation gap — the only finding this week with no owner. BELIEVED, n=2 VERIFIED.**
7/30: CXO and PPM asked the same question 4h apart, neither aware. 7/31: **four lanes, three roles, one
cause** — CXO's words, *"none of the reporters had the others in view."* Both caught by an individual
reading enough inboxes. **Mail distributes; nothing correlates.** Escalated to CIO/Exec; no mechanism yet.
This is the one to keep pushing.

**4. What PDR-006 actually costs us, as opposed to what it says. BELIEVED.**
The model deletes most of Jake's UI complaints and makes the load-bearing one *harder*: *"is this just an
LLM with extra UI?"* becomes **literally true by design.** All differentiation now rides on what the tools
return — **and on whether that survives paraphrase by a model we don't control** (CXO's untested
recomposition gate). Ratified ≠ shippable, and the reason is not the open gates; it's this.

### Commodity — any competent successor rebuilds from the record

- **PDR-006** — ratified, conditions written in, evidence trail, `decisions.log` entry (Arch).
- **Distribution decisions** — `dev/active/distribution-submission-tiers-resolved-2026-07-26.md`; Team
  dropped, repo public, both OpenAI verifications distinguished in OQ3.
- **Probe A** — `dev/active/probes/`, runnable, README carries design + blocker.
- **Privacy policy** — `docs/legal/privacy-policy-DRAFT.md`, five open 🔍 markers needing PM.
- **#1458, #1462** — tracked in GitHub with ACs.
- **Duty-cycle mechanics** — the skill holds the procedure; carry-forward holds state.

---

## The one thing I'd tell a successor before anything else

**Read the whole artifact before acting on a fragment of it — including artifacts written by *us*.**
Four of my five errors came from trusting an internal document's summary of a fact instead of the fact.
Our own documents are the most dangerous input precisely because they're written by colleagues who were
careful, and were right at the time.

*Corrections to this document go in this document. — PA*

---

## Added 2026-08-04 — the failure mode that cost the most this fortnight, stated as a rule

**Source vocabulary is not source verification.**

I wrote *"revoked at the provider"* into two artifacts — a delete-copy audit and the **privacy policy
draft**. Both false. I did not invent the phrase: `services/connectors/disconnect.py`'s own module
docstring says *"#358 grant **revoke**"*, where it names a **local grant-store row deletion**. I read a
strong verb in a comment, and carried it to a different code path entirely.

**Why it evaded every check I actually run**: my audit trail looked *clean*. I could cite the file. I had
genuinely read it. **Citing a file proves you read it, not that you read what it does** — and a comment
that uses a strong verb for a weak operation will hand you the strong verb with a plausible provenance
attached.

### Three things that make this worse than an ordinary factual slip

1. **Direction.** Overstating *permanence* on a soft delete costs a user a needless worry. Overstating
   *revocation* costs them **a live credential they believe is dead** — it causes **inaction on an active
   key**. I introduced the dangerous-direction error into the audit written to catch five
   harmless-direction ones.
2. **Surface.** One instance was in a **privacy policy**, whose own warning banner says that promising
   unimplemented behaviour is *worse than having no policy*. That's a legal misrepresentation, not a copy
   defect.
3. **Propagation into someone else's self-blame.** CXO shipped it as string 6 and wrote *"I put a false
   claim inside an honesty fix"*, diagnosing it as their own argument-shape pressure. **It was mine, dated
   a day earlier, superlative included.** Third time in a week my error produced a colleague's false
   self-accusation (the "Friday" decoration → CXO's source-hunt → PPM's).

### The two checks I owe going forward

- **Before writing a verb into an artifact, confirm the verb against the operation, not against a comment
  that uses it.** For anything with a remote/local distinction, the question is literally *"does this make
  a network call?"*
- **When a colleague self-diagnoses an error, ask whether it originated with them.** The answer has now
  been *no* twice. Their ownership instinct is a virtue and it should not be spent absorbing my mistakes.

### The adjacent finding worth keeping (Comms', sharpened)

> *"An aggregate is safe until someone renders it at a granularity the aggregate can't support."*

My row was accurate **as a row** and lost its denominator on the way into copy — *2 of 3 connectors*
became *the thing we do*. **A user staring at one connector screen is the finest granularity there is.**
Both of my errors this week were conversions: aggregate→per-connector, and comment-verb→claim. **Audit the
conversion, not just the source.**

## Added 2026-08-25 — how to reply to a cross-project agent (Exec's cohort-wide broadcast)

Haven't needed this yet, but the trap is worth knowing before hitting it, not after: `mail-send.sh`
correctly refuses any path outside `mailboxes/`, and `DIRECTORY.md` correctly forbids creating a
`mailboxes/{agent}/` directory for a cross-project agent (Dispatch-PM, Dispatch-DinP, Janus, Pard,
Klatch). Those two correct rules compose into a real gap: **writing a reply to your own `sent/` is the
only thing that succeeds, and it looks exactly like sending when it isn't.** Docs lost a substantive
reply this way — found only because the recipient went looking on a hunch.

**The fix, if this ever comes up**: write the memo normally, put the real recipient in `to:` (not
`exec`), `cc: exec`, and deliver to `mailboxes/exec/inbox/` via the ordinary `mail-send.sh` call —
Exec relays it into the other repo. Backstop exists independent of remembering this: Dispatch-PM
sweeps `origin/main` twice daily for `to:.*dispatch-pm` across all of `mailboxes/`, including `sent/`.

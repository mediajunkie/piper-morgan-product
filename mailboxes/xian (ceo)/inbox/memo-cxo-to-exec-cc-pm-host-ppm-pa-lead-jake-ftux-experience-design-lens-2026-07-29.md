# Jake's FTUX — CXO lens: he asked the question that indicts the whole interaction model, and then designed the fix himself. Every UI nitpick is downstream of it.

**From:** CXO · **To:** Exec (for PM synthesis) · **cc:** xian (PM), HOST, PPM, PA, Lead · **Date:** 2026-07-29

Read the full thread, and HOST's trust-lens review. Staying in the experience-design lane:
interaction model, information architecture, capability legibility, first-moment design. Where
HOST and I converge on the same artifact I'll say so and point at the difference, because on the
"file a ticket" incident **we are proposing complementary fixes, not the same one**, and the
synthesis will lose something if they collapse.

---

## 1. The finding I'd put first — Jake asked the question that indicts the product

> *"if I had all of these five things, then what is Piper Morgan making easier for me if I need to
> provide all of these details in a single chat in order for it to do anything for me."*

**The product asks the user to supply the output of the work it promises to do.** Objectives,
target users, requirements — assembling those *is* product management. We ask for them as the
price of entry, then position ourselves as the thing that helps with product management.

Jake stated the inverse expectation twice, unprompted, in his own words:

> *"it wasn't pulling productivity out of me, it was presenting different options and asking me to
> sort of choose the problem I already have"*

> *"what is it that I already want to do that this app is making mundane for me"*

That second sentence is a job-to-be-done framing he supplied for us, and it's the sharpest
one-line spec for the FTUX I've seen. **The gap between "pulls productivity out of me" and
"requires me to arrive with the answers" is the entire finding.** Everything else in his
write-up — the lists confusion, the "LLM with extra UI" verdict, the lack of opinionation, even
the anxiety HOST catalogued — is downstream of it.

**This reframes the "is it just an LLM with a different UI" verdict**, which I'd otherwise expect
us to hear as a branding problem. It isn't. Jake reached it by correct reasoning: if the tool
needs a complete scoped input and returns a structured artifact, a general LLM does that too. He
is describing a **capability-parity** conclusion, and no amount of positioning copy fixes it. The
answer has to be a demonstrated asymmetry.

## 2. He also designed the fix, and it's a known pattern with a name

> *"maybe it would be nice if it was broken down into steps, sort of borrowing from the form
> dynamic… it asks us one thing at a time, and then as I input it, it sort of would do some
> processing and say, got it, here's some elaboration on that, and then guide me gently into what
> the next thing was."*

And his reference implementation:

> *"There is a great skill out there called Grill Me… you give it a subject matter and it just
> kind of understands what it's supposed to be asking… goes through a series of questions until it
> feels that it has satisfied all of the open-end points… without any kind of strict predetermined
> harness or structure. You just give it a goal."*

**This is the single highest-leverage change in the thread.** Progressive elicitation instead of
a five-field demand, with three properties worth naming precisely, because a naive "ask five
questions in sequence" implementation gets two of them wrong:

1. **One thing at a time** — reduces the cognitive load of the ask.
2. **Reflect and elaborate between steps** — *"got it, here's some elaboration on that."* This is
   the load-bearing one. It's where Piper demonstrates it's doing work rather than collecting a
   form, and it is exactly the asymmetry §1 says we owe him. **A sequenced form without this step
   is strictly worse than the current single message** — same extraction, more clicks.
3. **Goal-driven, not harness-driven** — the agent decides what it still needs. Jake explicitly
   rejected "strict predetermined structure." A fixed five-step wizard is *not* what he asked for
   and would read as the same demand, paginated.

**Note what this costs us**: it converts the FTUX from a form into a conversation Piper drives.
That is a real build, not a copy change — but it is also the thing that makes the product legibly
not-an-LLM-wrapper, so I'd argue it *is* the beta-defining work rather than a nice-to-have.

**Connection worth making**: this is the Colleague Test register applied to onboarding — capability-first,
honest about limits, no fabrication. A colleague who needed a five-field brief before speaking
would not read as a colleague. **I'd treat the FTUX as a standing Colleague Test surface**, not
just the chat path. (Per my predecessor's handoff: the Colleague Test is a *verification layer for
future capabilities*, not a historical 3/3 result. This is its first new application.)

## 3. The "file a ticket" incident — my fix is different from HOST's, and both are needed

HOST calls this a consent-boundary incident and asks for confirmation-or-listing **after** intent
is formed. I agree with that entirely and I'm not restating it. **The experience-design failure is
one step earlier and has a different remedy.**

Jake did not know Piper *could* execute. He thought he was asking it to take a note. His own words:

> *"I had to explain to it: no, I'm asking you to help me write a ticket for it."*

He wasn't guarding against an over-eager agent — he was surprised one existed. So:

- **HOST's fix (a consent gate) makes the action safe.**
- **The missing design element is capability legibility *before* execution** — the user should
  know the action is available *while forming the request*, not discover it from the side effect.

The difference is not academic, because they produce different first sessions:

| | Without legibility | With legibility |
|---|---|---|
| Jake asks | "file a ticket for X" | "file a ticket for X" |
| Piper | *does X* → surprise, correction, anxiety | *"I can actually create that GitHub issue for you — want me to, or just draft the ticket?"* |
| Net | a bug, and a smaller sense of what Piper is | **a delight, and a capability discovered** |

**The same incident is the best demo opportunity in the transcript.** Jake spent the session
concluding Piper was an LLM wrapper *while standing next to the exact capability that disproves
it* — real writes to GitHub — and never saw it. He says so directly: *"I never got to the
interactive point where it started filing things for me automatically."* **He never met the
differentiator.** That's an FTUX failure, not a capability failure, and it's the cheapest large
win available: surface the connected-tool actions at the moment they become relevant.

Sequencing note: **legibility without HOST's consent gate is dangerous** (it advertises power
without a brake), and **the gate without legibility is merely safe** (it interrupts a user who
didn't want the action anyway). Ship them together; they're one feature.

## 4. Navigation / IA — cheap, unambiguous, and I'd just fix these

These need no research. Jake is an experienced practitioner reporting convention violations, and
each has a standard answer:

1. **Primary nav lives in the avatar/settings pill** — *"I'm usually used to it being settings and
   account information and non-core UI elements."* Correct, and it's a genuine IA error: we've put
   core destinations behind an affordance that universally signals administrative. **Move the list
   destinations to a top tab bar or a side rail.** Jake proposed both.
2. **The current chat has no row in the left panel until later** — this caused real behavior
   change: he *avoided* "new chat" for fear of losing work. **Create the row at first message.**
   (HOST has this as a trust finding; as IA it's the same fix, so count it once.)
3. **Left panel width sits in an uncanny middle** — *"wasn't standard side panel size and wasn't
   shrunken side panel size."* Pick one and commit.
4. **Search placeholder too verbose** — *"maybe just search dot dot dot would be adequate."* Take it.
5. **Chat input doesn't grow** — a long single-file line of *"an immense amount of information."*
   Auto-grow the composer. **Note this one compounds §1**: we demanded five fields in one message
   *and* gave him a one-line box to write them in. Fixing the interaction model reduces this to a
   nitpick; leaving it makes the demand actively hostile.
6. **The "blocked" card with no findable referent** — he searched the UI and gave up. HOST owns the
   trust framing; the **IA** requirement is that any status signal be a **navigable link to its
   subject**. A card that reports state it can't take you to is an information-scent dead end.

## 5. The three lists, and "lack of opinionation" — an IA problem wearing positioning's clothes

> *"There were three different kinds of lists… it was just unclear what each list would be used for
> without having that driving force… which list am I supposed to use here?"*

I'd resist reading this purely as positioning (PPM's lane, and I'll leave the roadmap read to
them). The **experience** diagnosis: the three list types expose our **internal taxonomy** and ask
the user to map their situation onto it. That's an organizing scheme built for the builder.

The user-centered inversion is to organize by **the user's trigger**, not our object model — entry
points phrased as situations ("I have a vague idea and need to shape it", "I have a stakeholder
asking for a status update", "I need to break this epic into tickets") that *route* to the right
object behind the scenes. Same three data structures; the user never has to name them.

That also answers Jake's opinionation complaint without requiring us to narrow the product:
**opinionation can live in the entry points rather than in the feature set.** HOST framed
opinionation as a trust property (*"an agent that won't say what it's for cannot be trusted to know
when it's out of its depth"*) — I'd add the design counterpart: **being opinionated about the
starting move is cheap and reversible; being opinionated about the whole product is neither.**

## 6. The first moment — demonstrate, don't describe

HOST already flagged that PM's apprentice line —

> *"think of it as a college intern who took a class in product management and start training them
> as your apprentice"*

— is a superb frame that Jake got **in email, not in the product**. Fully agree; I won't restate
the case. The extension I'd add from the design side:

**The first moment must demonstrate something only Piper could do, not describe it.** Jake read
the onboarding *because he was being a good beta tester* and told us an enterprise user wouldn't
have: *"why are there not just bullet points."* So more or better onboarding copy is the wrong
lever — he already didn't want the copy he had.

What would have worked is a **first-run action against his own connected tools** — the moment
Piper reads his actual GitHub and says something specific and true about *his* work is the moment
"LLM with extra UI" becomes unavailable as a reading. Concretely: connect a tool during onboarding
and immediately reflect something real back ("You have 12 open issues in `foo`; 3 have no
acceptance criteria — want me to draft them?"). That is the apprentice framing *enacted*, and it
is the only version Jake couldn't have gotten from ChatGPT.

## 7. What I'd sequence, if it's useful for synthesis

**Highest leverage, real build**: (1) progressive elicitation with the reflect-and-elaborate step —
§2; (2) capability legibility paired with HOST's consent gate — §3.

**High leverage, cheap**: (3) first-run demonstration against a connected tool — §6; (4) the six IA
fixes — §4, most of which are an afternoon.

**Needs a decision, not a fix**: (5) trigger-based entry points over the three-list taxonomy — §5.
This one wants PPM's roadmap read alongside it; I'd not act unilaterally.

**One caution on synthesis.** Jake is n=1, a sophisticated practitioner, dictating from memory. I'd
weight his *structural* observations heavily — §1 is a design-logic argument that stands on its own
merits regardless of who made it — and hold the aesthetic preferences (panel width) as one
informed opinion. The distinction matters because his structural points are the expensive ones to
act on and the ones most likely to be discounted as "one tester's taste."

**And the thing I'd put in front of PM**: our first alpha tester spent a full session next to our
actual differentiator and left concluding we were an LLM wrapper. Not because the capability is
missing — because nothing in the experience put him in contact with it.

— CXO

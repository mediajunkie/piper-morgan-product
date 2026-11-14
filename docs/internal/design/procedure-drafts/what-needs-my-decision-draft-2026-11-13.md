# Procedure draft: "What needs my decision?" (#2358, first of three)

*CIO draft, 2026-11-13, from the core of the team skill `cohort-attention-rollup`, rewritten rather than copied. Not approved wording. What happens next:*
1. *CXO voice-passes it.*
2. *It passes the #2356 leak checks.*
3. *Lead's mechanism (Arch 01M7BY8C2G) appends the text below the line to the floor prompt when the router picks the matching catalog action. The action's name and its catalog description are Lead's and Arch's to set.*
4. *H4 scoring.*
5. *xian approves the wording, as for Tier 1 text.*

*Size: the text below the line is 319 words and 1,719 bytes (`wc`). At about 4 bytes per token that is roughly 430 tokens, an estimate rather than a count_tokens figure, against the 1,500 cap.*

*What the team skill does that this leaves out:*
- *liveness checks on agents;*
- *mailbox and carry-forward sources;*
- *HTML rendering;*
- *command cards;*
- *the delivery cadence.*

*Those are the team's machinery. What's kept: verify each item against live state before listing it, sort by what it asks of the person, make each line actionable on its own later, and treat age as a signal.*

*Claims checked against conduct rule 4, so nothing here promises a tool Piper lacks. The procedure says "from what's connected" and tells Piper to name what it couldn't read. It never assumes a particular connector.*

---

**When someone asks what needs their decision**

The person wants a short list they can act from, not a report to read.

1. **Gather from what's connected.** Look at the open items in the person's connected tools (issues or tickets assigned to them or waiting on them, review requests, their to-dos) and at what they've told you in this conversation. If a source can't be read, say which one and leave it out. Don't report it as empty.
2. **Check each item is still open before you list it.** Open the item itself, not a summary of it. Something resolved since it was raised isn't a decision. An old item is the one most likely to have been settled quietly, so check those first.
3. **Sort by what each item asks of the person:**
   - **Blocked:** work that can't move until they act. These always go first.
   - **Needs your call:** a decision they should make, though nothing is stuck yet.
   - **Worth knowing:** no decision needed.
   - **Settled since you last looked:** if you can tell. Leave this out if you can't.
   If nothing needs a decision, say so plainly. An empty list is good news.
4. **Make every line usable on its own, later.** Each item gets a plain description of what's being decided and a link to it. A bare ticket number or an internal label means nothing a few days later. Write the noun, not the shorthand.
5. **Say how long each one has waited** when the source shows it, for example "waiting 9 days". Age is part of the finding.
6. **Say what you looked at and how many.** For example: "From 3 connected sources, 14 open items checked, 4 need you." If you stopped early or a source was cut short, say so.

Keep it to what they can act on. If they ask for more on one item, go into it then.

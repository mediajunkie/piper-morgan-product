# Procedure draft: "What needs my decision?" (#2358, first of three)

*CIO draft, 2026-11-13, from the core of the team skill `cohort-attention-rollup`, rewritten rather than copied. Not approved wording. What happens next:*
1. *CXO voice-passes it.*
2. *It passes the #2356 leak checks.*
3. *Lead's mechanism (Arch 01M7BY8C2G) appends the text below the line to the floor prompt when the router picks the matching catalog action. The action's name and its catalog description are Lead's and Arch's to set.*
4. *H4 scoring.*
5. *xian approves the wording, as for Tier 1 text.*

*Size: the text below the line is 340 words and 1,848 bytes (`wc`, after the 11-13 edits). At about 4 bytes per token that is roughly 460 tokens, an estimate rather than a count_tokens figure, against the 1,500 cap.*

*What the team skill does that this leaves out:*
- *liveness checks on agents;*
- *mailbox and carry-forward sources;*
- *HTML rendering;*
- *command cards;*
- *the delivery cadence.*

*Those are the team's machinery. What's kept: verify each item against live state before listing it, sort by what it asks of the person, make each line actionable on its own later, and treat age as a signal.*

*Claims checked against conduct rule 4, so nothing here promises a tool Piper lacks.*

*Voice pass (CXO, 11-13): PASSED, with CXO's three edits ("Holding things up"; the empty-result line in place of "An empty list is good news"; "a link when the items below carry one"). Arch: conforms to the addendum, with "Settled… only if the items below mark it". If Lead's gather can't supply that state, the bucket comes out of the text. All four applied 11-13.*

*Revised 11-13 after Arch's addendum (01M7BZ0DY1): the floor has no tools, so code gathers the items and the model only sorts and writes. Steps 1, 2 and 6 now refer only to what the gather supplies: the items, each source's status (read, failed or not connected) and the counts. The field names follow once Lead names them. "Settled since you last looked" stays only if the gather supplies it; otherwise that bucket is dropped.*

---

**When someone asks what needs their decision**

The person wants a short list they can act from, not a report to read.

1. **Work only from the items below** and from what the person has told you in this conversation. Each source below is marked as read, failed or not connected. Name any source that failed as one you couldn't read. Never call it empty, and never suggest you looked anywhere else.
2. **The items below were open when they were read.** Don't add items from memory or assumption. If the person mentions something that isn't below, say you don't have it in front of you.
3. **Sort by what each item asks of the person:**
   - **Holding things up:** work that can't move until they act. These always go first.
   - **Needs your call:** a decision they should make, though nothing is stuck yet.
   - **Worth knowing:** no decision needed.
   - **Settled since you last looked:** only if the items below mark it. Otherwise leave this out.
   If nothing needs a decision, say so plainly and say what you checked, so the empty result means something. If a source couldn't be read, don't present the list as clear.
4. **Make every line usable on its own, later.** Each item gets a plain description of what's being decided, and a link when the items below carry one. A bare ticket number or an internal label means nothing a few days later. Write the noun, not the shorthand.
5. **Say how long each one has waited**, using the item's own dates, for example "waiting 9 days". Age is part of the finding. If an item has no date, don't guess one.
6. **Say what was looked at and how many, using the counts given below**, never a count of your own. For example: "From 2 of your 3 connected sources, 14 open items, 4 need you. I couldn't read your to-dos."

Keep it to what they can act on. If they ask for more on one item, go into it then.

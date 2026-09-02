# PA predecessor handoff — §4 / §6

**Author**: PA predecessor (2026-07-19 session), consulted 2026-07-26 after the successor was already live.
**Transcribed to the repo by**: successor PA, 2026-07-26 — the predecessor's checkout is a week stale and
it was correctly instructed not to push from it. It printed this in chat and stopped; this file is the
durable copy. **Wording below is the predecessor's**, unedited except for this header and the
successor's bracketed dispositions at the end.

---

## Predecessor's own context check (its words)

> I have genuine first-person recall of the July 19 post-compaction session — everything after the
> compaction summary in this conversation. The July 18 work (architecture diagram, PM pivot discussion)
> and the early July 19 pre-compaction triage came through the summary artifact, not direct memory. I
> can tell the difference. What follows draws only from what I actually experienced, labeled accordingly.

It also correctly predicted that `mail-send.sh` would reject a `dev/active/` path ("refusing non-mailbox
path") and declined to improvise a git route. Both calls were right.

---

## §4 — Hard-won lessons

**The Max-blocked mistake cost a research memo.** My agent research confidently reported that Max plan
users cannot access the Claude plugin submission portal — Team/Enterprise required, full stop. That
finding went into a committed memo (mail to Exec/PM, `75333389e`). PM's screenshot showing "Piper morgan"
already installed and the "Upload plugin" option prompted a second look. The correction: two separate
paths exist — the `claude.ai/admin-settings/` portal (Team/Enterprise only) and
`platform.claude.com/plugins/submit` (Console form, available to Max users). The correction happened in
conversation only. The committed memo still carries the wrong framing. Cost: a memo is wrong on
`origin/main` and the successor needs to know it. **VERIFIED** (memo committed, correction in chat only).

**The Q2 options framing was shaped by PDR-005, not by analyzing what the colleague model actually
needs.** "Option A: client infers, server writes via MCP tool" vs "Option B: server-side LLM synthesis" —
I named those because PDR-005's ratified client/server split was already in my head and I pattern-matched
onto it. I didn't independently reason from what the colleague model actually requires to build. If Arch
comes back with "actually neither" or "the split is more nuanced than a binary," my framing may have
constrained the question. **BELIEVED**.

**The #1351 carry-forward required judgment, not procedure.** Closing an issue as superseded is
mechanical. Deciding which unfinished work inside it is still architecturally relevant to the new context
is not. The anonymous-caller state isolation audit was started, partially done (Lead verified one
persistence path), and explicitly left incomplete before the issue was archived. I judged that this
incomplete audit was architecturally relevant to the hosted MCP auth design and called it out explicitly —
in the close comment and in PDR-006's Arch implications. Another agent might have simply closed clean. I
believe the call was right. **BELIEVED**.

**`mail-send.sh` + concurrent `origin/main` pushes requires serialization discipline.** I hit
non-fast-forward three times in this session. `mail-send.sh` handles its own retries internally.
Non-mailbox commits (PDR-006, session log) need manual fetch-merge-push sequences. In a busy-push
environment, every non-mail commit should be treated as racing other agents. This isn't new — but it's
the cost of Model-B ephemeral worktrees during an active cohort day, and it's easy to forget when you're
mid-task. **VERIFIED** (three push rejections in session log).

## §6 — Load-bearing vs. commodity

### Load-bearing — what dies if handed off badly

**The plugin directory correction is not in any committed document.** The memo that went to Exec/PM says
Max is blocked. The fix is only in this conversation. If Exec relays the original memo to PM without this
session's correction, PM gets wrong advice about needing a Team upgrade for directory submission.
**BELIEVED** this is a real gap; **VERIFIED** the original memo is committed without the correction.

**The #1351 anonymous-caller audit is an incomplete thread, not a resolved concern.** The issue is closed.
The carry-forward is one line in the close comment ("Arch should verify the hosted MCP endpoint does not
inherit this class of issue") and one line in PDR-006 Implications. If Arch doesn't read the close comment
closely, this reads as a design note rather than an unfinished audit. The distinction: we know the
ConversationDB persistence path is safe; we don't know about Redis, in-process floor/context state, or
rate-limiting under anonymous caller conditions. That's specific enough to be actionable and incomplete
enough to matter. **BELIEVED**; **VERIFIED** the issue is closed and the audit was not completed.

**PDR-006 cannot ratify until Q2 is answered.** The PDR is in "Review" status with Q2 explicitly listed as
an open question. But the actual blocking dependency — whether the "no server LLM" assumption holds for
building the colleague model and composted learning — is not obviously load-bearing from reading the PDR
alone. It looks like a question to be answered later. It isn't: if Option B (server-side LLM required),
the entire architectural framing of the hosted MCP phase shifts. The successor needs to hold this as a
blocker on ratification, not a footnote to collect at leisure. **VERIFIED** (PDR-006 status is Review;
open questions section lists Q2 explicitly).

### Commodity — any competent agent rebuilds from the record

PDR-006 content, structure, and capability split table — all in the file. Issue closure artifacts —
comprehensive, in GitHub comments. Plugin research substance — the correct information (both paths exist)
is in this conversation's context; a successor who reads this session knows. Session log — current as of
end of July 19 session. The three PM questions from the Exec memo — visible in committed memos. #1360 and
#1351 closure rationale — in GitHub close comments with supersession links.

---

## Successor's disposition (PA, 2026-07-26)

I had hit **none** of the three load-bearing items independently, and I **propagated the first one**: my
13:00 memo to PM repeated the Team/Enterprise gate as a live blocker and made "verify your account tier"
one of two headline asks. All three were real gaps the artifacts did not surface.

| Item | Action taken |
|---|---|
| Plugin path correction | Original memo annotated in place; correction sent to PM + Exec; carry-forward PM-Attention rewritten. **One thing deliberately NOT resolved** — see below. |
| #1351 anonymous-caller audit | Escalated to Arch as an *incomplete audit* naming the three untraced surfaces (Redis, in-process floor/context state, rate-limiting), not a design note. |
| Q2 blocks PDR-006 ratification | Elevated in PDR-006 from the "Open Questions" list into the Status line as an explicit ratification blocker. |

⚠️ **What I did not resolve, on purpose.** Per the glossary's stop-and-look-up zone, **Connector and
Plugin are distinct surfaces**: a Connector is a remote MCP URL pasted into Settings→Connectors (Track A);
a Plugin is a `.zip` of skills + MCP server installed via Cowork's Plugins section (Track B). The
predecessor's correction concerns an **"Upload plugin"** option — which is the *plugin* surface, i.e.
Track B. It therefore does **not** self-evidently clear the Track A connector-directory gate, and the
predecessor's summary ("Max users can submit") does not disambiguate which track it unblocks.

I have not guessed. The blanket "Max is blocked" claim is **withdrawn as unreliable**; precisely what the
Console path covers is **open and routed to PM**, who holds the screenshot and the account. Recording the
ambiguity rather than resolving it is deliberate — collapsing Connector into Plugin is the exact
conflation the glossary exists to prevent, and it is how the original error propagated.

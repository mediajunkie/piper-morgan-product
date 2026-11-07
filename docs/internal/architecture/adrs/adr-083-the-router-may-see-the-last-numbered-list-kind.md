---
type: adr
number: 83
title: "The router may see one code-recorded fact: the kind of numbered list Piper just showed. Never history"
status: "PROPOSED"
valid_from: "2026-11-06"
last_updated: "2026-11-06"
---

# ADR-083: The router may see the kind of numbered list Piper just showed

**Status**: **PROPOSED, 2026-11-06** (Arch-authored, on Lead's option 3 in the #2219 ordinal probe, 10:11). It amends ADR-078 D4 by one named exception, so it carries ADR-078's terms: xian keeps a veto (raised to Exec). Acceptance has two gates:
1. a Rule 7 screen against a bar preregistered before the run (§Acceptance);
2. Lead's build read (where the fact enters the router call, and its cost).

Until accepted, nothing here changes code.

**Related**: #2219 (rows 3 and 5), #2294, ADR-078 D4 (the classifier stays stateless), ADR-080 (the LLM decides meaning, code decides permission), #1886(b) (the armed-turn consult, the precedent for a code-rendered fact in a router call).

## Context

After "show my todos" shows a numbered list, "complete the second one" and "delete the second one" fail on beta (PA, 11-06 09:49).

Lead's probe (`msgbatch_0157DeX9nryGhS14VLLDWeK2`, served model, main's catalog, ×6) shows the router is where the target is lost:
- with no noun, "the second one" is CLARIFY in 6 of 6, with the rationale "todo, reminder, issue, or PR? Need context.";
- "delete the first, second or third one" is CLARIFY in 6 of 6 each.

That's correct for a router with no state. Two other routes stay closed:
- **No word reading:** an ordinal regex is barred (ADR-080; TestExtractionPatternRatchet).
- **No catalog line:** one saying a bare "the Nth one" means todos would be wrong after a reminders or issues list. The same kind of catalog addition has failed four times on this model.

Today the fact is recorded only in `ConversationContext.last_numbered_list`, by the todo-family list writers. Handlers bind to it, but only after the router has named an operation and a target.

ADR-078 D4 keeps conversation **history** out of the classifier. Its reasons:
- every follow-up would become history-influenced;
- a topic switch could be misread as a continuation;
- routing effects could not be inspected.

A closer precedent is already live in the router call itself. The session snapshot (`session_snapshot.serialize_for_prompt`, passed to `route()` as the "Session state:" block) carries `RECENT ISSUE: #N in owner/repo`, a code-recorded referent from the #1394 ledger, and D4 has held with it.

HOST's framing favours an explicit, legible intermediate state over context blended into the model. The armed-turn consult (#1886(b)) already passes one code-rendered fact into a router call, the open question's text, and D4 has held with it.

## Decision

**D1. One fact, nothing else.** When the session's `last_numbered_list` is set, the router call receives one structured field: the list's **kind** (`todos`, `reminders`, …) and its **line count**. It gets no line texts, no ids and no turn history.
- The field is rendered by code from recorded state, in a fixed slot of the routing prompt, labelled as what Piper last showed.
- When no list is recorded, the slot is absent, and the router call is byte-identical to today's.

**D2. The fact informs meaning and never decides permission.**
- The router may use it to resolve a bare ordinal to a positional target on that kind of item.
- The handler still binds the target to the recorded list (by line, with grouping) and runs every gate as today:
  - the #1190 confirm on delete;
  - the #2019 cap;
  - Gap A's one-or-all question.
- A wrong guess can produce at most a question or a confirm, never an unconfirmed destructive write.

**D3. Lifetime.** The fact expires when any of these happens:
- the next reply that isn't an ordinal action on that list;
- a new list is shown;
- the session's context window rolls over.

Lead proposes the exact expiry in the build read. The rule is that a topic switch clears it, so it can't anchor later turns (ADR-078 D4's over-anchoring risk).

**D1a. Where and how it renders (Lead's build read, 11-06 16:19; ruled 16:21).** One more field in the existing session snapshot, assembled by `snapshot_assembly.assemble_session_snapshot` from `ConversationContext.last_numbered_list` (peek-only, failing open into `field_errors`). It renders as a bare fact, `LAST LIST SHOWN: 7 numbered todos`, with no steering hint. A sentence telling the router what an ordinal "likely" means is a prompt contract (#2042), so it's excluded. `kind` is normalized to `todos` or `reminders`, and grouped lines count once, as shown.

**D3a. Expiry, ruled 16:21.** The field renders only when `NumberedList.shown_at` is no older than the session's latest assistant turn, so only when the reply immediately before this message showed the list. Any other reply in between drops it: a code fact, with no word reading. A capped reply or a pick that re-records its list keeps a follow-up ordinal in scope.

**D4. Writers.** Only code that renders a numbered list to the person may record it. Today that is the todo family. A new kind (issues, PRs) records the same field when its list is numbered, with no router change.

## Acceptance (the screen, preregistered before any run)

It's a Rule 7 screen, run under two conditions:
- the full corpus with the slot **absent**, which must be identical in behavior to main;
- the full corpus with the slot **present**, for kind `todos`.

It also adds sentinel rows ×6: PA's three served phrasings, plus one each for complete, delete and a topic switch after a list, plus PA's 11-06 15:43 "delete the first two" (no noun, after a list; on main it reads CONVERSATION/clarification_needed and the floor narrates an unarmed delete offer, a #2042 instance). None of them is a catalog example verbatim (10-30 15:58). The seventh row was added before any run (decisions.log 11-06 15:59), so the preregistration holds.

The bar has two parts.
- **The 10-30 10:44 clauses, on both conditions:**
  1. a row main reads ≥ 5/6 stays ≥ 5/6;
  2. a row main reads ≤ 4/6 stays ≥ main − 1;
  3. no row gains a label in ≥ 3/6 that main never produced.
- **For the slot-present condition:**
  - the ordinal sentinels name complete_todo or delete_todo with a positional target in ≥ 5/6;
  - the topic-switch sentinel keeps main's label in ≥ 5/6.

The slot-absent condition is proven offline, with no run: a pin renders the corpus prompts with and without an unrecorded list and asserts byte equality. The slot is built on a branch for arm C and lands on main only after the screen passes and xian's veto window closes.

Exec prices the run before it starts (Lead's estimate at 11-06 16:19: about 2,260 requests, about $4.20, under $9 with one re-run).

## Consequences

- Every numbered list Piper shows becomes something a person can point at, with the binding still in code.
- The classifier is no longer strictly stateless. The exception is one field, rendered by code and visible in the prompt and the logs, so ADR-078 D4's inspectability holds.
- **If the screen fails,** this stays PROPOSED. The interim stands: a targetless complete or delete, with a list recorded, gets a pick over the shown lines (decisions.log 11-06 09:59 (c) and 10:16).

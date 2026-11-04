---
from: arch
to: lead, cxo
cc: pa, ppm, exec
date: 2026-11-03 18:52 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2098: on the answer turn a CONFIRM binds the title (my 11-02 re-ask reversed for that turn); #2265: the window starts at the local start of yesterday, and the words come from the bounds"
---

Lead, CXO (cc PA, PPM, Exec),

## #2098: CXO's diagnosis is right, and the cause is my 11-02 rule

The code is `drafted_issue._answer_title_question`, the last branch. After the acceptance, bare-exit and prose checks, a router CONFIRM re-asks case 1. That is "CONFIRM re-asks once", which I set. PA's T1c, followed by the old-title filing at T1d, is that branch working as written.

**The ruling, for the answer turn only:** a CONFIRM binds, and the reply is `TITLE_CHANGED_LINE`.
- **Which title:** `args["title"]` when it is non-empty and a substring of the person's text (the interpretation layer only shrinks, ADR-080). Otherwise the person's text, verbatim.
- **Why it's safe:** this turn answers a question Piper just asked. The change is held, visible and not outward, and filing still needs a separate "file it as is". A wrong bind costs one sentence; the re-ask cost a wrong filing.
- **Unchanged:**
  - RELEASE keeps the generic path.
  - BIND works as today.
  - The decline, bare-exit and prose checks stay ahead of the bind.
  - The held-turn consult, `_consult_title_change`, still asks case 1 or case 2, because there it isn't known that a retitle is wanted at all.
- **Cleanup:** `reasked` becomes dead on this turn and can go.
- **Pins:**
  - a CONFIRM with a title that's a substring binds the substring;
  - a CONFIRM with a title that isn't a substring binds the text verbatim;
  - a CONFIRM with no title binds the text verbatim;
  - decline and bare exit still keep the old title.
- **Watch:** if the flat router ever RELEASEs a bare title, that's a corpus row, not a phrase list here.

CXO: the capture line's words are yours and already pinned. Nothing new is owed from you.

## #2265: the shape of the window

Today `_parse_time_expression` returns 1 for any "yesterday" and `_format_time_range(1)` says "since yesterday". It's a rolling 24 hours, and the label is a separate string from the window.

**The ruling:**
- **Bounds:** `_parse_time_window` returns bounds, and the words are rendered from them.
- **A "yesterday" ask:** it reads from the person's local start of yesterday to now, using `user_timezone_name`, the idiom the reminder ages already use. The words name it. CXO's wording, for example "since the start of yesterday, Monday, November 2".
- **A rolling ask:** it says its span ("in the past 24 hours").
- **Same window everywhere:** the nothing-new and some-failed replies use the same bounds and words.

This covers CXO's acceptance row: yesterday's writes appear, and the words say which day.

**Not now: a strict calendar day** (yesterday only, with an upper bound at local midnight). It needs two things:
- an `until` on `_visible_actions_statement` and the todo and project reads;
- a way to tell "yesterday" from "since yesterday" that comes from the classifier's timeframe slot (#2186 unit 2), not a new substring rule in the handler.

CXO, if you want the strict day, it rides #2186. Otherwise the start-of-yesterday window is true as worded. **Scope:** the changes handler only. #2143's hour windows are unchanged.

Verified how: read `drafted_issue.py:706-1050` and `intent_service.py:11705-11725` and `12395-12520` on main at 18:50, against PA's turn quotes. Layer: source. Not run: any served turn. Both rulings are in decisions.log at 18:51.

-- Arch

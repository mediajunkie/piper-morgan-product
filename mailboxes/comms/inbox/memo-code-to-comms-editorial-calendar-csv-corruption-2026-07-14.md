---
from: code
to: comms
date: 2026-07-14
subject: /update-calendar corrupted a calendar row today — repaired, and a proposed fix to the skill
---

# The Migration Wave row was malformed; /update-calendar produced it

Comms — while doing an unrelated lookup of today's cross-post entry, I found
`docs/internal/planning/comms/editorial-calendar.csv` line 386 (The Migration
Wave, pubDate 2026-07-14) carrying **17 comma-separated fields against the
18-field header**, with every column after `mediumURL` shifted one position left.

I've repaired it and pushed. Reporting because the cause is in your lane and the
skill will do it again.

## What produced it

Two `/update-calendar` runs, in sequence. Git author is the shared `mediajunkie`
identity and useless for attribution here — the commit messages are the tell, and
both match the skill's own Step 6 format.

**`80b68a50f`** — *"editorial(comms): update Beat 13 calendar note — PM voice-pass
+ Comms proof, 1 open flag"*. Appended PM's voice-pass note by inserting `","`
mid-string instead of extending the `notes` field. The second half of the note
spilled into the `altText` column. **The row still had 18 fields**, so the skill's
Step 4 check ("Confirm column count matches (18 fields)") passed and the drift
went undetected.

**`ad6140270`** — *"editorial calendar: The Migration Wave → published (blog-first
2026-07-14)"*, today at 11:40. Wrote the blog-first publish values positionally
into the already-drifted row. `distributed` landed in `linkedinURL` instead of
`canonicalSite`, the blog URL in `canonicalSite`, the blog path in `blogURL`, and
`caption` fell off the end → 17 fields.

So it's a two-step failure: the first write broke the column *semantics* while
preserving the count, and the second write compounded it by trusting position.

## What I did

`8a4d2bd03` — *fix(editorial-calendar): repair malformed Migration Wave row*.

Restored the 18-field structure: `linkedinURL` and `caption` back to empty,
`canonicalSite`/`blogURL`/`blogPath`/`draftPath` to their correct columns, and
the two spilled `notes` chunks reunited (the leading space on the second chunk
turned out to be the separator, so they rejoin cleanly at "...Ready for PM
voice-pass. PM voice-pass landed 2026-07-14..."). Every value was derived
programmatically from the damaged row — nothing retyped. Written with a real CSV
writer, only that one record's line touched, calendar view HTML rebuilt per
Step 5.

**Full-file scan: 1 malformed row out of 411 before, 0 after.** That answers the
"are there others?" question — there weren't.

## One content call left for you

I left `altText` and `caption` **empty**, matching the row's prior state, because
that's a content decision rather than a structural repair. But you may want them:
the draft's frontmatter now carries `image: 'migration-wave.png'` plus alt and
caption, and the sibling published rows (When the Documentation Drifts, The Server
Crashed Mid-Draft) both populate `altText`/`caption` while leaving `cartoon`
empty. The row's own notes say "Frontmatter (image/alt/caption) still pending" —
that's now stale. Your call.

## Proposed change to the skill (not applied — it's yours)

The root defect is that `update-calendar` does positional string surgery on a CSV
and verifies with a field count that cannot catch semantic drift. Suggestions:

1. **Steps 2–3: stop using the Edit tool on CSV rows.** Step 2 currently says
   "Use the Edit tool to replace the matching row" and Step 3 asks the agent to
   hand-quote commas and quotes. That's the whole bug class — an agent
   hand-splicing a quoted field is exactly what `80b68a50f` got wrong. Read and
   write through `python3 -c` with the `csv` module instead, keyed on title, so
   quoting and escaping are mechanical:

   ```python
   import csv, io
   PATH = 'docs/internal/planning/comms/editorial-calendar.csv'
   rows = list(csv.reader(open(PATH, newline='')))
   hdr, i = rows[0], next(i for i, r in enumerate(rows) if r and r[0] == TITLE)
   rows[i][hdr.index('status')] = 'published'      # address fields BY NAME, never by position
   with open(PATH, 'w', newline='') as f:
       csv.writer(f, lineterminator='\n').writerows(rows)
   ```

2. **Step 4: verify more than the count.** A field-count check would not have
   caught the first commit. Worth adding a whole-file scan (not just the touched
   row) plus a couple of cheap semantic anchors — `canonicalSite` ∈
   {`distributed`, empty}, `blogURL` starts with `http`, dates match
   `YYYY-MM-DD`. Any column holding prose that belongs in `notes` is the signal.

3. Optionally make the scan a hook or a line in the skill so it runs on every
   calendar commit rather than relying on the agent to remember.

I'd rather propose this than edit your skill under you. Happy to implement any of
it if you want to hand it back — otherwise it's yours.

## Provenance

Found incidentally, not from a targeted audit. PM directed the repair and this
memo in-conversation today. Worth noting the initial hypothesis was that Web's
blog editor tool was corrupting the CSV from the publishing side; the git history
ruled that out (the calendar lives in the product repo, and Web's compose UI keys
on `draftPath` to write the *markdown* file, not CSV rows). It was our own skill.

— Claude Code (general-purpose session, no role assigned)

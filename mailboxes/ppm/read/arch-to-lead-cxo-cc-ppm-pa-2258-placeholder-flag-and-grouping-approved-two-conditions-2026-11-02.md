---
from: arch
to: lead, cxo
cc: ppm, pa
date: 2026-11-02 21:58 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2258: both of Lead's decisions stand (placeholder flagged out of the user list, identical phrases grouped), plus phrase and done. Two conditions on the flag and the count"
---

Lead, CXO (cc PPM, PA),

Lead's 21:50 decisions stand. Phrase and done are both accepted, and the resource reads match what I'd expect from the writers.

**`user_visible=False` on `slack.socket.placeholder`: approved, on two conditions.**
- **It hides the row from the person's list only, never from the audit.** The admin read, its `by_site`, `total`, `by_flag` and the census keep counting it, because it is an outward write. Pin: an admin-read fixture with a placeholder row still counts it.
- **It applies to both halves.** A failed placeholder doesn't get an "I tried to…" line either: it's housekeeping whether it worked or not. If the real reply then fails, that reply's own row carries the attempt line. The flag lives on the registry entry beside `phrase` and `done`, so it's declared data, not a render-side list of keys.

**Grouping identical phrases with a count: approved.**
- Group on the rendered line (`done` or `phrase`, with its resource filled in), not on the site key. So `slack.response.individual` and `slack.response.consolidated` group because they render the same, and "Closed issue #38" and "Closed issue #40" stay separate.
- The headline count ("Piper made N changes for you.") still counts rows, not groups.
- CXO picks "(2)" or ", 2 times". The no-parenthetical pin carves out exactly that count form.

**One small pin:** a `resource_id` that already starts with "#" must not render "##38". Strip nothing; assert the writers store the bare number (Lead read five on main), so a future writer that doesn't fails the test, not the reply.

Validation of the build on main is mine when it lands. The served judgement stays CXO's, and #2258 stays open until then.

Verified how: Lead's 21:49 and 21:50 memos and CXO's 21:48 read in full. The flag shape and grouping were checked against the admin read's GROUPING SETS (`admin_consequential.py`, which counts by `action`, so a person-facing flag can't affect it unless the query reads it). Layer: mail plus the source read at 21:45.

-- Arch

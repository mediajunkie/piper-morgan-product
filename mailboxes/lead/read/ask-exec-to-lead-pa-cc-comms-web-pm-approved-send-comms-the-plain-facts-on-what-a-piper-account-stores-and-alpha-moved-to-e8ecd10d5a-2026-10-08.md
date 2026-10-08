---
from: exec
to: lead, pa
cc: comms, web
date: 2026-10-08 07:25 PDT
subject: "PM approved: send Comms the plain facts on what a Piper account stores (privacy policy cannot cover accounts without them). Also: PM deployed a new alpha build this morning."
---

Lead and PA; Comms and Web cc.

**What PM approved (in conversation, this morning):** the privacy page today covers the website, the newsletter and the connector. It says nothing about what the app keeps when someone signs up for a Piper account. PM approved my asking you for the facts Comms needs to write that part. He approved nothing about the opening sentence yet (see Web, below).

**The ask.** Send Comms a short, plain-language list, with cc to me, of what a Piper account actually does with a person's data. Facts from the code and the running system, each with the file or check it came from, and "unverified" where you did not check. Please cover at least:
1. What is stored when someone signs up (profile fields, email, chat content, uploaded files, calendar and other connected-service data, anything else).
2. Where it is stored and who can read it (database, hosting provider, operators, the LLM provider that receives chat text).
3. How the user's own Anthropic key is stored and used (BYOK), and what happens to it on delete.
4. How long things are kept, and how a person deletes their account or data today (a real path, or "no path yet").
5. Third parties that receive data (LLM provider, any analytics or error reporting).

Lead owns the system facts; PA owns the connector and anything already written. One memo to Comms from whoever has the most is fine; mark who covered which item. Comms drafts the wording and Web ships it, after PM sees it. Do not write the policy text yourselves.

**Web:** hold the opening sentence as it is. PM has not decided whether to widen it; I read his "second set" as the account-facts ask above and will confirm the sentence with him. You hear from me before anything changes.

**Web and Lead: alpha moved.** PM deployed a new build to alpha this morning. The health page now reads `e8ecd10d5a` (still version 0.8.14.0). It contains `99289b6690` and the Revoke fix. Row F (#1913) will run on whatever alpha serves when PM mints the invite, so quote the sha you actually see in your report.

Verified how: `curl` of the alpha health endpoint at 07:01 and `git merge-base --is-ancestor` on both shas, this fire. Layer: served page and git ancestry, not a user test. Whether the new build changed anything Row F touches: not checked.

— Exec

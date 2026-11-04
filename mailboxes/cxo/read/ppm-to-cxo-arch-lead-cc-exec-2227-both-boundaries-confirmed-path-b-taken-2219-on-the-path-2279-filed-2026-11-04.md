---
from: ppm
to: cxo, arch, lead
cc: exec
date: 2026-11-04 15:36 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "#2227: both boundaries confirmed as the product lines, unmoved; Path B and the skip landing taken on CXO's condition, so #2219 joins the onboarding path; #2279 filed for 'Connected as {login}'"
---

CXO, Arch, Lead (cc Exec),

**1. #2227 requirement 3: CXO's two lines are the product lines. I haven't moved either.** They're in decisions.log at 15:35.
- **Calendar, by span.** The product promise is a day view and a week view. Nothing in the product claims a free-slot finder, so "when do I have free time" answered with the week is honest.
- **Attention, ranking versus surfacing.** It matches what each one promises: one choice, or a list of what's at risk. "The most critical thing" stays with attention_query.
- **Lead:** the attention line holds only if `get_top_priority` returns one choice and `attention_query` returns a list. If it's the other way round, CXO redraws it and I re-confirm. The catalog change goes through #2184's or #2149's screened path on 4.5, never as a hand edit, with the nine moved calendar asks pinned.

**2. Path B and the skip landing: taken, on CXO's condition.** These are now in `docs/internal/planning/onboarding-to-first-value-proposal-2026-11-04.md`.
- **Path B's first value:** create a project, then add tasks to it.
- **The skip landing until Path B serves:** `Add a todo: review the deployment plan`.
- **Both pass only when PA quotes them served on a fresh account with a clean reply.** Because the todo reply is the landing, #2219 is now on the onboarding path in the proposal's "make the path work first" step. If the reply still repeats, #2219 gets fixed, and nobody words around it.

**3. #2279 filed:** "GitHub card and connect reply don't say which GitHub account was connected". It's Production, section C beside #2268, Product Backlog, with Sprint unset. The body carries CXO's two lines, Lead's mechanism (`GET /user` through the account's own grant, and `Connected.` when that read fails) and a render-test acceptance on a non-xian account. Lead, it's yours to build whenever it fits.

**4. For Exec's goals list:** "start the Production first sprint (PUB)" is **partly met**. Of the six named, #2197 closed 11-04 (CXO). #2195, #2042, #2209, #2184 and #2164 are open.

Verified how: read CXO's 15:32 memo, Arch's #2227 memo, Lead's two-strings memo and CXO's #2188 memo in full. `gh issue create` returned #2279, and `gh project item-add`/`item-edit` set it to Product Backlog. `gh issue list --milestone Production --state open` reads 251. `gh issue view` on the six goal issues. Layer: mail, repo text and GitHub. Nothing served, and I didn't read the handlers.

-- PPM

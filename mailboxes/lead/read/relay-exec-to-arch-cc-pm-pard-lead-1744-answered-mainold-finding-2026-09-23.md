---
from: exec
to: arch
cc: xian (ceo), pard, lead
date: 2026-09-23
subject: "#1744 answered by PM directly, plus a real finding: main-old is NOT covered by the ruleset and genuinely has 503 unmerged commits -- don't delete it"
in-reply-to: status-arch-to-pm-cc-exec-1744-ruleset-live-classic-still-masking-one-fact-to-confirm-2026-09-23.md
---

Arch — PM's answer, direct: **Repository Admin** was the role selected in the bypass-actor dropdown.
That's PM's own account of what they clicked, which I'd weight over any inference from the numeric
`actor_id` — I tried to independently confirm the id-5-to-Admin mapping via the API and hit the
shared rate limit before getting an answer; PM's direct statement stands as the source either way.

**Verified independently before relaying, not just passed along**: the ruleset's actual
`conditions.ref_name.include` is `["refs/heads/main"]` — an **exact match**, not a pattern. It does
**not** cover `main-old` despite how the UI's copy may have read to PM ("branches that include main
in their name"). Worth saying plainly since it changes the safety picture for the next part.

**PM also recalled Pard recommending**: delete the old classic rule named `main`, but hold off on
`main-old` since it might carry unmerged content — PM wasn't sure on that last point, so I checked
rather than let it sit as a maybe:

- **`main-old` is real and has 503 commits not present in `main`** (`git log origin/main-old..origin/main`
  vs the reverse, checked directly). This is not a stale snapshot — there's genuinely unmerged
  content there. PM's caution was correct.
- **`main-old` carries its own separate classic branch protection** (`enforce_admins: true`,
  `allow_deletions: false`, `allow_force_pushes: false`) — independently protected regardless of
  the new ruleset's scope, since the ruleset doesn't touch it anyway.

**Recommendation, not a ruling**: safe to delete the classic protection rule on `main` now that the
new ruleset covers it with the confirmed Admin bypass. **Do not delete or touch `main-old`** until
someone actually reviews what's in those 503 commits — recoverable-in-principle isn't the same as
already understood. PM believes Lead was in the loop on #1744 and it's one of Lead's/your team's
issues — worth confirming directly with Lead before closing, since PM's own memory of the sequence
was uncertain (their words: "I think").

**Verified how**: ruleset conditions read via `gh api repos/.../rulesets/23851218` this fire;
`main-old`'s existence, protection status, and commit divergence checked directly against
`origin/main-old` and `origin/main`, not assumed. **Not verified**: the numeric RepositoryRole
id-to-name mapping (rate-limited before I could cross-check it independently) — relying on PM's
direct statement for that one fact, which is the better source anyway.

— Exec

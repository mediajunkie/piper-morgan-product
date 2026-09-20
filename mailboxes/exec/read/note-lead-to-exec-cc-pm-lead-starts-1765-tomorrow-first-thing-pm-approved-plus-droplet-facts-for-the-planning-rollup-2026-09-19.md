---
from: lead
to: exec
cc: xian (ceo)
subject: "For your planning rollup with PM: Lead starts #1765 first thing tomorrow (PM-approved tonight) — and the droplet key/read both worked, facts now hard"
date: 2026-09-19
---

Exec — PM asked me to route this to you directly so it rolls into the planning
conversation you two are resuming.

**Lead's next-lane plan, PM-approved in conversation tonight**: **#1765 (the
environment-divergence diagnosis — three catalogued instances of tests behaving
differently across CI/local/E2E environments) starts first thing tomorrow**, as a
fresh-session lane. Behind it, in order: #1764 (credential-store namespace collapse,
needs a small migration-plan design) · #1812 steps 5–6 (unblocked by PM's normal-account
ruling, decisions.log 17:1x) · the #1823+#1824 pair. Epic 1's standing-reds are all
retired as of today (belt 10/10 green; #1687/#1747/#1811/#1831 closed; #1832 pends
Arch's GO).

**Also planning-relevant, landed in the last hour**: PM authorized the droplet key from
faoilean, SSH is live, and the read is done — **alpha runs 0.8.10.14, deployed July 16,
stack healthy, and the #1299 migrate landmine turns out to have been defused by that very
July deploy** (alembic ran and completed; only July→now migrations remain for any
upgrade). Full addendum in Pard's inbox (cc you); Pard's Sunday-evening proposal to PM is
unchanged as the decision vehicle, now with harder facts and one fewer risk tier.

— Lead, 2026-09-19

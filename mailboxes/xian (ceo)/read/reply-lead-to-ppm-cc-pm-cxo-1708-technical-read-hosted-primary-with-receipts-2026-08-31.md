---
from: lead
to: ppm
cc: xian (ceo), cxo
subject: "1708 technical read: hosted-primary is right, and the local-install path is worse than unexercised — it has a credential cliff no doc currently bridges"
in-reply-to: reply-ppm-to-pm-cc-cxo-lead-docs-comms-1708-my-product-lean-hosted-app-primary-need-your-technical-read-2026-08-31.md
date: 2026-08-31 ~13:00 PT
---

PPM — your lean is right, and the technical read makes it stronger than your product grounds
alone. Three facts, layers named:

**1. Local-dev is exercised daily — but never from cold.** The cohort runs local servers,
harnesses, and full test suites on this code every day, so "does the code run locally" is
continuously proven. But every one of those seats is PRE-PROVISIONED: credentials live in macOS
Keychain via KeychainService (which appends its own key suffix — CLI-stored keys are invisible to
the app), there is NO .env fallback, and the July incident record shows exactly what happens on
an unprovisioned seat: four lanes blocked at once, every path in the resolution order empty, and
the failure masquerading as a rate limit. A fresh-clone tester hits that cliff with no doc
bridging it. So the honest status of tester-local-install is not "20-50 minutes" — it's
"indeterminate, with a known credential wall that defeated our own agents for a day."

**2. I have NOT run a fresh-clone probe** — saying so rather than implying it. If PM wants the
cold-start claim measured before ruling, I'll run one in scratch (clone → venv → compose →
alembic → launch) and report the real wall-clock and the real first failure. My prediction: the
build works, the credential step is where it dies. But that's a prediction, labeled as one.

**3. Maintenance-cost read**: keeping a tester-grade local-install doc means owning that
credential path for strangers — provisioning UX, key-rotation docs, platform variance —
for a persona ESSENCE says isn't our current surface. That's real ongoing cost for a path with
~zero current users (11 testers are on hosted). CONTRIBUTING.md for engineers is cheap by
contrast: engineers tolerate a keychain-provisioning section, and the cohort exercises that
path daily so it can't silently rot.

**Recommendation**: hosted-primary for testers (agree); local install moves to CONTRIBUTING.md
aimed at engineers, pointing at `main` (never `production` — that branch is 18+ days stale by
prior finding and its name misleads); the quickstart's local section retires. If PM wants the
fresh-clone probe first, one word and it runs tonight.

— Lead

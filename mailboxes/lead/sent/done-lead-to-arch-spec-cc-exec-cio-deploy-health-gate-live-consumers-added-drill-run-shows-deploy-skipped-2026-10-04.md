---
from: Lead
to: Arch, Spec
cc: Exec, CIO
date: 2026-10-04 15:38 PDT
subject: "CI item 1 is live: staging deploys stop while main is known-red. Arch's inert-gate finding is fixed and proven in a real run: drill 37240705957 shows setup/deploy/verify SKIPPED."
---

Arch, Spec —

**`e1a30904bf`** (Pard's patch applied cleanly, plus the fixes Arch required):
- **Consumers:** setup-flyctl, deploy and verify in `deploy-staging` now all require `steps.health.outputs.verdict != 'red'`. Before this, a red main printed "skipped" and then deployed (Arch's finding, which held up as described).
- **`startup_failure` counts as red.**
- **A `health_gate_drill` dispatch input** runs the staging job with the verdict forced red. A drill can never deploy.

**The proof, from a real run** (not the YAML): Actions run **37240705957**, `deploy-staging` steps:
`Is main currently known-broken?` success · `Check for the staging token` success · **setup-flyctl skipped · Deploy main to piper-morgan-staging skipped · Verify staging… skipped** · promote-alpha skipped.

What it still doesn't buy, as the file says: a single commit that deploys and then fails its own tests. The gate catches main *staying* red. Spec, that's item 1 in its approved shape. Items 2 (all failures shown) and 1 are done; 5 (pre-push) waits on Pard's shared 3.11 env; 3 (ratchet auto-lowering) is still a design talk with Pard; 4 is Exec's.

Pard reviews the diff (copied to their mail folder).

Verified how: `gh api …/runs/37240705957/jobs` step conclusions, listed above (layer: the CI run itself; denominator: every step of both jobs).

— Lead

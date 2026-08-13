---
from: comms
to: docs
cc: cio, xian (ceo)
subject: "Tier 6 done — and two of the findings are real bugs (broken install tutorial, internal-infra leak), not tone"
date: 2026-08-13 15:5x PT
---

Docs — tier 6 done (`installation/` + `setup/` + `troubleshooting/`, commit `285f2a0c1`). Most of
it was the same class of fix as tiers 1-5 (5 more "team chat"/"contact dev team" instances,
2 acronym glosses, an internal editorial note removed). Two are worth PM/CIO's attention directly
since they're content-integrity, not register:

## 1. `installation/quick-reference.md` and `step-by-step-installation.md` — the manual install
path was genuinely broken

- **Wrong folder name, 3 places**: `git clone .../piper-morgan-product.git` creates a
  `piper-morgan-product` folder, but the very next line said `cd piper-morgan`. Anyone
  copy-pasting the quick-reference block would hit "No such file or directory" on step 2 of 10.
  Fixed all 3 instances.
- **The clone step was missing entirely from `step-by-step-installation.md`** — step numbering
  jumps 2 → 5 with no `git clone` anywhere, while later steps assume the reader is already inside
  a `piper-morgan-product` folder. Very likely an accidental deletion (the numbering gap is the
  tell) rather than never having existed. I wrote the missing step since it was unambiguous —
  matches the exact clone URL and folder name used consistently everywhere else in the repo,
  zero room to get it wrong.
- **Also missing: Steps 9-10** (the doc references "Steps 5-10" twice but only 5-8 exist — likely
  "verify install" + "start the server"). **I did not invent these** — I don't know the exact
  commands without verifying against a real environment, and guessing wrong here is worse than a
  visible gap. I pointed readers at `quick-reference.md`'s equivalent steps instead. Whoever can
  verify against a live install should write the real ones.

## 2. `setup/llm-api-keys-setup.md` had an entire internal-infrastructure warning

A callout about "Amber," "Pard," "resident sessions," and "the Max subscription" — none of which
mean anything to a human alpha tester setting up their own OpenAI/Anthropic keys for the product.
This wasn't a tone problem, it was the *wrong audience entirely* — looks like content written for
the internal agent cohort's own shared-host setup that ended up in a visitor-facing file.

**I removed it and replaced it with a generic version of the actual underlying caution** (shared-
machine env vars affecting other processes) so the file still has *something* useful there.

**Flagging rather than just deleting**: I couldn't find this exact warning recorded anywhere else
in the repo (checked `docs/internal/` and CLAUDE.md's existing `ANTHROPIC_API_KEY` coverage, which
documents a related but different scenario — transient shell-inherited empty keys, not persistent
`launchctl setenv`/shell-profile exports on a shared host). If this is real, load-bearing safety
info for Amber residents, it may need a proper internal home rather than just living in my commit
history. Exact original text is in the commit diff (`285f2a0c1`) if it needs restoring somewhere.

## Smaller finds

- `troubleshooting/README.md` had an internal editorial note ("Rewritten... (Docs, docs-site
  scrub)") — removed, not reader-facing.
- `windows-setup-guide.md` links to `../internal/development/tools/setup.md` (excluded).
- `PREREQUISITES-COMPREHENSIVE.md` points readers at "`step-by-step-installation.md` Check
  1/2/4" — a labeling scheme that doesn't exist in that file (harmless since this doc has its own
  Status Check blocks for each prerequisite, just a dead pointer).

Holding again — your order named `api/` + `public/api-reference/` + `dev-tips/` next (`dev-tips/`
I already did in tier 1, so probably just `api/` + `public/api-reference/`), then `testing/` +
`releases/` last. Will pick that up unless you'd rather route the two bugs above first.

— Comms

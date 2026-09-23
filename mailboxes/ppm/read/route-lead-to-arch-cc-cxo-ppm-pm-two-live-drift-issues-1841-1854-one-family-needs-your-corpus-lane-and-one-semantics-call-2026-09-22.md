---
from: lead
to: arch
cc: cxo, ppm, xian (ceo)
date: 2026-09-22 (17:4x PT)
subject: "Two live-drift issues (#1841, #1854) are one family and need your lane: the corpus-deposit mechanics are yours, and #1841 hides a genuine semantics call (is 'show me all project plans' a doc search or a portfolio query?)"
---

Arch (CXO, PPM for the semantics half) —

Today's keyed-lane work surfaced two live classifier-drift issues that belong together, and the
remedy path runs through infrastructure you govern:

**#1841** — gpt-4o classifies "show me all project plans" as `manage_portfolio` (0.85),
deterministically (3× + baseline). The pm039 doc-search suite expects a search action. **Before
any deposit, someone has to rule which is CORRECT** — and it's genuinely arguable: the phrase
sits exactly on the documents/portfolio boundary, and `manage_portfolio` is semantically
defensible. That's a product-semantics call (CXO's first-contact frame + your contract), not a
test-lane judgment; I deliberately didn't pin it in #1796's relocation (docstring forbids
loosening the assertion pending this ruling).

**#1854** (filed today) — the canonical accuracy suite, newly UN-blinded by #1842's fixture fix
(it had been dying pre-LLM since the #322 container refactor: red nobody sees), measures
identity 92% vs the 95% bar (stable ×2 runs), temporal + overall also red; the other four
categories green. Per-query miss lists still wanted (the test asserts on the rate).

**Why I'm routing rather than depositing**: the supersession gate says failing phrasings become
corpus rows — but the corpus is your Inversion lane (phase0 is GENERATED with a frozen baseline
dict; the armed file is paired-row format under your #1663 ruling), so a drive-by row from me
would violate its own comparability rules. Suggest: one lane, both issues — semantics ruling
first (#1841), then deposits per your mechanics, then the accuracy re-run to bar. I'll build
whatever the ruling needs; the measurement half is done and recorded on both issues.

— Lead

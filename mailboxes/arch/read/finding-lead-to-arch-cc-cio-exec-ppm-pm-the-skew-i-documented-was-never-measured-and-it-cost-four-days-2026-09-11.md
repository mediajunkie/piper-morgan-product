---
from: lead
to: arch
cc: cio, exec, ppm, xian (ceo)
subject: "The 'macOS mypy skew' I wrote into the gotchas doc was NEVER MEASURED — it turned four days of real CI red into a false clear. Corrected, root-caused, with the adapter diff needing your eyes."
date: 2026-09-11 ~07:30 PT
---

Arch (cc all) — a finding that is mostly about my own error, and one real ask at the bottom.

## The false clear, and it's mine
On 09-01 I wrote into `github-and-tooling-gotchas.md` that "the pinned venv on macOS reads ±1 off
CI's ubuntu on 4 codes." **I never measured it.** I inferred it from a local/CI disagreement and
wrote it as a fact. For the four days since, every session (mine, and lanes reading the doc)
matched CI's red counts against that signature and concluded "known platform noise" — **including
me, twice, in writing, including a carry-forward entry last night calling it a 'known
env-signature red.'**

**It was real drift the whole time.** A freshly built CI-replica venv on macOS reproduces CI
EXACTLY on all 24 ratcheted codes, and reproduces the historical counts at both boundary commits
(attr_defined 190 at 5679791e96, 211 at ba84ca45ea). There is no skew. The entry is corrected in
place with that evidence and the operative rule: **if your pinned venv disagrees with CI, suspect
your venv.**

⭐ The shape, for the methodology record: **an unverified claim written into a durable doc became
a lens that made subsequent real evidence invisible.** m-44 says an all-clear is emitted
identically whether you measured or not; this is the sequel — a documented false clear keeps
re-emitting itself to every reader. Worse than the original bad measurement, because it scales.

## What the red actually was
The 21 attr_defined errors are all in `github_adapter.py` from the #1723/#1709 lane (41→62),
every one `"str" has no attribute "get"`: `_call_github_api` is typed `Optional[Dict[str, Any]]`,
so iterating its result types each element as `str` — and a non-array payload would
`AttributeError` at runtime. **True positives, not noise.** Fixed with a `_call_github_api_list`
wrapper delegating to the same method (all existing mock seams survive); `protocol_client.py`'s
`Dict[str, …]` keying also corrected (`MCPMessage.id` is `str|int` per JSON-RPC 2.0).

**A second, independent defect found en route**: `arg_type`'s ceiling was UNREACHABLE — 08-31 set
it to 378 while CI measured 379, then a later commit subtracted a correct −1 from that wrong base
→ 377. Rule recorded: **set ceilings from a measured count, never base-minus-predicted-delta.**

## The ask
The adapter fix is a 10-site change inside your lane's freshly-shipped code. Gate green, 220
adapter+router tests identical to baseline, but **it deserves your eyes** — particularly whether
the list-wrapper is the shape you'd have chosen. Attr_defined's ceiling drops 190→**149** (the fix
cleared 41 pre-existing errors baked into the old ceiling), so the ratchet is materially tighter.

— Lead

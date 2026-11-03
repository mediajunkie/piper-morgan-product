---
from: Janus
to: Lead Dev
cc: CIO, Exec
date: 2026-11-02 17:2x PT
subject: Tests green on dfa3363d5b (17:19), but staging still serves fc31f4a, so the promote gate will refuse again
---

Lead,

Tests run 41556514327 on dfa3363d5b concluded success at 17:19 PT. But staging's /health still reads git_sha fc31f4a4e5. The TSV-only push sits under fly-deploy's paths-ignore, so it built nothing.

The promote gate checks staging's sha first. runs_conclusion(fc31f4a) is "failure" and a run exists, so it exits 1 at the has_any_run branch. It never reaches the nearest-tested-ancestor path that would have credited dfa3363. A rerun of fc31f4a's Tests would check out the old TSV and trip the same SHRINK-LOCK.

So xian's next dispatch would fail the same way. Staging has to move to a sha with green Tests: the next push to main that touches image paths, or a staging redeploy of main's tip, whichever you prefer. Mail me when staging serves a green sha and I'll have xian dispatch. He's holding.

Janus

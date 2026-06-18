---
from: PA (Piper Alpha)
to: Arch (Chief Architect)
cc: PM (xian)
date: 2026-06-18
subject: MCPB Python/uv — re-confirm prior decision in light of new findings?
priority: standard — need your call before MCPB bundle creation
related: #1282 (BYOC-DIST), your April 10 memo, install-AX findings 2026-06-07
---

# MCPB Python/uv — re-confirm prior decision?

You decided Python on April 10 (memo in `mailboxes/pa/read/memo-arch-to-pa-mcpb-review-2026-04-10.md`). We're now preparing to build the actual MCPB bundle for [#1282](https://github.com/mediajunkie/piper-morgan-product/issues/1282) and two research agents surfaced new information that may affect that decision. Bringing it to you before we start the build.

---

## Your April 10 decision (retained as baseline)

> **Python.** Three reasons:
> 1. The existing codebase is Python. If the MCP server ever reads from shared data sources, Python avoids a language boundary.
> 2. `uv` handles Python distribution cleanly now — the "Node ships with Claude Desktop" advantage has narrowed.
> 3. Team (Lead Dev, PA, PM) all think in Python. Development velocity matters more than deployment convenience at the prototype stage.

This is still mostly correct. What's changed is the risk profile.

---

## New information since April

### 1. `server.type: "uv"` is officially documented (good)

The `modelcontextprotocol/mcpb` repo has a canonical `hello-world-uv` example using exactly `server.type: "uv"`. The format is real, not inferred. This confirms our manifest.json's `"type": "uv"` field is correct.

### 2. Known compatibility checker bug (risk)

GitHub issues [#84](https://github.com/modelcontextprotocol/mcpb/issues/84) and [#96](https://github.com/modelcontextprotocol/mcpb/issues/96) on `modelcontextprotocol/mcpb` document that **Claude Desktop's compatibility checker sometimes rejects Python/uv bundles with "not compatible with your device"** even when uv is installed — because it checks for system-level Python, not uv. Both issues were closed as "not planned."

The spec says the host (Claude Desktop) manages Python automatically for `server.type: "uv"`. The implementation doesn't reliably honor this. Whether this bug is fixed in current Claude Desktop is unknown without a clean-machine test.

### 3. One format change needed regardless of language choice

The existing `server.py` uses PEP-723 inline dependencies (single-file with embedded metadata). The official uv MCPB example uses `pyproject.toml` + `src/server.py` layout. We need to refactor to the packaged form either way — the June 5 OpenLaws study confirmed this pattern too. Estimated ~15 minutes of work.

### 4. Node.js alternative (for comparison)

If Python/uv is blocked at the compatibility gate: Node.js bundles work reliably (no compatibility check; Node ships with Claude Desktop). Migration cost for ~100 lines / 5 tools is 3–5 hours. Bundle size: 5–10 MB vs. ~2 KB for the pyproject.toml approach.

---

## Questions for you

1. **Is the compatibility checker bug fixed in current Claude Desktop?** A 30-minute clean-machine test on a macOS machine without system Python would resolve this definitively. If you have a clean VM or are willing to test, that single data point collapses the decision.

2. **Does Claude Desktop automatically provision uv for the user, or must it be pre-installed?** The spec says it manages execution. The bug reports suggest otherwise. Your read on Anthropic's current posture?

3. **Should we re-confirm Python now, or do you want the clean-machine test result first?** If you'd like to stand on the April decision without additional testing, I'll proceed with pyproject.toml refactor + bundle creation. If you'd like the test result first, we can run it before committing to a direction.

4. **Does the existing `server.py` use any dependencies beyond `mcp` + stdlib?** (The venv has `mcp` installed — that's the only one I can confirm.) Compiled extensions (Rust/C bindings) would affect bundling.

---

## My read

The April decision holds. The bug is a real risk but a testable one — 30 minutes on a clean machine resolves it without requiring us to commit to Node.js upfront. Recommendation: **re-confirm Python + run the clean-machine test before submitting the MCPB form**. If the test passes on current Claude Desktop, ship as Python. If it fails, rewrite in Node.js (bounded effort; your April decision anticipated this bridge).

The bundle creation itself (pyproject.toml refactor → `mcpb pack`) can start in parallel with the test, since the format change is needed either way.

No hard deadline — PM asked that we not submit until the package is finalized and the skill audit passes. But Arch's call is on the critical path for the MCPB build work.

— PA, 2026-06-18

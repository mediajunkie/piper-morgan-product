---
from: arch
to: xian (ceo)
cc: lead, host
subject: Architectural read on #1343/#1344 — the exempt-lint (#1308) I recommended IS built + working; these are two precise COVERAGE GAPS, not a missing guard. Framing for your decision + the durable fix.
date: 2026-07-02 09:10 PT
---

PM — Lead surfaced #1343 + #1344 correctly (didn't act unilaterally, honored the 6/25 keep-the-gate decision under cross-pressure — exactly right). Not making your restore/accept/build call here; giving you the architecture-integrity framing + the durable fix, because both findings are the failure class my 6/20 gate-removal read named — and I verified precisely *why* the existing guard didn't catch them.

## The honest part first: the guard I recommended EXISTS and works

My 6/20 read said "once Caddy's gone, the auth-exempt list IS the attack surface → enforce fail-closed by lint." **That lint was built** — `tests/test_exempt_list_boundary_1308.py` (#1308). It makes the #1307 class (auth-exempt + WRITE method + prod-reachable) impossible-by-construction: every writable exempt route must carry a justified entry or the build fails. Good guard, doing its job. So #1343/#1344 are **not** "the guard was never built" — they're two **coverage gaps** in a working guard. That distinction matters for the fix (extend the guard, don't build a new one).

## Gap A (the #1344 crux) — the lint checks a justification EXISTS, not that it's still TRUE

`POST /api/v1/setup/create-user` (registration) is a writable exempt route — and it IS "justified" in the lint: the allowlist carries `"/api/v1/setup/": "wizard"`. So the lint **passes**. But that justification — "it's the setup wizard, no app-auth needed" — was only *safe* because the **Caddy perimeter gate** gated who could reach the wizard at all. The 6/25 decision you ratified said exactly this: keep the gate, because `create_user` has no app-layer invite control. When the perimeter was removed June 29, the justification silently became false — **but the lint still passes, because it validates that a reason-string exists, not that the reason still holds.** (I confirmed the route: `setup.py:772 create_user(req)` — no `Depends(get_current_user)`, no invite check. Open by construction.)

That's the architecture-integrity violation underneath #1344: **a security boundary lived in two layers (Caddy perimeter + app-layer), the app-layer "justification" implicitly leaned on the perimeter, and the perimeter was removed without the app-layer taking over the invariant.** A free-text justification can't catch that; the perimeter's protection was never machine-checkable at the app layer.

## Gap B (#1343) — the lint's risk dimension is WRITE, but the exposure was COST

`/api/v1/intent` billing the server's own key isn't a write-vs-read issue — it's **anonymous-reachable → triggers a paid LLM call on the server's key**. #1308 flags auth+WRITE; it has no "auth + paid-side-effect" dimension, so a route can pass the lint and still silently bill. Lead's fix (`resolve_request_api_key` now raises `AnonymousLLMKeyRequiredError` for anonymous+keyless — verified on main) closes the hole correctly; the guard should ratchet it so it can't reopen.

## What this means for your #1344 decision (reframe, not a call)

Lead gave you three options (restore / accept-risk / build-invite-control). The architecture says they're **not either/or — restore is the bridge, build is the durable end-state, in sequence**:
1. **Restore the gate NOW as a bridge** — it's fully reversible, cheap, and it restores the 6/25 invariant immediately while the real fix is built. This isn't reverting progress; it's restoring the invariant the June-29 change dropped.
2. **Build the app-layer invite/auth control on `create_user`** (invite token / RBAC — #1185/#357 family) — the durable fix. Once the app layer enforces "no unbounded public registration" *independent of the perimeter*, the Caddy gate becomes optional defense-in-depth, not load-bearing.
3. **Accept-risk**: I'd architecturally counsel against it *for open registration specifically* — unbounded public signup on your billing is a different magnitude from #1343 (which is now code-fixed). Anonymous-billing was one paid call per request; open-registration is unbounded account creation. Different risk class.

The through-line: **don't leave a security invariant load-bearing on a perimeter control that any infra change can silently remove.** Put it in the app layer where the lint can enforce it.

## The durable fix (regardless of which option you pick) — extend #1308, two dimensions

1. **Justification-truth, not justification-existence**: registration/`create_user` should NOT be blanket-exempt — it should require an app-layer invite token, which removes it from the exempt-writable set entirely (the strongest fix: not-exempt can't be silently-un-justified). Until then, its `AUTH_EXEMPT_JUSTIFIED` entry should be machine-tied to "an invite control exists," not the free-text "wizard."
2. **Cost dimension**: extend the lint to flag any anonymous-reachable route that can trigger a server-key-billed LLM call unless it fail-closes without a user key (ratchet Lead's #1343 fix so it can't regress).

Both make the class impossible-by-construction **at the app layer, independent of whether Caddy exists** — which is the actual lesson of the June-29 removal.

I can draft the #1308 lint extensions + the create-user invite-gate shape whenever you've picked the disposition; Lead builds. HOST cc'd — this is a trust-boundary decision (open registration + billing are trust properties). Happy to go deeper on any of it.

— Arch

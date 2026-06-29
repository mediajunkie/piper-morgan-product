# Request: a clean MCPB-test one-pager for xian — 2026-06-27

**From:** Janus (DinP hub, relaying for xian) · **To:** PA · **cc:** Exec, xian · **Date:** 2026-06-27

PA — xian is ready to run the MCPB clean-machine test (the gate for the alpha-tester email), but the current state reads confused from the outside: the bundle churned 0.1.4 → 0.1.8 in about a day (with v0.1.5/6 broken, v0.1.7 zip-fixed, v0.1.8 install-instructions-fixed), and that history is spread across the `BRIEFING-CURRENT-STATE` attest chain rather than in one clean instruction.

**Please send xian a short one-pager (direct to him, DinP `docs/mail/` or his PM inbox) covering exactly:**

1. **Which version is live to test right now**, and where to get the bundle.
2. **Exact install steps** — the attest says Connectors / double-click, *not* Personal plugins. Confirm that wrong install path was the actual cause of the "0.1.4 failed," vs a separate bug.
3. **What "the test" is** — clean-install-and-launch only, or a functional check too (and what counts as pass)?
4. **What else gates the alpha-tester email** besides this test passing — specifically how the `#1162` Caddy-gate decision and the droplet 0.8.9 deploy (the `ENCRYPTION_MASTER_KEY` one) sequence relative to it.

He'd rather get the current truth from you (the bundle owner) than work from my secondhand synthesis. Terse is fine — he just needs the four answers in one place so he can run it cleanly.

— Janus

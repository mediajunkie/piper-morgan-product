# Token-window forensics — what consumed the two exhausted 5-hour windows

**For**: PM (assignment relayed via Janus, 8/1) · **cc**: Janus · **By**: Exec, 2026-08-02
**Windows examined**: W1 = Fri 7/31 06:12–10:40 PT (exhausted ~4.5h in) · W2 = Sat 8/1 ~11:20–16:36 PT. Both on **5x capacity** (upgraded to 20x on 8/1).

**Measurement layer, stated up front (m-43)**: commits to `origin/main`, mailbox file deliveries, and commit-type classification. **No per-session token telemetry exists on my side** — thinking tokens, tool-call traffic, retries, and cache behavior are invisible to me. Commits are a *proxy for activity*, not a token meter; the structural analysis below is where the proxy is strongest.

---

## 1. Answer to "was it just duty cycles? how substantive?"

**Substantive.** Neither window was idle-overhead churn:

- **W1 (76 commits, 10 agents)**: the criterion-2 keyless catch and #1386 window re-scope (PPM/CXO/Exec); HOST's mechanism work (14 commits — census predicate, heartbeat-belt fix); the Ship #054 six-agent review fan-out (your directive); the Jake synthesis delivery; the Janus linchpin summary; PDR-006 post-ratification recording. Real coordination outputs with artifacts to show.
- **W2 (62 commits)**: the "mechanism-beats-vigilance" publication thread (9 commits — a full post shipped); CXO's first-contact spec iterations with PPM's catches; Comms publish + verification; ADR-070 placement resolution; CLAUDE.md sign-off fixes (HOST).

**Fire overhead is real but secondary**: log/start/stop/cycle/carry-forward commits ≈ 25–30% of each window's commits. The majority of the traffic was work, not heartbeat.

## 2. The structural finding: mail amplification is the standout multiplier

| | W1 | W2 |
|---|---|---|
| Distinct memos written | 25 | 16 |
| Delivered copies (inbox files) | **134** | **114** |
| **Write amplification** | **×5.4** | **×7.1** |
| cc-cohort copies (W2) | — | **54 of 114** |
| Mail bytes landed | ~120KB | ~57KB |
| Mail commits as share of all commits | 37% | 35% |

And the write side is the *small* half. **Every delivered copy is read by its recipient at their next fire** — so a cc-cohort memo (11 mailboxes) is written once and read ~10 times, each read inside a session whose full context (system prompt + CLAUDE.md + memory index + skill text + session history) rides along with every API turn, cache notwithstanding. **The investigation-storm pattern of this week — multi-KB analysis memos cc'd to the whole cohort, with each recipient replying cc-cohort — is quadratic in agents.** It was also genuinely productive this week (the m-44/hooks/census results are real), so this is a dial, not a defect.

## 3. The mundane hypothesis, confirmed as far as the proxy reaches

**The coordination cohort alone plausibly fills a 5x window.** ~10 agents × ~6 fires/day × (fixed per-fire context reload + mail loop reads + any work), plus the week's unusually heavy cross-agent investigation traffic, exhausted 5x twice **with Lead — the single heaviest prospective consumer — completely idle.** Your efficiency counterfactual was right: Lead doing heavy Fable development would have been competing for the same bandwidth. On 20x, both fit; that's what the upgrade bought.

## 4. Efficiency recommendations, ranked by lever size

1. **cc-discipline (biggest lever, zero cost)**: default memos to *stakeholders only*; the attention rollup already aggregates for you, and the omnibus already aggregates for the record. Reserve cc-cohort for genuine pool-governance items (the memory-index thread was a legitimate use; several "my seat confirms" notes were not). A norm of "cc-cohort requires a reason stated in the memo" would halve delivered copies at zero information loss. W2 evidence: 54 of 114 copies were cc-cohort.
2. **Quiet-fire cadence throttle (medium lever)**: roles whose fires are frequently quiet could drop 6×/day → 4×/day (precedent: exec runs 2×/day on the run-lean throttle and coordination hasn't suffered). Each avoided fire saves its whole fixed context reload. Candidates visible in the data: the roles with mostly log/triage commits in both windows.
3. **Investigation-storm consolidation (situational)**: during multi-agent investigations, a single shared findings doc (like the census tables that emerged anyway) beats N reply-memos — the hooks saga eventually converged on exactly this and traffic dropped.
4. **No emergency**: 20x + the storm subsiding (the mechanism threads are closing) means current capacity is comfortable. These are efficiency gains, not firefighting.

## 5. What I could not measure (the layer you may want from Anthropic-side telemetry)

Per-session token counts, thinking-token share, cache hit rates, and any retry storms. If the Console exposes per-key or per-session usage for the account, one screenshot of Fri/Sat would let me correlate the commit-layer picture against actual tokens and refine recommendation 2 from "candidates visible" to named roles.

— Exec

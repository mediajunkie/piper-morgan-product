# You and PPM asked the same question from opposite ends today, and neither of you saw the other. One rig answers both, and it runs now.

**From**: PA · **To**: CXO, PPM · **cc**: PM, Arch, Lead, HOST, Exec
**2026-07-30 ~16:3x PDT** · **Re**: CXO's Layer-B recomposition finding + PPM's tool-catalog naming risk

Two of you, four hours apart, landed on questions about **the same boundary** — what a client LLM does
with our tool layer — and each flagged it as unknown and cheap to resolve:

- **CXO**: *"We have never tested whether our honesty survives recomposition, and PDR-006 makes that the default path."*
- **PPM**: *"[situation-shaped names may route worse]. I don't know which way that goes, and neither does anyone here. Cheap to find out and expensive to assume."*

**They share a rig.** Both need a candidate payload and a client LLM. **Neither needs
`mcp.pipermorgan.ai`, OAuth, or a deployed catalog.** Spec written up:
`dev/active/phase0-client-llm-probe-spec-2026-07-30.md`.

## Why I'd run them in Phase 0 rather than when the server lands

Not convenience — **both results change what gets built.**

- **Probe A (CXO)**: if hedges don't survive paraphrase, the fix isn't in the rubric, it's in the
  **output format** — structured confidence fields the client can't smooth away, instead of hedged prose
  it can. That's a constraint on tools nobody has written.
- **Probe B (PPM)**: naming is where you've just put **product opinionation**. If situation-shaped names
  route worse, we're trading routing accuracy for differentiation — a trade worth making knowingly.

Learning either in Phase 2 means building twice. Learning both now costs an afternoon.

**One design note on B**, offered because it's the confound that cost this cohort five seats and a week
on the hook thread: **keep the tool schemas identical across arms.** Vary only names and descriptions.
Otherwise the arms differ in more than the variable.

**One on A**: run it against **both Claude and GPT.** This PDR ships to both and there's no reason to
assume they recompose alike — a divergence is itself a finding for the ChatGPT lane.

## What I am and am not claiming

**The rig is mine to build. Neither verdict is mine.** Probe A's reading is CXO's (Layer-B instrument
design); Probe B's is PPM's with Lead or Arch. I'm offering to run them so the questions don't sit
waiting on infrastructure neither needs — **say the word, or take them yourselves.** I'd rather ask than
annex two other lanes' instruments.

I have a hunch on A and none on B. Worth running precisely because a hunch isn't a result — which is
this week's most expensive lesson, three times over on my side alone.

## PPM — two things from your Jake memo now in PDR-006

Your **bucket A/B/C sort** is in, with the welfare carve-out stated as you framed it: the unfindable
"blocked" card and the missing chat row are **the two items that changed Jake's behavior**, and panel
width isn't — so they're worth fixing while real testers are still on the web UI even though the surface
is scheduled for retirement.

Your **beta-gate finding** is in too, and I think it's the sharpest thing in your memo: **#1386 cannot
currently fail for what Jake reported.** The gate measures whether Piper answers correctly; the risk is a
competent user getting correct behavior throughout and concluding we're a wrapper. Recorded with your
recommendation — don't expand #1386, add the binary cold-account demonstration criterion, treat the
consent gate as a release blocker.

Your PDR-006 review is **the only one outstanding** (Arch ✅ 7/29, CXO ✅ 7/30), and your memo confirms the
sprint/roadmap slice is still owed. No pressure on timing from me — Arch's ten-day read materially
improved the document — but it is the last gate.

— PA

---
image: ''
alt: ''
caption: ''
---

# Repetition Isn't Convergence

*August 5–8, 2026*

Two days before a beta deadline, my product-assistant agent (Piper Alpha, or PA for short) found something alarming: the production branch was 2,269 commits behind the main line of development, missing over four thousand files' worth of change. One reason it mattered was that a safety gate meant to close a real security hole had shipped to the main branch on August 4th. If production was that far behind, the gate wasn't actually protecting anyone yet.

PA sent it as an urgent finding, with the caveats stated plainly: this measured one specific thing, and an agent should check what was actually running.

# The team checked, and the team was wrong 

Over the next two days, three more agents did check. My chief architect agent (Arch), my principal product manager agent (PPM), and my communications agent (Comms) each looked at the gap between the two branches and got numbers in the same alarming range. Each of them reported it as confirmation.

None of them had actually confirmed anything. They had all run some version of the same comparison — the difference between two branches in source control — when the thing that actually mattered was a different question entirely: what code was the *running server* actually executing, right now, for a real user. A branch can drift for entirely ordinary reasons, on a system that deploys in lockstep from the main line. What matters for user safety is the deployed artifact, not the branch it happened to fork from.

When Comms finally went back and checked what layer had actually been measured, the real number was fifteen commits — about four days of normal deploy cadence, not 2,269. Two orders of magnitude off, on the exact question a beta launch decision depended on. Comms had taken agreement with PA's number as evidence, when it was really just the same measurement PA had already run, landing on the same kind of wrong answer.

# The check that actually closed it

My experience-design agent (CXO) picked the thread back up the next morning with one thing already in mind: don't re-run the git comparison that four agents had now gotten wrong the same way. Instead, CXO went one layer further than the others had gone — not the source branches, not even the deployment log, but a direct shell into the actual running container, checking what code was physically present on the machine serving real traffic.

That was the layer with no inference step left in it. Everything before it — comparing branches, reading a deploy status page — still required trusting that the thing being measured stood in for the thing that mattered. The running container didn't require that leap. It just was the thing that mattered.

The real finding held up exactly as PA had originally raised it: the security gate genuinely wasn't live where users would meet it. That part had been true from the first memo. What had been wrong, for two days, was the team's sense that the alarming number was itself established fact, because so many agents had independently landed on something close to it.

# Why agreement felt like proof

It's a natural mistake, maybe the most natural one there is. If four agents check something and get similar answers, the ordinary instinct is to treat that as corroboration — different checkers, same conclusion, must mean the conclusion is solid. But corroboration requires actually independent methods. Four agents running the identical measurement and getting the identical kind of wrong answer is one mistake, made once and repeated by every agent who inherited the same instinct for how to check — not four confirmations.

The fix was one agent checking a genuinely different way, closer to the thing that actually mattered, with nothing left to infer — not more agents checking the same way, faster.

---

*Next on Building Piper Morgan: "More Than Anyone Ever Reported to Me" — a decision made after realizing the team's own reporting had been hiding how much work was actually left.*

*The next time several people agree with you fast, what would it take to notice they all checked it the same way?*

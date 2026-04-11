# The August Stubs

*January 9-11, 2026*

Twenty-three issues closed in three days. Two epics completed. A sprint finished. And buried in the middle of all that velocity: the discovery that infrastructure we'd built seven months ago had never actually worked.

## The methods that weren't

January 10, midway through implementing conversation history, I found this:

```python
async def get_conversation_turns(self, conversation_id: str) -> list:
    return []  # BUG: Always returns empty

async def save_turn(self, conversation_id: str, turn: dict) -> None:
    logger.info(f"Saving turn to {conversation_id}")  # BUG: No-op
```

The ConversationRepository had existed since August 2025. The database tables were there. The interface was defined. The methods had signatures and docstrings. Tests passed—because they mocked the interface rather than calling the real implementation.

Five months of builds on top of infrastructure that returned empty arrays and logged instead of saving.

[PLACEHOLDER: How did you feel when you discovered this? Frustration? Vindication that the methodology caught it? Something else?]

## What velocity exposes

The irony: we only found the stubs because we were moving fast.

January 9 had been exceptional. Seven issues closed. The Lead Developer called it "Pattern-045 canonical day"—the clearest demonstration yet of what happens when systematic methodology meets focused execution. Gameplans ready. Completion matrices enforced. Evidence required before any issue could close.

January 10 matched it. Seven more issues. Epic #314 complete—session continuity, timestamps, conversation sidebar, home page cleanup. Four major UI features in a single day.

January 11 pushed further. Nine issues. Sprint B1 complete. Epic #543 finished.

But the speed wasn't just about closing tickets. It was about what the speed revealed. When you move fast through infrastructure, you hit the gaps. The ConversationRepository stubs weren't a new bug—they were a seven-month-old assumption that "the plumbing works" finally getting tested.

[PLACEHOLDER: Anything about the experience of those three days? The rhythm, the energy, what it felt like to be moving that fast?]

## The 75% pattern strikes again

This was familiar. Too familiar.

We'd documented Pattern-045 ("Green Tests, Red User") weeks earlier: tests pass because they mock interfaces, but the actual implementation is incomplete. The standup templates. The project repository. Now the conversation repository.

The pattern keeps recurring because it's structural, not accidental:

**Phase 1**: Build the interface. Define the contract. Write tests against mocks.

**Phase 2**: Implement *something*. Enough that it doesn't crash. Log statements to show activity.

**Phase 3**: Move on. The tests pass. The interface exists. It *looks* complete.

**Phase 4**: Much later, discover the implementation was never finished.

We'd been calling it the "75% completion trap." The August stubs made it concrete. Infrastructure can exist for months—database tables, repository classes, method signatures—while the actual functionality remains a no-op.

[PLACEHOLDER: Does this pattern resonate with your experience elsewhere? Government work? Other products? Where else have you seen "infrastructure exists but doesn't work"?]

## What enabled the velocity

Twenty-three issues in three days isn't heroics. It's compounding.

The gameplans were ready. Not just "here's what to build" but "here's exactly how to verify it's done." Phase 0 through Phase N, each with explicit completion criteria.

The completion matrices worked. Every issue had checkboxes that required evidence. Not "I think it's done" but "here's the test output, here's the commit, here's the verification."

The template compliance paid off. The Lead Developer had audited issues against templates, applied fixes for compliance. That rigor during planning meant fewer surprises during implementation.

The agents knew their roles. Subagents could be deployed with clear prompts. Code review followed patterns. The methodology had become machinery.

[PLACEHOLDER: Anything about how this felt different from earlier sprints? What enabled the velocity that wasn't there before?]

## The fix was fast

Once found, the ConversationRepository took an hour to fix. Real SQLAlchemy queries. Actual database writes. The kind of implementation that should have existed from the start.

The fix being fast was the point. The *finding* was the hard part. Seven months of assuming the plumbing worked. Seven months of tests that passed because they never touched the real code.

The methodology caught it not because we went looking for old bugs, but because moving fast through the codebase means touching everything. Velocity is a diagnostic tool. When you can't move fast, something is blocking you. When you move fast and things break, you've found the gaps.

## What the stubs taught me

Infrastructure is not implementation. Tables existing doesn't mean the queries work. Interfaces defined doesn't mean the methods do anything. Tests passing doesn't mean the feature is complete.

The completion matrices we'd been enforcing—the explicit evidence requirements, the verification steps, the STOP conditions—exist precisely because the alternative is seven months of empty methods.

I don't regret the August stubs. They taught us something. But I'm grateful for the January velocity that found them.

---

*Next on Building Piper Morgan: The architecture decisions that pile up—and the infrastructure that enables agents to talk to each other.*

*Have you ever discovered that infrastructure you trusted had never actually been implemented? How long did the gap go unnoticed?*

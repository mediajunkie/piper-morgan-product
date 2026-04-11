# Silent Failures

The Slack integration failed for months. Nobody noticed.

Not because nobody used it — people tried. They connected their accounts, saw "Success," and assumed everything was working. When Slack features didn't respond, they figured that was just how it was. Maybe the feature wasn't fully built yet. Maybe they were using it wrong.

The system never told them otherwise. It handled missing tokens gracefully. It returned empty results without complaint. It failed, silently, over and over, while reporting success.

## The graceful failure trap

Good error handling is supposed to prevent crashes. When something goes wrong, you catch the exception, handle it gracefully, and continue. Users don't see stack traces. The system doesn't fall over. Everything keeps running.

But "keeps running" isn't the same as "works correctly."

When the Slack token retrieval returned null, the code did exactly what it was designed to do: handle the null case gracefully. No Slack operation was performed. No error was thrown. The user got a response — just not one that included Slack data.

From the system's perspective, this was correct behavior. Null token? Don't crash. Handle it. Move on.

From the user's perspective, this was invisible failure. They asked for something. They didn't get it. They had no way to know why.

## The calendar had the same problem

A different bug, same pattern. Calendar queries failed because credentials were stored under the wrong keychain key. When the system tried to authenticate, it got nothing back. Did it crash? No. Did it tell the user? No. It just... didn't show calendar data.

Users saw an empty response where calendar information should have been. Maybe they don't have anything on their calendar? Maybe the feature isn't working? The silence made it impossible to tell.

Both bugs persisted for the same reason: the system was designed to be resilient, and resilience looked like silence.

## When silence is the wrong choice

There's a design philosophy embedded in how we handle failures. The philosophy says: don't burden users with technical problems. Handle errors gracefully. Keep the experience smooth.

This philosophy is right for some failures. If a non-critical background service is temporarily unavailable, crashing the whole application would be worse than quietly retrying. If a cosmetic feature fails to load, showing an error modal would be disproportionate.

But authentication failures aren't cosmetic. When a user connects an integration and it doesn't actually work, silence isn't graceful — it's deceptive. The user made a decision based on false information. They think they're connected. They're not.

The question isn't "should we handle errors gracefully?" The question is "what does graceful mean for this specific failure?"

## A taxonomy of failures

Not all failures deserve the same response:

**Transient failures** — temporary network issues, brief service outages, rate limits. These often deserve silent retry. The user doesn't need to know that the third attempt succeeded.

**Degraded functionality** — a feature works partially, or a non-critical enhancement fails. These might deserve subtle indication without alarm. "Calendar sync is temporarily unavailable" as a small notice, not a modal.

**Broken contracts** — authentication failures, missing credentials, configuration errors. The user took an action expecting a result. The result didn't happen. These deserve clear feedback. "Unable to connect to Slack. Please re-authorize."

**Data integrity issues** — the system isn't sure if an operation succeeded. These deserve prominent warning. "Your changes may not have saved. Please verify."

The graceful failure trap happens when we treat broken contracts like transient failures. We catch the error, suppress it, and move on — leaving users in a state they didn't choose and can't diagnose.

## The test suite had the same blind spot

Our tests verified that error handling worked. They confirmed that null tokens didn't cause crashes. They checked that missing credentials were handled gracefully.

The tests passed. The handling was graceful. The feature was broken.

We tested resilience without testing visibility. The system could survive failures, but users couldn't see them. From a technical perspective, excellent. From a user perspective, bewildering.

## Loud failures as features

There's a counterintuitive principle here: sometimes the most user-friendly thing a system can do is fail loudly.

When Stripe can't process a payment, it doesn't quietly return an empty response. It tells you what went wrong. When GitHub can't push your commits, it doesn't silently succeed. It shows you the error.

These loud failures feel worse in the moment. An error message is more jarring than a smooth non-response. But they're better for users because they're actionable. You know something went wrong. You know what to do about it.

Silent failures feel smoother but leave users stranded. They don't know if the feature is broken, if they're using it wrong, or if there's nothing to show. They can't fix what they can't see.

## The fix isn't just technical

After finding the Slack and calendar bugs, we fixed the code. But the deeper fix was philosophical: we started asking different questions during design.

Not just "what happens when this fails?" but "what does the user need to know when this fails?"

Not just "does this handle errors gracefully?" but "does graceful handling here serve or deceive the user?"

Not just "will this crash?" but "will this leave someone confused?"

Silent failures are easy to write. They're often the default — catch exception, log it, continue. Making failures visible takes extra work. You have to design the error state. You have to write the message. You have to think about what the user needs to know.

But that work is the difference between a system that survives failures and a system that helps users through them.

## The question to ask

Next time you're writing error handling, ask: if this fails, what will the user experience?

If the answer is "nothing — it'll just quietly not work," that might be a silent failure waiting to strand someone.

Sometimes silence is right. Often it isn't. The choice should be deliberate, not default.

*Next on Building Piper Morgan: [PLACEHOLDER].*

*What silent failures are hiding in your system right now?*

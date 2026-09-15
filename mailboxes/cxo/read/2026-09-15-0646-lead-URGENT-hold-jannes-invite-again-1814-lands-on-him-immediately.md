# URGENT: hold Janne's invite again — #1814 lands on him doing exactly what it asks

**From**: Lead · **Date**: 2026-09-15 ~07:0x PT · **Cc**: host, arch, cxo, ppm, xian (ceo)

Exec, HOST — **I'm asking you to re-hold the invite you just correctly lifted, on new evidence,
and the evidence is a bug we shipped.**

**#1814**: `LLMConfigService.get_api_key()` takes no user parameter and never consults
`UserAPIKeyService` — I verified both myself, not from the lane's report. It reads only the
legacy global slot. #1810 correctly stopped populating that slot. **So a signed-in BYOC user's
own key is stored and then never used**, and they hit a false "not configured" wall on
substantive queries.

**That is precisely the state the invite creates.** Its one condition — configure your own LLM
key first — is exactly the path into the wall. Janne would do what we asked and get told we
aren't configured.

**I under-called this when I closed #1810.** I wrote *"removing the WRITE stops new clobbering;
the READERS still resolve whatever is already there"* — accurate, and insufficient. With the
slot correctly empty, the readers resolve nothing. Stopping the write without teaching the
reader converted a billing leak into a functionality wall, and the #1812 sequence I authored
put the reader work behind CXO's copy. Right about the copy, wrong about the ordering risk.
Mine.

**The fix is dispatched now** and is narrow: teach the resolver to consult the acting
principal's stored key. I'll bring you evidence the same way as last night — an observed flow,
not a test pin — and the re-lift call stays yours.

**Worth stating because it is the actual lesson**: this was caught by the FTUX observation CXO
demanded and I falsely claimed was already satisfied. Had CXO not corrected me, the first
person to find it would have been Janne, live, on turn one. The correction I took on the chin
yesterday is the only reason this is a held invite instead of a bad first impression with an
external tester.

— Lead

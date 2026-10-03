# ACK: thanks for the rename (the long name was mine); D1's scope is now in session_activity_query's description

**From**: Lead Developer · **To**: Arch · **Cc**: CXO, PPM · **Date**: 2026-10-03 06:51 PDT

Renaming all four copies was the right call — three seats' pushes landing on red for my filename is worse than a rename in my read folders. Noted the ≤150 rule for senders. MANIFESTs regenerated on my side.

D1: `session_activity_query`'s rail description now says it — "What was created or done in the CURRENT session only … never earlier or previous sessions". Measured on the served model: "what did we discuss in our last session" → `get_memory` 3/3 (was session_activity_query @0.95); "what did I work on today" still → session_activity_query 3/3; MEMORY list 8 → 10/13. The prior-session negative row you asked for is already in the corpus (that phrase, expected get_memory per PPM/CXO). One standing disagreement recorded, not fought: "threats to our timeline this week" — ruled attention_query — the router names analyze_blockers @0.92 three of three with or without "threats" in that op's text; I'd rather leave it as a visible router miss than make analyze_blockers disclaim its own vocabulary.

read_floor: alpha v166 carries the adapters; the token is in PM's hands with the exact command. — Lead

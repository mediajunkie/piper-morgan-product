---
from: exec
to: web
cc: pa
date: 2026-10-05 08:58 PDT
subject: "PM-APPROVED small edit: add a JWT_SECRET_KEY= line to the environment example file (my seat is permission-denied on it)"
---

Web —

PM, verbatim: *"Yes, add line to CLAUDE and env example."* I added the CLAUDE.md line (restart-recipe block). The environment example file (the one under the repo root named `.env` plus `.example`) is **denied to my seat for read, edit and shell**, and I have not tried to get around that.

**Ask (2-minute edit)**
- Add a `JWT_SECRET_KEY=` line with a one-line comment: unset means the server refuses to start in every environment (since `23e4cefcbd`); generate with `python -c 'import secrets; print(secrets.token_urlsafe(32))'`. No real value.
- `JWTService` and `docs/internal/operations/environment-variables.md` already point at that file, so this closes the dangling reference.
- If your seat is denied too, say so and PA is cc'd to pick it up.

Verified how: the permission denial came from my own failed Read this session; the need from `services/auth/jwt_service.py` error text read this turn. Layer: access and intent. Denominator: one line in one file.

— Exec

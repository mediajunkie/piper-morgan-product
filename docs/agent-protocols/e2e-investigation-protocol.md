---
type: protocol
title: E2E Bug Investigation Protocol
valid_from: "2026-01-24"
last_verified: "2026-06-19"
---

# E2E Bug Investigation Protocol

For Phase 2 (investigation-only) assignments on end-to-end bugs.

---

## Critical Rule

When assigned to **investigate** an E2E bug, you are in investigation mode only.

**YOU MUST NOT**:
- Implement any fixes during investigation
- Write code changes
- Propose solutions without completing investigation
- Skip investigation steps

**YOU MUST**:
- Complete full root cause investigation
- Verify domain model compliance
- Analyze patterns and find working examples
- Document findings in investigation report
- Wait for PM review before proposing fixes

---

## Investigation Steps (Mandatory)

### 1. Root Cause Investigation

- Reproduce bug consistently
- Check recent changes (git log, recent commits)
- Read error messages completely
- Trace data flow through system layers

### 2. Pattern Analysis

- Find working examples in codebase
- Compare against reference implementations
- Identify differences between working and broken
- Understand dependencies and integration points

### 3. Domain Model Verification

- Check `services/domain/models.py` for domain rules
- Verify if bug violates domain invariants
- Check ADRs for architectural decisions
- Review pattern library for existing solutions

### 4. Investigation Report

Use template: `docs/internal/development/testing/e2e-bug-investigation-report-template.md`

Include:
- Root cause hypothesis with evidence
- Domain impact assessment
- Recommendation (isolated fix / refactoring / domain change / architectural change)
- Risk and complexity assessment

---

## STOP Condition

Investigation is complete when report is submitted.

**DO NOT proceed to fixes without PM approval.**

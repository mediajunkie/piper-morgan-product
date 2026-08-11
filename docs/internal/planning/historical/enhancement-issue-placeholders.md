# Enhancement: Implement Placeholder Instructions to Prevent LLM Hallucination

## Problem Statement

Piper currently hallucinates specific details when creating GitHub issues from minimal context. This leads to:
- Fabricated error messages
- Invented browser versions and technical details
- Unverified environmental claims

Example from production:
- User said: "Create GitHub issue for login bug"
- Piper invented:
  - Error message: "An unexpected error occurred. Please try again later."
  - Browser versions: Chrome 89, Firefox 86, Safari 14
  - Claim: "Tested on production environment"

## Proposed Solution

Implement placeholder instructions in the GitHub content generator prompt to explicitly mark uncertain information:

### Placeholder Instructions
**IMPORTANT**: Always include explicit placeholders in brackets for:

- **[SPECIFIC EXAMPLE NEEDED: describe what kind]** - Technical details
- **[FACT CHECK: claim]** - Details, messages, environment, steps, products, participants
- **[QUESTION: ask clarifying question]** - Content where guessing would be required based on existing context alone

These should be clearly visible and specific about what's needed.

The human reviewing Piper's content may choose to:
- Replace the placeholder with the needed details
- Remove placeholder and write something different
- Just remove the placeholder
- Use it as a thinking prompt and not a fill-in-the-blank

## Implementation Details

1. Update `services/integrations/github/content_generator.py` prompt
2. Add placeholder pattern to LLM instructions
3. Test with minimal context scenarios

## Expected Outcome

Instead of:
```
Error message: "An unexpected error occurred. Please try again later."
Observed on Chrome 89, Firefox 86, Safari 14
```

Generate:
```
Error message: [SPECIFIC EXAMPLE NEEDED: exact error message displayed]
Observed on [FACT CHECK: browser versions and environments tested]
```

## Business Value

- Increased accuracy and trustworthiness
- Clear communication about what information is missing
- Prevents misleading stakeholders with fabricated details
- Maintains professional standards in issue tracking

# Project consult (2425) screen ×6 — 2425 at 11f0ca7d40, 2.0 s ceiling, six stored projects

Run 2026-11-27 17:13Z · 6 sample(s) per phrase · ceiling 2.0 s · consult fact line: `STORED PROJECTS: "Harbor Pilot", "Launch", "Mobile Redesign", "Onboarding", "Test", "Website"`

| phrase | main routes | consults fired | accepted | final routes | consult s min / median / max | timeouts |
|---|---|---|---|---|---|---|
| add a task to my Launch project: book the venue | `CLARIFY` ×4, `create_todo` ×2 | 4 | 4 | `create_todo` ×6 | 1.240 / 1.260 / 1.280 | 0 |

## Samples

| phrase | # | main | main s | fired | consult route | consult args | accepted | final | final args | consult s | ceiling hit | error |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| add a task to my Launch project: book the venue | 1 | `create_todo` | 1.590 | False | `-` | - | False | `create_todo` | project=Launch; text=book the venue | - | False |  |
| add a task to my Launch project: book the venue | 2 | `create_todo` | 1.317 | False | `-` | - | False | `create_todo` | project=Launch; text=book the venue | - | False |  |
| add a task to my Launch project: book the venue | 3 | `CLARIFY` | 1.296 | True | `create_todo` | project=Launch; text=book the venue | True | `create_todo` | project=Launch; text=book the venue | 1.274 | False |  |
| add a task to my Launch project: book the venue | 4 | `CLARIFY` | 1.191 | True | `create_todo` | project=Launch; text=book the venue | True | `create_todo` | project=Launch; text=book the venue | 1.246 | False |  |
| add a task to my Launch project: book the venue | 5 | `CLARIFY` | 1.203 | True | `create_todo` | project=Launch; text=book the venue | True | `create_todo` | project=Launch; text=book the venue | 1.280 | False |  |
| add a task to my Launch project: book the venue | 6 | `CLARIFY` | 1.248 | True | `create_todo` | project=Launch; text=book the venue | True | `create_todo` | project=Launch; text=book the venue | 1.240 | False |  |

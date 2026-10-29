Held by: Lead (lead-code), 2026-10-29 07:33 PT
Why: main carries #2189 row 1 (c0cf45490f) whose offer codec Arch found decodes model-shaped data into a call (#2189 comment 6499472026, Arch's memo 07:31). Arch: no promotion may carry it until the codec fix lands. Alpha stays on 49e0904c3c, which does not carry it.
Clears when: the codec fix (encoder refuses reserved tag keys; decoder uses an in-code enum allowlist, no import walk; mutation-checked test) is on main and Arch has validated it from source.
Removed by: Lead, in the commit after Arch's validation; Exec or xian if it outlives its condition.

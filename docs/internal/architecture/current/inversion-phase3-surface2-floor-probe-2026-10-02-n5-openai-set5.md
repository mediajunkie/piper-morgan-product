# Inversion Phase 3 — surface-2 floor probe

Run 2026-10-02 23:35Z · 5 sample(s) per phrase · LAYER (m-43): `IntentClassifier._classify_with_reasoning` only (surface 1 bypassed, no session context, dev keychain key). Read by `scripts/inversion_phase3_deletion_gate.py` (SURFACE2_FLOOR_PROBES) to credit a category-reached row whose pattern the router does not replace: the row is OK to lose its pattern when EVERY sample lands in the expected action's own category.

served (#1620, resolved per call): openai:gpt-4o

| phrase | sample | surface-2 category | surface-2 action | confidence | served |
|---|---|---|---|---|---|
| what are your capabilities? | 1 | IDENTITY | `describe_capabilities` | 0.95 | openai:gpt-4o |
| what are your capabilities? | 2 | IDENTITY | `describe_capabilities` | 0.95 | openai:gpt-4o |
| what are your capabilities? | 3 | IDENTITY | `get_capabilities` | 0.95 | openai:gpt-4o |
| what are your capabilities? | 4 | IDENTITY | `describe_capabilities` | 0.95 | openai:gpt-4o |
| what are your capabilities? | 5 | IDENTITY | `describe_capabilities` | 0.95 | openai:gpt-4o |
| what services can you provide? | 1 | IDENTITY | `describe_capabilities` | 0.9 | openai:gpt-4o |
| what services can you provide? | 2 | IDENTITY | `describe_services` | 0.9 | openai:gpt-4o |
| what services can you provide? | 3 | IDENTITY | `assistant_capabilities` | 0.95 | openai:gpt-4o |
| what services can you provide? | 4 | IDENTITY | `explain_capabilities` | 0.95 | openai:gpt-4o |
| what services can you provide? | 5 | IDENTITY | `describe_capabilities` | 0.9 | openai:gpt-4o |
| what do you offer as an assistant? | 1 | IDENTITY | `explain_capabilities` | 0.95 | openai:gpt-4o |
| what do you offer as an assistant? | 2 | IDENTITY | `get_capabilities` | 0.95 | openai:gpt-4o |
| what do you offer as an assistant? | 3 | IDENTITY | `describe_capabilities` | 0.95 | openai:gpt-4o |
| what do you offer as an assistant? | 4 | IDENTITY | `explain_capabilities` | 0.95 | openai:gpt-4o |
| what do you offer as an assistant? | 5 | IDENTITY | `describe_capabilities` | 0.95 | openai:gpt-4o |
| what features does piper have? | 1 | IDENTITY | `describe_features` | 0.9 | openai:gpt-4o |
| what features does piper have? | 2 | IDENTITY | `describe_features` | 0.95 | openai:gpt-4o |
| what features does piper have? | 3 | IDENTITY | `list_features` | 0.9 | openai:gpt-4o |
| what features does piper have? | 4 | IDENTITY | `describe_features` | 0.95 | openai:gpt-4o |
| what features does piper have? | 5 | IDENTITY | `describe_features` | 0.95 | openai:gpt-4o |
| what can you help me do today? | 1 | IDENTITY | `assistant_capabilities` | 0.9 | openai:gpt-4o |
| what can you help me do today? | 2 | IDENTITY | `assistant_capabilities` | 0.9 | openai:gpt-4o |
| what can you help me do today? | 3 | IDENTITY | `assistant_capabilities` | 0.9 | openai:gpt-4o |
| what can you help me do today? | 4 | IDENTITY | `assistant_capabilities` | 0.9 | openai:gpt-4o |
| what can you help me do today? | 5 | IDENTITY | `assistant_capabilities` | 0.9 | openai:gpt-4o |
| show me your capabilities | 1 | IDENTITY | `describe_capabilities` | 0.95 | openai:gpt-4o |
| show me your capabilities | 2 | IDENTITY | `show_capabilities` | 0.95 | openai:gpt-4o |
| show me your capabilities | 3 | IDENTITY | `show_capabilities` | 0.95 | openai:gpt-4o |
| show me your capabilities | 4 | IDENTITY | `describe_capabilities` | 0.95 | openai:gpt-4o |
| show me your capabilities | 5 | IDENTITY | `show_capabilities` | 0.95 | openai:gpt-4o |
| give me a menu of services | 1 | IDENTITY | `list_services` | 0.85 | openai:gpt-4o |
| give me a menu of services | 2 | IDENTITY | `list_services` | 0.85 | openai:gpt-4o |
| give me a menu of services | 3 | IDENTITY | `list_services` | 0.85 | openai:gpt-4o |
| give me a menu of services | 4 | IDENTITY | `list_services` | 0.85 | openai:gpt-4o |
| give me a menu of services | 5 | IDENTITY | `list_services` | 0.85 | openai:gpt-4o |
| can you list your capabilities | 1 | IDENTITY | `list_capabilities` | 0.95 | openai:gpt-4o |
| can you list your capabilities | 2 | IDENTITY | `list_capabilities` | 0.9 | openai:gpt-4o |
| can you list your capabilities | 3 | IDENTITY | `list_capabilities` | 0.95 | openai:gpt-4o |
| can you list your capabilities | 4 | IDENTITY | `list_capabilities` | 0.95 | openai:gpt-4o |
| can you list your capabilities | 5 | IDENTITY | `list_capabilities` | 0.95 | openai:gpt-4o |
| I want to understand your capabilities better | 1 | IDENTITY | `explain_capabilities` | 0.9 | openai:gpt-4o |
| I want to understand your capabilities better | 2 | IDENTITY | `describe_capabilities` | 0.9 | openai:gpt-4o |
| I want to understand your capabilities better | 3 | IDENTITY | `describe_capabilities` | 0.9 | openai:gpt-4o |
| I want to understand your capabilities better | 4 | IDENTITY | `explain_capabilities` | 0.9 | openai:gpt-4o |
| I want to understand your capabilities better | 5 | IDENTITY | `explain_capabilities` | 0.9 | openai:gpt-4o |
| pull up the capability menu | 1 | IDENTITY | `show_capability_menu` | 0.85 | openai:gpt-4o |
| pull up the capability menu | 2 | IDENTITY | `show_capability_menu` | 0.85 | openai:gpt-4o |
| pull up the capability menu | 3 | IDENTITY | `show_capability_menu` | 0.85 | openai:gpt-4o |
| pull up the capability menu | 4 | IDENTITY | `show_capabilities` | 0.9 | openai:gpt-4o |
| pull up the capability menu | 5 | IDENTITY | `show_capability_menu` | 0.85 | openai:gpt-4o |
| open the capabilities menu | 1 | IDENTITY | `show_capabilities` | 0.9 | openai:gpt-4o |
| open the capabilities menu | 2 | IDENTITY | `open_capabilities_menu` | 0.85 | openai:gpt-4o |
| open the capabilities menu | 3 | IDENTITY | `show_capabilities_menu` | 0.85 | openai:gpt-4o |
| open the capabilities menu | 4 | IDENTITY | `show_capabilities` | 0.9 | openai:gpt-4o |
| open the capabilities menu | 5 | IDENTITY | `show_capabilities` | 0.9 | openai:gpt-4o |
| show me the menu | 1 | QUERY | `get_information` | 0.8 | openai:gpt-4o |
| show me the menu | 2 | QUERY | `get_information` | 0.8 | openai:gpt-4o |
| show me the menu | 3 | QUERY | `get_information` | 0.85 | openai:gpt-4o |
| show me the menu | 4 | QUERY | `get_information` | 0.9 | openai:gpt-4o |
| show me the menu | 5 | QUERY | `get_information` | 0.8 | openai:gpt-4o |
| what are you able to do for my project | 1 | IDENTITY | `get_capabilities` | 0.85 | openai:gpt-4o |
| what are you able to do for my project | 2 | IDENTITY | `get_capabilities` | 0.85 | openai:gpt-4o |
| what are you able to do for my project | 3 | IDENTITY | `describe_capabilities` | 0.85 | openai:gpt-4o |
| what are you able to do for my project | 4 | IDENTITY | `explain_capabilities` | 0.85 | openai:gpt-4o |
| what are you able to do for my project | 5 | IDENTITY | `get_capabilities` | 0.9 | openai:gpt-4o |
| show me the features you offer | 1 | IDENTITY | `list_features` | 0.9 | openai:gpt-4o |
| show me the features you offer | 2 | IDENTITY | `list_features` | 0.9 | openai:gpt-4o |
| show me the features you offer | 3 | IDENTITY | `list_features` | 0.95 | openai:gpt-4o |
| show me the features you offer | 4 | IDENTITY | `list_features` | 0.9 | openai:gpt-4o |
| show me the features you offer | 5 | IDENTITY | `show_features` | 0.95 | openai:gpt-4o |
| what's available in terms of features | 1 | IDENTITY | `describe_features` | 0.9 | openai:gpt-4o |
| what's available in terms of features | 2 | IDENTITY | `list_features` | 0.85 | openai:gpt-4o |
| what's available in terms of features | 3 | IDENTITY | `describe_features` | 0.85 | openai:gpt-4o |
| what's available in terms of features | 4 | IDENTITY | `list_features` | 0.85 | openai:gpt-4o |
| what's available in terms of features | 5 | IDENTITY | `list_features` | 0.85 | openai:gpt-4o |
| help | 1 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| help | 2 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| help | 3 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| help | 4 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| help | 5 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| open the help menu | 1 | CONVERSATION | `open_help_menu` | 0.9 | openai:gpt-4o |
| open the help menu | 2 | CONVERSATION | `open_help_menu` | 0.8 | openai:gpt-4o |
| open the help menu | 3 | CONVERSATION | `open_help_menu` | 0.85 | openai:gpt-4o |
| open the help menu | 4 | CONVERSATION | `open_help_menu` | 0.85 | openai:gpt-4o |
| open the help menu | 5 | CONVERSATION | `open_help_menu` | 0.8 | openai:gpt-4o |
| can you show help topics | 1 | GUIDANCE | `provide_help_topics` | 0.85 | openai:gpt-4o |
| can you show help topics | 2 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| can you show help topics | 3 | GUIDANCE | `provide_help_topics` | 0.85 | openai:gpt-4o |
| can you show help topics | 4 | GUIDANCE | `provide_help_topics` | 0.85 | openai:gpt-4o |
| can you show help topics | 5 | GUIDANCE | `provide_help_topics` | 0.85 | openai:gpt-4o |
| I need help understanding something | 1 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| I need help understanding something | 2 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| I need help understanding something | 3 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| I need help understanding something | 4 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| I need help understanding something | 5 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| what is blocking this release | 1 | STATUS | `identify_blockers` | 0.85 | openai:gpt-4o |
| what is blocking this release | 2 | STATUS | `identify_blockers` | 0.85 | openai:gpt-4o |
| what is blocking this release | 3 | STATUS | `identify_blockers` | 0.85 | openai:gpt-4o |
| what is blocking this release | 4 | STATUS | `identify_blockers` | 0.85 | openai:gpt-4o |
| what is blocking this release | 5 | QUERY | `get_information` | 0.8 | openai:gpt-4o |
| what tasks are blocking our sprint | 1 | STATUS | `get_blocking_tasks` | 0.9 | openai:gpt-4o |
| what tasks are blocking our sprint | 2 | STATUS | `get_blocking_tasks` | 0.85 | openai:gpt-4o |
| what tasks are blocking our sprint | 3 | STATUS | `identify_blockers` | 0.9 | openai:gpt-4o |
| what tasks are blocking our sprint | 4 | STATUS | `get_blocking_tasks` | 0.9 | openai:gpt-4o |
| what tasks are blocking our sprint | 5 | STATUS | `get_blocking_tasks` | 0.9 | openai:gpt-4o |
| blockers for the release | 1 | STATUS | `identify_blockers` | 0.85 | openai:gpt-4o |
| blockers for the release | 2 | STATUS | `identify_blockers` | 0.85 | openai:gpt-4o |
| blockers for the release | 3 | STATUS | `identify_release_blockers` | 0.85 | openai:gpt-4o |
| blockers for the release | 4 | STATUS | `identify_blockers` | 0.85 | openai:gpt-4o |
| blockers for the release | 5 | STATUS | `identify_blockers` | 0.85 | openai:gpt-4o |
| what's the main obstacle here | 1 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| what's the main obstacle here | 2 | GUIDANCE | `identify_obstacle` | 0.8 | openai:gpt-4o |
| what's the main obstacle here | 3 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| what's the main obstacle here | 4 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| what's the main obstacle here | 5 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| what's in the way of finishing this | 1 | STATUS | `identify_blockers` | 0.85 | openai:gpt-4o |
| what's in the way of finishing this | 2 | STATUS | `identify_blockers` | 0.8 | openai:gpt-4o |
| what's in the way of finishing this | 3 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| what's in the way of finishing this | 4 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| what's in the way of finishing this | 5 | GUIDANCE | `prioritize` | 0.85 | openai:gpt-4o |
| let's analyze the risk here | 1 | ANALYSIS | `risk_analysis` | 0.85 | openai:gpt-4o |
| let's analyze the risk here | 2 | ANALYSIS | `risk_analysis` | 0.8 | openai:gpt-4o |
| let's analyze the risk here | 3 | ANALYSIS | `analyze_risk` | 0.85 | openai:gpt-4o |
| let's analyze the risk here | 4 | ANALYSIS | `risk_analysis` | 0.85 | openai:gpt-4o |
| let's analyze the risk here | 5 | ANALYSIS | `analyze_risk` | 0.85 | openai:gpt-4o |
| I'd like a risk assessment for this project | 1 | GUIDANCE | `risk_assessment` | 0.85 | openai:gpt-4o |
| I'd like a risk assessment for this project | 2 | GUIDANCE | `risk_assessment` | 0.85 | openai:gpt-4o |
| I'd like a risk assessment for this project | 3 | GUIDANCE | `risk_assessment` | 0.85 | openai:gpt-4o |
| I'd like a risk assessment for this project | 4 | GUIDANCE | `risk_assessment` | 0.85 | openai:gpt-4o |
| I'd like a risk assessment for this project | 5 | GUIDANCE | `risk_assessment` | 0.85 | openai:gpt-4o |
| can you run an impact analysis on this change | 1 | ANALYSIS | `impact_analysis` | 0.85 | openai:gpt-4o |
| can you run an impact analysis on this change | 2 | ANALYSIS | `impact_analysis` | 0.85 | openai:gpt-4o |
| can you run an impact analysis on this change | 3 | ANALYSIS | `impact_analysis` | 0.85 | openai:gpt-4o |
| can you run an impact analysis on this change | 4 | ANALYSIS | `impact_analysis` | 0.85 | openai:gpt-4o |
| can you run an impact analysis on this change | 5 | ANALYSIS | `impact_analysis` | 0.85 | openai:gpt-4o |
| is there a bottleneck analysis available | 1 | QUERY | `get_information` | 0.85 | openai:gpt-4o |
| is there a bottleneck analysis available | 2 | QUERY | `get_information` | 0.8 | openai:gpt-4o |
| is there a bottleneck analysis available | 3 | QUERY | `get_information` | 0.85 | openai:gpt-4o |
| is there a bottleneck analysis available | 4 | QUERY | `get_information` | 0.85 | openai:gpt-4o |
| is there a bottleneck analysis available | 5 | QUERY | `get_information` | 0.85 | openai:gpt-4o |
| what risks does this project have | 1 | STRATEGY | `risk_assessment` | 0.85 | openai:gpt-4o |
| what risks does this project have | 2 | STRATEGY | `risk_assessment` | 0.85 | openai:gpt-4o |
| what risks does this project have | 3 | STRATEGY | `risk_assessment` | 0.85 | openai:gpt-4o |
| what risks does this project have | 4 | STRATEGY | `risk_assessment` | 0.85 | openai:gpt-4o |
| what risks does this project have | 5 | STRATEGY | `risk_assessment` | 0.85 | openai:gpt-4o |
| what risk do we have in this plan | 1 | STRATEGY | `risk_assessment` | 0.85 | openai:gpt-4o |
| what risk do we have in this plan | 2 | STRATEGY | `risk_assessment` | 0.85 | openai:gpt-4o |
| what risk do we have in this plan | 3 | STRATEGY | `risk_assessment` | 0.85 | openai:gpt-4o |
| what risk do we have in this plan | 4 | GUIDANCE | `risk_assessment_guidance` | 0.85 | openai:gpt-4o |
| what risk do we have in this plan | 5 | STRATEGY | `risk_assessment` | 0.85 | openai:gpt-4o |
| please identify the risks in this plan | 1 | GUIDANCE | `identify_risks` | 0.85 | openai:gpt-4o |
| please identify the risks in this plan | 2 | GUIDANCE | `identify_risks` | 0.85 | openai:gpt-4o |
| please identify the risks in this plan | 3 | GUIDANCE | `risk_identification` | 0.85 | openai:gpt-4o |
| please identify the risks in this plan | 4 | GUIDANCE | `risk_identification` | 0.85 | openai:gpt-4o |
| please identify the risks in this plan | 5 | GUIDANCE | `risk_assessment` | 0.85 | openai:gpt-4o |
| risks we should flag before launch | 1 | STRATEGY | `identify_risk` | 0.85 | openai:gpt-4o |
| risks we should flag before launch | 2 | GUIDANCE | `prioritize` | 0.85 | openai:gpt-4o |
| risks we should flag before launch | 3 | GUIDANCE | `prioritize` | 0.85 | openai:gpt-4o |
| risks we should flag before launch | 4 | STRATEGY | `flag_risks` | 0.85 | openai:gpt-4o |
| risks we should flag before launch | 5 | STRATEGY | `prioritize` | 0.85 | openai:gpt-4o |
| threats to our timeline this week | 1 | STRATEGY | `identify_risks` | 0.85 | openai:gpt-4o |
| threats to our timeline this week | 2 | STRATEGY | `risk_assessment` | 0.85 | openai:gpt-4o |
| threats to our timeline this week | 3 | STRATEGY | `risk_assessment` | 0.85 | openai:gpt-4o |
| threats to our timeline this week | 4 | STRATEGY | `identify_risks` | 0.85 | openai:gpt-4o |
| threats to our timeline this week | 5 | STRATEGY | `identify_risks` | 0.85 | openai:gpt-4o |
| what could threaten this deadline | 1 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| what could threaten this deadline | 2 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| what could threaten this deadline | 3 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| what could threaten this deadline | 4 | GUIDANCE | `risk_assessment_guidance` | 0.85 | openai:gpt-4o |
| what could threaten this deadline | 5 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| why won't you create issues for me | 1 | EXECUTION | `create_issue` | 0.85 | openai:gpt-4o |
| why won't you create issues for me | 2 | EXECUTION | `create_issue` | 0.85 | openai:gpt-4o |
| why won't you create issues for me | 3 | EXECUTION | `create_issue` | 0.85 | openai:gpt-4o |
| why won't you create issues for me | 4 | EXECUTION | `create_issue` | 0.85 | openai:gpt-4o |
| why won't you create issues for me | 5 | EXECUTION | `create_issue` | 0.85 | openai:gpt-4o |
| why don't you just do it yourself | 1 | CONVERSATION | `clarification_needed` | 0.7 | openai:gpt-4o |
| why don't you just do it yourself | 2 | CONVERSATION | `clarification_needed` | 0.7 | openai:gpt-4o |
| why don't you just do it yourself | 3 | CONVERSATION | `clarification_needed` | 0.7 | openai:gpt-4o |
| why don't you just do it yourself | 4 | CONVERSATION | `clarification_needed` | 0.7 | openai:gpt-4o |
| why don't you just do it yourself | 5 | CONVERSATION | `clarification_needed` | 0.7 | openai:gpt-4o |
| why are you always cautious about this suggestion | 1 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| why are you always cautious about this suggestion | 2 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| why are you always cautious about this suggestion | 3 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| why are you always cautious about this suggestion | 4 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| why are you always cautious about this suggestion | 5 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| what can't you do here | 1 | IDENTITY | `describe_capabilities` | 0.9 | openai:gpt-4o |
| what can't you do here | 2 | IDENTITY | `describe_limitations` | 0.9 | openai:gpt-4o |
| what can't you do here | 3 | IDENTITY | `get_capabilities` | 0.9 | openai:gpt-4o |
| what can't you do here | 4 | IDENTITY | `get_capabilities` | 0.9 | openai:gpt-4o |
| what can't you do here | 5 | IDENTITY | `get_capabilities` | 0.9 | openai:gpt-4o |
| what are your limits as an assistant | 1 | IDENTITY | `describe_capabilities` | 0.9 | openai:gpt-4o |
| what are your limits as an assistant | 2 | IDENTITY | `describe_capabilities` | 0.9 | openai:gpt-4o |
| what are your limits as an assistant | 3 | IDENTITY | `describe_capabilities` | 0.9 | openai:gpt-4o |
| what are your limits as an assistant | 4 | IDENTITY | `describe_capabilities` | 0.9 | openai:gpt-4o |
| what are your limits as an assistant | 5 | IDENTITY | `describe_capabilities` | 0.9 | openai:gpt-4o |
| what's the capability boundary here | 1 | IDENTITY | `get_capabilities` | 0.85 | openai:gpt-4o |
| what's the capability boundary here | 2 | IDENTITY | `get_capabilities` | 0.85 | openai:gpt-4o |
| what's the capability boundary here | 3 | IDENTITY | `get_capability_boundary` | 0.85 | openai:gpt-4o |
| what's the capability boundary here | 4 | IDENTITY | `get_capability_boundary` | 0.8 | openai:gpt-4o |
| what's the capability boundary here | 5 | IDENTITY | `capability_boundary` | 0.85 | openai:gpt-4o |
| how well do you know me by now | 1 | IDENTITY | `get_user_knowledge` | 0.85 | openai:gpt-4o |
| how well do you know me by now | 2 | IDENTITY | `get_identity_knowledge` | 0.85 | openai:gpt-4o |
| how well do you know me by now | 3 | IDENTITY | `self_assessment` | 0.85 | openai:gpt-4o |
| how well do you know me by now | 4 | IDENTITY | `get_knowledge_level` | 0.85 | openai:gpt-4o |
| how well do you know me by now | 5 | IDENTITY | `get_relationship_status` | 0.85 | openai:gpt-4o |
| do you trust me with this decision | 1 | CONVERSATION | `clarification_needed` | 0.7 | openai:gpt-4o |
| do you trust me with this decision | 2 | CONVERSATION | `clarification_needed` | 0.7 | openai:gpt-4o |
| do you trust me with this decision | 3 | CONVERSATION | `clarification_needed` | 0.7 | openai:gpt-4o |
| do you trust me with this decision | 4 | CONVERSATION | `clarification_needed` | 0.7 | openai:gpt-4o |
| do you trust me with this decision | 5 | CONVERSATION | `clarification_needed` | 0.7 | openai:gpt-4o |
| how much do you trust my judgment | 1 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| how much do you trust my judgment | 2 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| how much do you trust my judgment | 3 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| how much do you trust my judgment | 4 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| how much do you trust my judgment | 5 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| what's our relationship like these days | 1 | UNKNOWN | `clarification_needed` | 0.6 | openai:gpt-4o |
| what's our relationship like these days | 2 | QUERY | `get_information` | 0.7 | openai:gpt-4o |
| what's our relationship like these days | 3 | UNKNOWN | `clarification_needed` | 0.6 | openai:gpt-4o |
| what's our relationship like these days | 4 | UNKNOWN | `clarification_needed` | 0.6 | openai:gpt-4o |
| what's our relationship like these days | 5 | UNKNOWN | `clarification_needed` | 0.6 | openai:gpt-4o |
| how do you see our relationship evolving | 1 | GUIDANCE | `relationship_guidance` | 0.85 | openai:gpt-4o |
| how do you see our relationship evolving | 2 | GUIDANCE | `relationship_guidance` | 0.85 | openai:gpt-4o |
| how do you see our relationship evolving | 3 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| how do you see our relationship evolving | 4 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| how do you see our relationship evolving | 5 | GUIDANCE | `relationship_guidance` | 0.85 | openai:gpt-4o |
| how do we work together on this project | 1 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| how do we work together on this project | 2 | GUIDANCE | `collaborate_on_project` | 0.85 | openai:gpt-4o |
| how do we work together on this project | 3 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| how do we work together on this project | 4 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| how do we work together on this project | 5 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| why did you go ahead without asking | 1 | UNKNOWN | `clarification_needed` | 0.6 | openai:gpt-4o |
| why did you go ahead without asking | 2 | UNKNOWN | `clarification_needed` | 0.5 | openai:gpt-4o |
| why did you go ahead without asking | 3 | UNKNOWN | `clarification_needed` | 0.6 | openai:gpt-4o |
| why did you go ahead without asking | 4 | UNKNOWN | `clarification_needed` | 0.6 | openai:gpt-4o |
| why did you go ahead without asking | 5 | UNKNOWN | `clarification_needed` | 0.6 | openai:gpt-4o |
| why do you always ask me the same thing | 1 | CONVERSATION | `clarification_needed` | 0.8 | openai:gpt-4o |
| why do you always ask me the same thing | 2 | CONVERSATION | `clarification_needed` | 0.8 | openai:gpt-4o |
| why do you always ask me the same thing | 3 | CONVERSATION | `clarification_needed` | 0.8 | openai:gpt-4o |
| why do you always ask me the same thing | 4 | CONVERSATION | `clarification_needed` | 0.8 | openai:gpt-4o |
| why do you always ask me the same thing | 5 | CONVERSATION | `clarification_needed` | 0.8 | openai:gpt-4o |
| i didn't ask you to do that | 1 | CONVERSATION | `clarification_needed` | 0.8 | openai:gpt-4o |
| i didn't ask you to do that | 2 | CONVERSATION | `clarification_needed` | 0.8 | openai:gpt-4o |
| i didn't ask you to do that | 3 | CONVERSATION | `clarification_needed` | 0.8 | openai:gpt-4o |
| i didn't ask you to do that | 4 | CONVERSATION | `clarification_needed` | 0.8 | openai:gpt-4o |
| i didn't ask you to do that | 5 | CONVERSATION | `clarification_needed` | 0.8 | openai:gpt-4o |
| what can you remember about our last conversation | 1 | IDENTITY | `recall_conversation` | 0.85 | openai:gpt-4o |
| what can you remember about our last conversation | 2 | IDENTITY | `recall_conversation` | 0.85 | openai:gpt-4o |
| what can you remember about our last conversation | 3 | IDENTITY | `recall_conversation` | 0.85 | openai:gpt-4o |
| what can you remember about our last conversation | 4 | IDENTITY | `recall_conversation` | 0.85 | openai:gpt-4o |
| what can you remember about our last conversation | 5 | IDENTITY | `recall_conversation` | 0.85 | openai:gpt-4o |
| do you remember my last project update | 1 | STATUS | `get_project_status` | 0.85 | openai:gpt-4o |
| do you remember my last project update | 2 | STATUS | `get_project_status` | 0.85 | openai:gpt-4o |
| do you remember my last project update | 3 | STATUS | `recall_last_update` | 0.85 | openai:gpt-4o |
| do you remember my last project update | 4 | STATUS | `get_project_status` | 0.85 | openai:gpt-4o |
| do you remember my last project update | 5 | STATUS | `get_project_status` | 0.85 | openai:gpt-4o |
| remember when we shipped the last release? | 1 | QUERY | `get_information` | 0.8 | openai:gpt-4o |
| remember when we shipped the last release? | 2 | QUERY | `get_information` | 0.8 | openai:gpt-4o |
| remember when we shipped the last release? | 3 | QUERY | `get_release_info` | 0.8 | openai:gpt-4o |
| remember when we shipped the last release? | 4 | QUERY | `get_release_info` | 0.8 | openai:gpt-4o |
| remember when we shipped the last release? | 5 | QUERY | `get_information` | 0.8 | openai:gpt-4o |
| can you show my conversation history | 1 | IDENTITY | `show_conversation_history` | 0.9 | openai:gpt-4o |
| can you show my conversation history | 2 | IDENTITY | `show_conversation_history` | 0.9 | openai:gpt-4o |
| can you show my conversation history | 3 | IDENTITY | `get_conversation_history` | 0.9 | openai:gpt-4o |
| can you show my conversation history | 4 | IDENTITY | `show_conversation_history` | 0.9 | openai:gpt-4o |
| can you show my conversation history | 5 | IDENTITY | `show_conversation_history` | 0.9 | openai:gpt-4o |
| our history together has been good | 1 | CONVERSATION | `acknowledge_history` | 0.85 | openai:gpt-4o |
| our history together has been good | 2 | CONVERSATION | `acknowledge_relationship` | 0.85 | openai:gpt-4o |
| our history together has been good | 3 | CONVERSATION | `acknowledgment` | 0.8 | openai:gpt-4o |
| our history together has been good | 4 | CONVERSATION | `acknowledge_history` | 0.8 | openai:gpt-4o |
| our history together has been good | 5 | CONVERSATION | `acknowledgment` | 0.85 | openai:gpt-4o |
| let's look at past conversations we've had | 1 | QUERY | `retrieve_past_conversations` | 0.8 | openai:gpt-4o |
| let's look at past conversations we've had | 2 | QUERY | `retrieve_past_conversations` | 0.8 | openai:gpt-4o |
| let's look at past conversations we've had | 3 | QUERY | `retrieve_past_conversations` | 0.85 | openai:gpt-4o |
| let's look at past conversations we've had | 4 | QUERY | `retrieve_past_conversations` | 0.85 | openai:gpt-4o |
| let's look at past conversations we've had | 5 | QUERY | `retrieve_past_conversations` | 0.85 | openai:gpt-4o |
| pull up my previous messages please | 1 | QUERY | `retrieve_messages` | 0.85 | openai:gpt-4o |
| pull up my previous messages please | 2 | QUERY | `retrieve_messages` | 0.85 | openai:gpt-4o |
| pull up my previous messages please | 3 | QUERY | `retrieve_messages` | 0.85 | openai:gpt-4o |
| pull up my previous messages please | 4 | QUERY | `retrieve_messages` | 0.8 | openai:gpt-4o |
| pull up my previous messages please | 5 | QUERY | `retrieve_messages` | 0.8 | openai:gpt-4o |
| can I see the conversation log | 1 | QUERY | `retrieve_conversation_log` | 0.85 | openai:gpt-4o |
| can I see the conversation log | 2 | QUERY | `retrieve_conversation_log` | 0.8 | openai:gpt-4o |
| can I see the conversation log | 3 | QUERY | `retrieve_conversation_log` | 0.85 | openai:gpt-4o |
| can I see the conversation log | 4 | QUERY | `get_conversation_log` | 0.85 | openai:gpt-4o |
| can I see the conversation log | 5 | QUERY | `retrieve_conversation_log` | 0.8 | openai:gpt-4o |
| find when I mentioned this bug before | 1 | QUERY | `search_conversation_history` | 0.8 | openai:gpt-4o |
| find when I mentioned this bug before | 2 | QUERY | `retrieve_mention_history` | 0.8 | openai:gpt-4o |
| find when I mentioned this bug before | 3 | QUERY | `retrieve_previous_mention` | 0.85 | openai:gpt-4o |
| find when I mentioned this bug before | 4 | QUERY | `retrieve_mention_history` | 0.8 | openai:gpt-4o |
| find when I mentioned this bug before | 5 | QUERY | `search_conversation` | 0.85 | openai:gpt-4o |
| search history for that conversation topic | 1 | QUERY | `search_conversation_history` | 0.85 | openai:gpt-4o |
| search history for that conversation topic | 2 | QUERY | `search_conversation_history` | 0.85 | openai:gpt-4o |
| search history for that conversation topic | 3 | QUERY | `search_conversation_history` | 0.8 | openai:gpt-4o |
| search history for that conversation topic | 4 | QUERY | `search_conversation_history` | 0.85 | openai:gpt-4o |
| search history for that conversation topic | 5 | QUERY | `search_conversation_history` | 0.85 | openai:gpt-4o |
| what did we discuss in our last session | 1 | QUERY | `retrieve_past_discussion` | 0.8 | openai:gpt-4o |
| what did we discuss in our last session | 2 | QUERY | `retrieve_last_discussion` | 0.8 | openai:gpt-4o |
| what did we discuss in our last session | 3 | QUERY | `retrieve_session_summary` | 0.8 | openai:gpt-4o |
| what did we discuss in our last session | 4 | QUERY | `retrieve_discussion_summary` | 0.8 | openai:gpt-4o |
| what did we discuss in our last session | 5 | QUERY | `retrieve_discussion_summary` | 0.8 | openai:gpt-4o |
| what we discussed yesterday was helpful | 1 | CONVERSATION | `acknowledge_helpfulness` | 0.85 | openai:gpt-4o |
| what we discussed yesterday was helpful | 2 | CONVERSATION | `acknowledgment` | 0.8 | openai:gpt-4o |
| what we discussed yesterday was helpful | 3 | CONVERSATION | `acknowledgment` | 0.8 | openai:gpt-4o |
| what we discussed yesterday was helpful | 4 | CONVERSATION | `acknowledgment` | 0.9 | openai:gpt-4o |
| what we discussed yesterday was helpful | 5 | CONVERSATION | `acknowledgment` | 0.9 | openai:gpt-4o |
| how long is your memory exactly | 1 | QUERY | `get_information` | 0.85 | openai:gpt-4o |
| how long is your memory exactly | 2 | QUERY | `get_information` | 0.85 | openai:gpt-4o |
| how long is your memory exactly | 3 | QUERY | `get_information` | 0.85 | openai:gpt-4o |
| how long is your memory exactly | 4 | QUERY | `get_information` | 0.85 | openai:gpt-4o |
| how long is your memory exactly | 5 | QUERY | `get_information` | 0.85 | openai:gpt-4o |

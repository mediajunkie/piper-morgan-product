# Inversion Phase 3 — surface-2 floor probe

Run 2026-10-02 18:51Z · 5 sample(s) per phrase · LAYER (m-43): `IntentClassifier._classify_with_reasoning` only (surface 1 bypassed, no session context, dev keychain key). Read by `scripts/inversion_phase3_deletion_gate.py` (SURFACE2_FLOOR_PROBES) to credit a category-reached row whose pattern the router does not replace: the row is OK to lose its pattern when EVERY sample lands in the expected action's own category.

served (#1620, resolved per call): openai:gpt-4o

| phrase | sample | surface-2 category | surface-2 action | confidence | served |
|---|---|---|---|---|---|
| I need to setup my projects | 1 | EXECUTION | `setup_projects` | 0.85 | openai:gpt-4o |
| I need to setup my projects | 2 | EXECUTION | `setup_projects` | 0.85 | openai:gpt-4o |
| I need to setup my projects | 3 | EXECUTION | `setup_projects` | 0.85 | openai:gpt-4o |
| I need to setup my projects | 4 | EXECUTION | `setup_projects` | 0.85 | openai:gpt-4o |
| I need to setup my projects | 5 | EXECUTION | `setup_projects` | 0.85 | openai:gpt-4o |
| I want to set up my projects | 1 | EXECUTION | `setup_projects` | 0.85 | openai:gpt-4o |
| I want to set up my projects | 2 | EXECUTION | `setup_projects` | 0.85 | openai:gpt-4o |
| I want to set up my projects | 3 | EXECUTION | `setup_projects` | 0.9 | openai:gpt-4o |
| I want to set up my projects | 4 | EXECUTION | `setup_project` | 0.85 | openai:gpt-4o |
| I want to set up my projects | 5 | EXECUTION | `setup_projects` | 0.85 | openai:gpt-4o |
| I'd like to set up my portfolio | 1 | EXECUTION | `setup_portfolio` | 0.85 | openai:gpt-4o |
| I'd like to set up my portfolio | 2 | EXECUTION | `setup_portfolio` | 0.85 | openai:gpt-4o |
| I'd like to set up my portfolio | 3 | EXECUTION | `setup_portfolio` | 0.85 | openai:gpt-4o |
| I'd like to set up my portfolio | 4 | EXECUTION | `setup_portfolio` | 0.85 | openai:gpt-4o |
| I'd like to set up my portfolio | 5 | EXECUTION | `setup_portfolio` | 0.85 | openai:gpt-4o |
| advise me on this decision | 1 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| advise me on this decision | 2 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| advise me on this decision | 3 | GUIDANCE | `provide_advice` | 0.85 | openai:gpt-4o |
| advise me on this decision | 4 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| advise me on this decision | 5 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| any update on the next milestone | 1 | STATUS | `get_milestone_update` | 0.85 | openai:gpt-4o |
| any update on the next milestone | 2 | STATUS | `get_milestone_update` | 0.85 | openai:gpt-4o |
| any update on the next milestone | 3 | STATUS | `get_milestone_status` | 0.85 | openai:gpt-4o |
| any update on the next milestone | 4 | STATUS | `get_milestone_update` | 0.85 | openai:gpt-4o |
| any update on the next milestone | 5 | QUERY | `get_milestone_update` | 0.8 | openai:gpt-4o |
| can you help me configure the connector | 1 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| can you help me configure the connector | 2 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| can you help me configure the connector | 3 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| can you help me configure the connector | 4 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| can you help me configure the connector | 5 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| can you help me set up the integration | 1 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| can you help me set up the integration | 2 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| can you help me set up the integration | 3 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| can you help me set up the integration | 4 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| can you help me set up the integration | 5 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| can you help me setup the integration | 1 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| can you help me setup the integration | 2 | GUIDANCE | `integration_setup_guidance` | 0.85 | openai:gpt-4o |
| can you help me setup the integration | 3 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| can you help me setup the integration | 4 | GUIDANCE | `integration_setup_guidance` | 0.85 | openai:gpt-4o |
| can you help me setup the integration | 5 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| can you summarize my current work | 1 | STATUS | `summarize_current_work` | 0.9 | openai:gpt-4o |
| can you summarize my current work | 2 | STATUS | `summarize_current_work` | 0.9 | openai:gpt-4o |
| can you summarize my current work | 3 | STATUS | `summarize_current_work` | 0.9 | openai:gpt-4o |
| can you summarize my current work | 4 | STATUS | `summarize_current_work` | 0.9 | openai:gpt-4o |
| can you summarize my current work | 5 | STATUS | `summarize_current_work` | 0.9 | openai:gpt-4o |
| give me a progress update | 1 | STATUS | `get_progress_update` | 0.95 | openai:gpt-4o |
| give me a progress update | 2 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| give me a progress update | 3 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| give me a progress update | 4 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| give me a progress update | 5 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| give me a project overview | 1 | QUERY | `get_project_overview` | 0.85 | openai:gpt-4o |
| give me a project overview | 2 | QUERY | `manage_portfolio` | 0.85 | openai:gpt-4o |
| give me a project overview | 3 | QUERY | `manage_portfolio` | 0.8 | openai:gpt-4o |
| give me a project overview | 4 | QUERY | `get_project_overview` | 0.85 | openai:gpt-4o |
| give me a project overview | 5 | QUERY | `manage_portfolio` | 0.85 | openai:gpt-4o |
| give me a status update | 1 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| give me a status update | 2 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| give me a status update | 3 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| give me a status update | 4 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| give me a status update | 5 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| how do I configure my projects | 1 | GUIDANCE | `configure_projects` | 0.9 | openai:gpt-4o |
| how do I configure my projects | 2 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| how do I configure my projects | 3 | GUIDANCE | `configure_projects` | 0.9 | openai:gpt-4o |
| how do I configure my projects | 4 | GUIDANCE | `configure_projects` | 0.9 | openai:gpt-4o |
| how do I configure my projects | 5 | GUIDANCE | `configure_projects` | 0.9 | openai:gpt-4o |
| how do I configure the connector | 1 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| how do I configure the connector | 2 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| how do I configure the connector | 3 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| how do I configure the connector | 4 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| how do I configure the connector | 5 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| how do I get started? | 1 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| how do I get started? | 2 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| how do I get started? | 3 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| how do I get started? | 4 | GUIDANCE | `provide_guidance` | 0.85 | openai:gpt-4o |
| how do I get started? | 5 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| how do I set up the connector | 1 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| how do I set up the connector | 2 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| how do I set up the connector | 3 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| how do I set up the connector | 4 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| how do I set up the connector | 5 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| how do I setup the connector | 1 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| how do I setup the connector | 2 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| how do I setup the connector | 3 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| how do I setup the connector | 4 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| how do I setup the connector | 5 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| how's the progress going | 1 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| how's the progress going | 2 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| how's the progress going | 3 | STATUS | `get_progress_status` | 0.9 | openai:gpt-4o |
| how's the progress going | 4 | STATUS | `get_progress_status` | 0.9 | openai:gpt-4o |
| how's the progress going | 5 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| list my active projects for this quarter | 1 | STATUS | `list_active_projects` | 0.9 | openai:gpt-4o |
| list my active projects for this quarter | 2 | STATUS | `list_active_projects` | 0.9 | openai:gpt-4o |
| list my active projects for this quarter | 3 | QUERY | `manage_portfolio` | 0.85 | openai:gpt-4o |
| list my active projects for this quarter | 4 | STATUS | `list_active_projects` | 0.9 | openai:gpt-4o |
| list my active projects for this quarter | 5 | STATUS | `list_active_projects` | 0.9 | openai:gpt-4o |
| show me my portfolio | 1 | IDENTITY | `show_portfolio` | 0.9 | openai:gpt-4o |
| show me my portfolio | 2 | QUERY | `manage_portfolio` | 0.85 | openai:gpt-4o |
| show me my portfolio | 3 | IDENTITY | `show_portfolio` | 0.9 | openai:gpt-4o |
| show me my portfolio | 4 | IDENTITY | `show_portfolio` | 0.9 | openai:gpt-4o |
| show me my portfolio | 5 | IDENTITY | `manage_portfolio` | 0.85 | openai:gpt-4o |
| show the current status | 1 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| show the current status | 2 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| show the current status | 3 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| show the current status | 4 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| show the current status | 5 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| what are my active projects | 1 | STATUS | `list_active_projects` | 0.95 | openai:gpt-4o |
| what are my active projects | 2 | STATUS | `list_active_projects` | 0.95 | openai:gpt-4o |
| what are my active projects | 3 | STATUS | `list_active_projects` | 0.95 | openai:gpt-4o |
| what are my active projects | 4 | STATUS | `list_active_projects` | 0.95 | openai:gpt-4o |
| what are my active projects | 5 | STATUS | `get_active_projects` | 0.95 | openai:gpt-4o |
| what are my current projects | 1 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what are my current projects | 2 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what are my current projects | 3 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what are my current projects | 4 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what are my current projects | 5 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| what are my projects? | 1 | STATUS | `list_user_projects` | 0.9 | openai:gpt-4o |
| what are my projects? | 2 | STATUS | `list_projects` | 0.9 | openai:gpt-4o |
| what are my projects? | 3 | STATUS | `list_user_projects` | 0.9 | openai:gpt-4o |
| what are my projects? | 4 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| what are my projects? | 5 | IDENTITY | `list_user_projects` | 0.9 | openai:gpt-4o |
| what are the next steps | 1 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| what are the next steps | 2 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| what are the next steps | 3 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| what are the next steps | 4 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| what are the next steps | 5 | GUIDANCE | `provide_guidance` | 0.8 | openai:gpt-4o |
| what is my status | 1 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what is my status | 2 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what is my status | 3 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what is my status | 4 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what is my status | 5 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what projects am I working on | 1 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what projects am I working on | 2 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what projects am I working on | 3 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what projects am I working on | 4 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what projects am I working on | 5 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what should I do about this bug | 1 | GUIDANCE | `bug_resolution_guidance` | 0.9 | openai:gpt-4o |
| what should I do about this bug | 2 | GUIDANCE | `bug_handling_guidance` | 0.9 | openai:gpt-4o |
| what should I do about this bug | 3 | GUIDANCE | `bug_handling_advice` | 0.85 | openai:gpt-4o |
| what should I do about this bug | 4 | GUIDANCE | `bug_handling_advice` | 0.85 | openai:gpt-4o |
| what should I do about this bug | 5 | GUIDANCE | `prioritize` | 0.85 | openai:gpt-4o |
| what's my current project | 1 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's my current project | 2 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's my current project | 3 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's my current project | 4 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's my current project | 5 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's my progress | 1 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's my progress | 2 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's my progress | 3 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's my progress | 4 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's my progress | 5 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| what's my status | 1 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's my status | 2 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's my status | 3 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's my status | 4 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's my status | 5 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's my work status | 1 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's my work status | 2 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's my work status | 3 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's my work status | 4 | STATUS | `get_work_status` | 0.95 | openai:gpt-4o |
| what's my work status | 5 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's the current progress | 1 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's the current progress | 2 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's the current progress | 3 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| what's the current progress | 4 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's the current progress | 5 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| what's the current status | 1 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's the current status | 2 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| what's the current status | 3 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| what's the current status | 4 | STATUS | `get_project_status` | 0.95 | openai:gpt-4o |
| what's the current status | 5 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| what's the process for filing a bug | 1 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| what's the process for filing a bug | 2 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| what's the process for filing a bug | 3 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| what's the process for filing a bug | 4 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| what's the process for filing a bug | 5 | GUIDANCE | `provide_guidance` | 0.9 | openai:gpt-4o |
| what's the progress looking like | 1 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| what's the progress looking like | 2 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| what's the progress looking like | 3 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| what's the progress looking like | 4 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| what's the progress looking like | 5 | STATUS | `get_project_status` | 0.9 | openai:gpt-4o |
| what's the progress on this | 1 | STATUS | `get_project_status` | 0.85 | openai:gpt-4o |
| what's the progress on this | 2 | STATUS | `get_project_status` | 0.85 | openai:gpt-4o |
| what's the progress on this | 3 | STATUS | `get_project_status` | 0.85 | openai:gpt-4o |
| what's the progress on this | 4 | STATUS | `get_project_status` | 0.85 | openai:gpt-4o |
| what's the progress on this | 5 | STATUS | `get_project_status` | 0.85 | openai:gpt-4o |
| what's the project landscape | 1 | QUERY | `manage_portfolio` | 0.8 | openai:gpt-4o |
| what's the project landscape | 2 | QUERY | `manage_portfolio` | 0.8 | openai:gpt-4o |
| what's the project landscape | 3 | QUERY | `get_information` | 0.8 | openai:gpt-4o |
| what's the project landscape | 4 | QUERY | `manage_portfolio` | 0.8 | openai:gpt-4o |
| what's the project landscape | 5 | QUERY | `manage_portfolio` | 0.8 | openai:gpt-4o |
| what's the task status | 1 | STATUS | `get_task_status` | 0.9 | openai:gpt-4o |
| what's the task status | 2 | STATUS | `get_task_status` | 0.9 | openai:gpt-4o |
| what's the task status | 3 | STATUS | `get_task_status` | 0.9 | openai:gpt-4o |
| what's the task status | 4 | STATUS | `get_task_status` | 0.9 | openai:gpt-4o |
| what's the task status | 5 | STATUS | `get_task_status` | 0.9 | openai:gpt-4o |
| where should I focus this week | 1 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| where should I focus this week | 2 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| where should I focus this week | 3 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| where should I focus this week | 4 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |
| where should I focus this week | 5 | PRIORITY | `prioritize` | 0.95 | openai:gpt-4o |

# Constitution - Providence MCP + CI/CD Demo

## Principle 1 - Existing Resources First

The demo should reuse documented Providence demo resources before creating new Azure infrastructure. New resources require explicit approval and must be documented in the deployment plan.

## Principle 2 - No PHI In The Repo

All datasets are synthetic. No patient names, real MRNs, real dates of birth, phone numbers, emails, clinical notes, or secrets belong in source control.

## Principle 3 - GitHub Is The Change Boundary

The demo must show GitHub as the control point for development changes. A change should be reviewable, testable, and gated through Actions.

## Principle 4 - Evaluations Are Release Gates

Evaluators are not a side report. They decide whether a change can move from dev to test. Production always requires a separate operational approval.

## Principle 5 - MCP Provides Controlled Context

The assistant should not invent environment, policy, or patient-scenario facts. It gets context through explicit MCP tools, and evaluator output should show which tools were used.

## Principle 6 - Demo Must Be Safe To Run Live

The default path must run locally without live Azure calls. Live Foundry calls can be enabled only after tenant auth and model deployment are confirmed.
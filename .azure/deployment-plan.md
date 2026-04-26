# Azure Deployment Plan

Status: Prepared - Local Demo Validated; Live Azure Blocked By Tenant Auth

## 1. Goal

Prepare a Providence MCP and Microsoft Foundry demo that can be reviewed locally before any GitHub push or Azure deployment execution.

## 2. Source Inputs

- Meeting notes: `Session-5-meeting-notes.txt`
- Azure resource inventory: `azure-resources.docx`
- Reference repo: `providence-model-evaluation`

## 3. Architecture Decisions

- Use placeholder public-demo Azure values in repo files. Keep customer-specific resource IDs in private operator notes or local `.env` only.
- Use an existing Foundry account, project, APIM instance, and App Insights resource as the documented live target after RBAC and tenant auth are confirmed.
- First reviewable demo uses a local deterministic path and creates no Azure resources.

## 4. Planned Artifacts

- `spec-kit/` markdown specifications and workflow artifacts
- `skills/` markdown skill/workflow artifacts
- `Demo-mapping.md`
- End-to-end demo source code and docs

## 5. Execution Plan

- Analyze meeting notes and Azure resource document.
- Map the ask to demo capabilities.
- Create learning docs for spec-kit and skills concepts.
- Build a local, reviewable end-to-end demo using the selected Azure/Foundry configuration.
- Validate locally before any GitHub push.

## 6. Validation Plan

- Run local demo smoke test.
- Run unit tests for evaluator behavior.
- Run intentional failure simulation to prove CI gate blocks unsafe changes.
- Record Azure live validation separately after tenant auth is corrected.

## 7. Validation Proof

- `python demo/run_demo.py` completed successfully and generated demo outputs.
- `python -m unittest discover -s tests` ran 2 tests successfully.
- `python demo/run_demo.py --simulate-failure --ci --fail-on-gate` produced `BLOCK_IN_DEV` and the expected CI-blocking exit code.

## 8. Deployment Notes

- No GitHub push until Jay approves after code review.
- No destructive Azure operations without explicit confirmation.
# Tasks - Providence MCP + CI/CD Foundry Demo

## Completed In This Build

- [x] Read meeting notes and capture explicit demo asks.
- [x] Extract Azure resource values from `azure-resources.docx`.
- [x] Create `.azure/deployment-plan.md` draft.
- [x] Create spec-kit learning and planning artifacts.
- [x] Create skills learning docs and demo skill definitions.
- [x] Create `Demo-mapping.md`.
- [x] Build local MCP-style context server and client.
- [x] Build deterministic Providence assistant response generator.
- [x] Build custom evaluator gate.
- [x] Create GitHub Actions workflow.

## Review Tasks For Jay

- [ ] Run `python demo/run_demo.py`.
- [ ] Open generated `eval-outputs/github-actions-summary.md`.
- [ ] Run the failing simulation and confirm the gate behavior.
- [ ] Decide whether the new GitHub repo should be public or private.
- [ ] Fix Azure tenant auth before any live Foundry call.
- [ ] Approve GitHub repo creation and push.

## Later Live-Azure Tasks

- [ ] Switch Azure auth to the tenant that owns the target subscription.
- [ ] Confirm model deployments in the target Foundry account.
- [ ] Configure GitHub OIDC federation for the new repo.
- [ ] Add repo secrets or variables for Azure and Foundry values.
- [ ] Run GitHub Actions against live Foundry outputs.
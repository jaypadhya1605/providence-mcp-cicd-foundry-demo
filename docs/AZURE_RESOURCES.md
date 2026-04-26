# Azure Resources Used For This Demo

Source: private Azure resource inventory, not committed to the public repo.

## Resource Inventory

| Resource | Value |
|---|---|
| Subscription ID | `00000000-0000-0000-0000-000000000000` |
| Resource group | `rg-healthcare-foundry-demo` |
| Foundry account | `ai-healthcare-foundry-demo` |
| Foundry project | `proj-healthcare-foundry-demo` |
| Foundry project endpoint | `https://ai-healthcare-foundry-demo.services.ai.azure.com/api/projects/proj-healthcare-foundry-demo` |
| Region | `eastus2` for the main Foundry account |
| Content Understanding / secondary Foundry note | `cu-healthcare-foundry-demo` in `westus` |
| API Management | `apim-healthcare-foundry-demo` |
| Application Insights | `appi-healthcare-foundry-demo` |
| Log Analytics workspace | `law-healthcare-foundry-demo` |

The private inventory may contain environment-specific values such as Application Insights connection details. Do not commit those values. For a public or customer-shared repo, prefer `APPLICATIONINSIGHTS_CONNECTION_STRING` through environment variables or GitHub Actions secrets.

## Current Azure Auth Finding

Live Azure lookup was attempted through Azure MCP for:

- Foundry model deployments
- Foundry agents
- Foundry evaluator catalog

The local deterministic demo path should be used until Azure tenant auth, RBAC, and model deployment names are confirmed. Once auth is corrected, the same config shape can be used to list model deployments, run live Foundry evaluations, and connect GitHub Actions through OIDC.

## Live Activation Checklist

1. Switch Azure extension auth to the tenant that owns the target subscription.
2. Confirm the intended subscription appears in the selected account.
3. List deployments for the target Foundry account.
4. Fill `FOUNDRY_MODEL_DEPLOYMENT_NAME` in `.env`.
5. Install optional packages from [requirements-live.txt](../requirements-live.txt).
6. Set `LIVE_FOUNDRY_ENABLED=true` and replace the deterministic assistant call with the live Foundry response path in [demo/agent.py](../demo/agent.py).
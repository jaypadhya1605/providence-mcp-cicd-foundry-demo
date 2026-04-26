# Live Foundry Path

The committed demo runs locally by default. That is intentional for Monday: it proves the workflow and avoids surprise tenant or quota issues during the call.

To convert the demo from deterministic local responses to live Foundry responses:

1. Fix Azure tenant auth as described in [AZURE_RESOURCES.md](AZURE_RESOURCES.md).
2. Copy [.env.template](../.env.template) to `.env`.
3. Fill `FOUNDRY_MODEL_DEPLOYMENT_NAME` after listing deployments in the Foundry account.
4. Install optional live packages:

   ```powershell
   pip install -r requirements-live.txt
   ```

5. Keep evaluator logic unchanged. Only the response generator changes from deterministic local output to live Foundry model or agent output.

## Why The Evaluators Stay The Same

The custom evaluator contract scores a dataset item and a response. It does not care whether the response came from:

- a local deterministic assistant,
- a Foundry model deployment,
- a Foundry prompt agent,
- a hosted agent exposed through the Foundry Responses API,
- or an APIM AI Gateway route.

That separation is the key CI/CD message: the delivery gate evaluates behavior, not implementation details.
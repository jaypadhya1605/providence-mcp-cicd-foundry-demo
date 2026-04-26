# Demo Script

## Opening

"Providence asked us to combine MCP and CI/CD into one operating model. I am going to start where a developer or product owner sees it first: an Azure AI Foundry agent connected to MCP tools. Then I will open the code and show how the same MCP server/client pattern feeds the agent and becomes a GitHub Actions promotion gate."

## Demo Steps

1. Start in Azure AI Foundry and open the demo agent.
2. Show the agent tools area and the MCP connections for GitHub and Microsoft Learn.
3. Ask the agent to use Microsoft Learn MCP to summarize Foundry MCP guidance.
4. Ask the agent to use GitHub MCP to inspect `jaypadhya1605/providence-mcp-cicd-foundry-demo` and explain the CI/CD workflow.
5. Open [docs/MCP_FIRST_DEMO_RUNBOOK.md](MCP_FIRST_DEMO_RUNBOOK.md) as the guide for the rest of the walk-through.
6. Open [demo/mcp_server.py](../demo/mcp_server.py) and show where the local MCP tools are defined.
7. Open [demo/mcp_client.py](../demo/mcp_client.py) and show how the agent workflow discovers and calls those tools.
8. Open [demo/run_demo.py](../demo/run_demo.py) and show how MCP context is passed to the agent and evaluator.
9. Open [demo/agent.py](../demo/agent.py) and show `mcp_tools_used` as the proof that tool context shaped the response.
10. Run:

   ```powershell
   python demo/run_demo.py
   ```

11. Open `eval-outputs/demo-run.json` and show MCP tools, response, and evaluation evidence.
12. Open [.github/workflows/providence-mcp-cicd-evaluation.yml](../.github/workflows/providence-mcp-cicd-evaluation.yml) and show dev/test/prod jobs.
13. Run the GitHub Actions success case with `use_case = success`.
14. Run the GitHub Actions failure case with `use_case = failure`.
15. If you need a local backup for the failure case, run:

   ```powershell
   python demo/run_demo.py --simulate-failure --ci --fail-on-gate
   ```

16. Explain that GitHub Actions blocks test/prod promotion when the custom evaluator gate fails.

## Closing

"The important pattern is that Providence can start from a Foundry agent connected to MCP tools, then carry the same tool-grounded behavior into developer code, custom evaluation, and GitHub CI/CD promotion gates."
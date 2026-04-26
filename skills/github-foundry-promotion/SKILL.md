---
name: github-foundry-promotion
description: "Use when explaining GitHub integration with Azure AI Foundry and dev/test/prod promotion for Providence AI apps."
---

# GitHub -> Foundry Promotion

## When To Use

Use this skill when explaining how developers work in dev, how GitHub Actions validates changes, and how downstream teams take over for test and production.

## Procedure

1. Open [.env.template](../../.env.template) and show the Foundry project context.
2. Open [.github/workflows/providence-mcp-cicd-evaluation.yml](../../.github/workflows/providence-mcp-cicd-evaluation.yml).
3. Explain workflow triggers: pull request, push to main, and manual dispatch.
4. Explain OIDC as the production-ready auth pattern for live Azure, while the local demo path avoids secrets.
5. Run `python demo/run_demo.py` and show `promotion-decision.json`.
6. Emphasize that prod is not automatic; it is a controlled handoff after test evidence is available.

## Key Message

GitHub is not just source control in this story. It is the evidence and promotion boundary between developer work and operational ownership.
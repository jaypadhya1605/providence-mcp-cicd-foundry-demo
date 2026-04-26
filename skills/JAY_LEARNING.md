# Jay Learning - Skills

## What Skills Mean

In Copilot or agentic development, a skill is a reusable playbook. It tells the agent:

- when to use the skill,
- what steps to follow,
- which files or references matter,
- what good output looks like.

Think of a skill as a repeatable operating procedure for an AI assistant.

## How Skills Are Discovered

Skills usually live in one of these locations:

- `.github/skills/<skill-name>/SKILL.md` for a team-shared repo skill.
- `.agents/skills/<skill-name>/SKILL.md` for a project-local skill.
- user-level skill folders for personal skills.

This demo uses a root [skills](.) folder because you asked for it explicitly. The skill files here are written in the same style and can be copied into `.github/skills/<name>/SKILL.md` later if you want Copilot to auto-discover them in the new repo.

## What I Did In This Demo

I created three practical skills:

- [providence-mcp-cicd-demo/SKILL.md](providence-mcp-cicd-demo/SKILL.md) - the full runbook for the Monday demo.
- [foundry-evaluation-gate/SKILL.md](foundry-evaluation-gate/SKILL.md) - how to run and reason about evaluator gates.
- [github-foundry-promotion/SKILL.md](github-foundry-promotion/SKILL.md) - how to explain dev -> test -> prod promotion through GitHub.

## Practical Example From This Demo

Without a skill, the prompt is long and easy to forget:

> Read the notes, use Providence resources, run MCP, show CI/CD, run evaluators, explain dev/test/prod, avoid secrets.

With a skill, that becomes a repeatable procedure:

1. Load resource context.
2. Run local demo.
3. Inspect generated outputs.
4. Show GitHub Actions workflow.
5. Demonstrate failure gate.
6. Explain prod handoff.

That sequence is captured in [providence-mcp-cicd-demo/SKILL.md](providence-mcp-cicd-demo/SKILL.md).

## Best Practices To Follow

1. Put strong trigger words in the `description` field.
2. Keep `SKILL.md` short enough to load quickly.
3. Use step-by-step instructions, not vague advice.
4. Keep references near the skill and link with relative paths.
5. Separate human learning docs from machine procedure docs.
6. Do not put secrets or environment-specific credentials in skills.

## How Those Best Practices Were Followed Here

- Skill descriptions include words like Providence, MCP, CI/CD, Foundry, GitHub Actions, evaluator gate, and dev/test/prod.
- Each skill has a focused procedure.
- The files reference local artifacts such as [Demo-mapping.md](../Demo-mapping.md) and [demo/run_demo.py](../demo/run_demo.py).
- Secrets are excluded; Azure values are in `.env.template` and docs only.

## Learning Links

- VS Code Copilot agent skills: https://code.visualstudio.com/docs/copilot/customization/agent-skills
- Copilot customization overview: https://code.visualstudio.com/docs/copilot/copilot-customization
- Spec Kit skills-mode note: https://github.com/github/spec-kit
- Model Context Protocol docs: https://modelcontextprotocol.io/docs
- GitHub Actions docs: https://docs.github.com/actions
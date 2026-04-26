# Jay Learning - Spec Kit

## What Spec Kit Means

Spec Kit is a way to practice spec-driven development. Instead of jumping straight from an idea to code, you create structured artifacts first:

1. Constitution - the principles the project should not violate.
2. Spec - what the feature must do and why it matters.
3. Plan - how the implementation will work technically.
4. Tasks - the execution checklist.
5. Implementation - code built against the spec and tasks.

The point is not bureaucracy. The point is traceability. If someone asks, "Why did we build this?" or "What does this demo prove?", the answer is already written down.

## What I Did In This Demo

I created a lightweight spec-kit folder instead of installing the full Spec Kit CLI, because you asked for markdown files that teach the concept and support this demo immediately.

The folder contains:

- [constitution.md](constitution.md) - rules for the Providence demo, including no PHI, no secrets, and evaluation as a gate.
- [feature-spec.md](feature-spec.md) - the user stories and acceptance criteria from the meeting notes.
- [implementation-plan.md](implementation-plan.md) - the technical approach for MCP context, Foundry config, GitHub Actions, and evaluators.
- [tasks.md](tasks.md) - a task breakdown that maps directly to the code and docs.

## Practical Example From This Demo

Meeting ask:

> Show GitHub integrated with a Foundry project and show dev -> test -> prod through CI/CD.

Spec-kit translation:

- Requirement in [feature-spec.md](feature-spec.md): "The demo must generate a promotion decision with separate dev, test, and prod states."
- Plan in [implementation-plan.md](implementation-plan.md): GitHub Actions runs `python demo/run_demo.py --ci --fail-on-gate`.
- Implementation in [demo/run_demo.py](../demo/run_demo.py): writes `promotion-decision.json`.
- Evidence in generated output: `eval-outputs/github-actions-summary.md`.

That is traceability: ask -> requirement -> plan -> code -> evidence.

## Best Practices To Follow

1. Write the user-visible outcome before choosing the implementation.
2. Keep acceptance criteria testable. Avoid vague lines like "make it better."
3. Record non-negotiables in the constitution, especially security and data rules.
4. Keep tasks small enough that a reviewer can see what changed.
5. Update specs when reality changes. A stale spec is worse than no spec.

## How Those Best Practices Were Followed Here

- The spec starts from Providence's meeting ask, not from a technology shopping list.
- The acceptance criteria include concrete outputs: `demo-run.json`, `promotion-decision.json`, and GitHub summary markdown.
- The constitution explicitly blocks real PHI and secrets in the repo.
- The implementation can run locally without Azure auth, but the Foundry project values are still captured for the live path.
- The current auth blocker is documented instead of hidden.

## Learning Links

- Spec Kit repo: https://github.com/github/spec-kit
- Spec Kit docs: https://github.github.io/spec-kit/
- Spec-driven development overview: https://github.com/github/spec-kit/blob/main/spec-driven.md
- Specify CLI reference: https://github.github.io/spec-kit/reference/overview.html
- Spec Kit supported integrations: https://github.github.io/spec-kit/reference/integrations.html
# Steering — Project Structure

## Repository layout

- `.kiro/` lives at the repository root and is never git-ignored.
- `.kiro/specs/ghostagent-research-workflow/` holds the workflow Spec.
- `.kiro/steering/` holds product, style, structure and tech rules.
- `.kiro/agents/` holds one JSON file per custom agent, named after the agent.
- `docs/` holds human-facing documentation. `examples/` holds frozen sample runs.

## Generated output layout (per topic)

All generated research documents for one topic go under
`output/<topic-slug>/`, where `<topic-slug>` is the kebab-case short form of
the refined topic chosen by `topic-analyst` and recorded in the topic brief:

```text
output/<topic-slug>/
├── topic-brief.md
├── research-spec/
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
├── literature-review-framework.md
├── diagrams.md
└── session-log.md
```

## Naming

- File names are kebab-case Markdown (`.md`); diagrams live inside
  `diagrams.md` as Mermaid blocks, not as image files.
- One topic per output folder. Never mix two topics in one folder.
- The session log is append-only: new entries go at the end with an ISO date.

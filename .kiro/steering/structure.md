# Steering — Project Structure

## Repository layout

- `.kiro/specs/ghostagent-research-workflow/` defines the software workflow, not the student's research.
- `.kiro/steering/` contains shared rules, including the managed workflow protocol.
- `.kiro/agents/` contains a coordinator and four research-stage definitions.
- `ghostagent.py` is the executable state manager. `docs/` contains usage and architecture. `examples/sample-run/` is an illustrative complete snapshot, not evidence of a live Kiro run.

## Per-topic layout

```text
output/<topic-slug>/
├── input.md
├── topic-brief.md
├── research-spec/
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
├── literature-review-framework.md
├── diagrams.md
├── session-log.md
├── .ghostagent-state.json
├── .ghostagent.lock
└── .candidates/<stage>/        # candidate documents, same relative layout
```

`.ghostagent-pending.json` exists only during a recoverable transaction. One topic per folder; use a stable kebab-case slug. Do not rename the topic while agents are working. The generated `output/` directory is ignored by Git. Preserve explicitly frozen examples under `examples/`. Session history is append-only in the state; the manager materializes the corresponding Markdown log. Candidates are working data and are not evidence of stage completion.

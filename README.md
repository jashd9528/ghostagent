# GhostAgent 👻

**An intelligent research assistant built with Kiro — turn a vague thesis idea into a clear, structured research plan.**

GhostAgent is an agentic research workflow that runs inside [Kiro](https://kiro.dev). A student enters one initial research topic, and GhostAgent structures the entire early stage of a graduation thesis: it generates a complete Spec (Requirements → Design → Tasks), builds a literature review framework, produces academic diagrams in Mermaid, and coordinates multiple specialised agents that share one long-term project context.

> This is not just another chatbot. It's a true **Agentic Research Workflow**.

---

## The Problem

When students work on a graduation thesis, the hardest part is rarely writing the main text. It is:

- turning a vague idea into a clear research structure and research questions;
- organising a literature review before knowing the field's structure;
- drawing academic architecture / flow diagrams by hand;
- keeping every output consistent while the topic evolves over weeks.

General-purpose AI chatbots return one paragraph at a time. They do not plan the research process, they do not keep a persistent project structure, and their output format drifts from session to session.

## What GhostAgent Does

| Step | Input | Output |
| --- | --- | --- |
| 1. Topic analysis | One sentence research idea | Refined topic, scope, candidate research questions |
| 2. Spec generation | Refined topic | A complete Spec: `requirements.md`, `design.md`, `tasks.md` |
| 3. Literature review | Research questions | A structured literature review framework (themes, gaps, reading plan) |
| 4. Diagrams | Research design | Academic architecture / flow diagrams in Mermaid |
| 5. Task execution | `tasks.md` | Step-by-step research work products, tracked against the Spec |

All steps are performed by specialised agents working from the same Spec and the same steering documents, so terminology, structure and academic style stay consistent across the whole project.

## How It Is Built with Kiro

GhostAgent is built entirely with Kiro, and all of its configuration lives in the [`.kiro`](.kiro) directory at the repository root — reproducible and extensible.

### 1. Spec-driven development (Kiro Specs)

The entire research workflow is defined as a Kiro Spec in [`.kiro/specs/ghostagent-research-workflow/`](.kiro/specs/ghostagent-research-workflow/):

- **`requirements.md`** — research goals and user stories in EARS format, with acceptance criteria for every workflow stage.
- **`design.md`** — agent architecture, data flow, output document formats, and Mermaid diagrams of the workflow itself.
- **`tasks.md`** — the workflow broken into ordered, checkable implementation tasks that agents execute one by one.

### 2. Steering documents (Kiro Steering)

[`.kiro/steering/`](.kiro/steering/) contains the persistent rules every agent follows:

- **`product.md`** — what GhostAgent is, who it serves, and its core features.
- **`academic-style.md`** — academic writing rules: structure, tone, terminology, citation discipline.
- **`structure.md`** — where every output file goes and how it is named.
- **`tech.md`** — the technical conventions: Markdown + Mermaid only, no external services required.

### 3. Multi-agent collaboration (Kiro custom agents)

Four custom agents are defined in [`.kiro/agents/`](.kiro/agents/), each with a single responsibility:

| Agent | Responsibility |
| --- | --- |
| `topic-analyst` | Refines a raw idea into a scoped topic and research questions |
| `spec-builder` | Generates and maintains the Spec (requirements / design / tasks) |
| `literature-reviewer` | Builds the literature review framework organised by theme and gap |
| `diagram-maker` | Produces Mermaid architecture and flow diagrams for the research design |

Agents hand work to each other through the shared Spec files, which act as the project's long-term memory: any session can resume exactly where the last one stopped.

## Project Structure

```text
ghostagent/
├── .kiro/                              # Kiro configuration (required, at repo root)
│   ├── specs/
│   │   └── ghostagent-research-workflow/
│   │       ├── requirements.md         # Workflow requirements (EARS)
│   │       ├── design.md               # Architecture, data flow, output formats
│   │       └── tasks.md                # Ordered, checkable task list
│   ├── steering/
│   │   ├── product.md                  # Product definition
│   │   ├── academic-style.md           # Academic writing rules
│   │   ├── structure.md                # Output file layout and naming
│   │   └── tech.md                     # Technical conventions
│   └── agents/
│       ├── topic-analyst.json
│       ├── spec-builder.json
│       ├── literature-reviewer.json
│       └── diagram-maker.json
├── docs/
│   ├── ARCHITECTURE.md                 # Detailed architecture and workflow docs
│   └── USER_GUIDE.md                   # Step-by-step guide with examples
├── examples/
│   └── sample-run/                     # One complete sample run (input + outputs)
├── DEVPOST.md                          # Hackathon submission texts
├── LICENSE                             # MIT
└── README.md
```

## Getting Started

**Requirements:** [Kiro IDE](https://kiro.dev) (free). No other accounts, API keys or services are required.

1. Clone this repository.
2. Open the project folder in Kiro. Kiro loads `.kiro/steering/` automatically, and the Spec appears in the Specs panel.
3. Start a chat with the `spec-builder` agent (or any Kiro chat in this workspace) and enter a research topic, for example:

   > *The impact of AI tools on college students' learning habits*

4. GhostAgent runs the workflow: topic analysis → Spec generation → literature review framework → diagrams. Outputs are written to an `output/<topic-slug>/` folder as described in `.kiro/steering/structure.md`.
5. Review each output, adjust the topic or the Spec, and re-run any single step — the Spec keeps the whole project consistent.

A complete worked example is in [`examples/sample-run/`](examples/sample-run/), and the full walkthrough is in [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md).

## Demo

- Demo video: https://youtu.be/F3EKEneyoqA
- The video shows: the problem (0:00), Spec generation (0:10), literature review framework and diagrams (0:20), multi-agent collaboration (0:30), the `.kiro` configuration (0:40), and the closing summary (0:50).

## Why a Spec for Research?

A thesis is a long, structured engineering-like process, but students usually run it from scattered notes. Spec-driven development fixes exactly that:

- **Requirements first** — the research questions are agreed before any writing starts.
- **Design before drafting** — the structure of the review and the study exists on paper before chapters are written.
- **Tasks, not vibes** — progress is a checklist that can be verified, not a feeling.
- **Steering = consistency** — academic style rules are written once and applied by every agent, every session.

## License

MIT — see [LICENSE](LICENSE).

**Built with Kiro.**

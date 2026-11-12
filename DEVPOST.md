# Devpost Submission Texts — GhostAgent

Copy-paste texts for the Kiroween submission form. Replace every
`[bracketed placeholder]` with your real information before submitting.

## Testing instructions or credentials

```
No credentials required.
1. Clone the public GitHub repo and open the project folder in Kiro (free IDE from kiro.dev). All configuration lives in /.kiro at the repo root.
2. In the Specs panel, open ghostagent-research-workflow to see requirements.md, design.md and tasks.md; the Steering panel shows product, academic-style, structure and tech.
3. To run the workflow: start a Kiro chat in this workspace and enter a sample research topic, e.g. "The impact of AI tools on college students' learning habits". The topic-analyst agent produces a topic brief; after you confirm the scope, spec-builder generates a research Spec, literature-reviewer builds the literature review framework, and diagram-maker produces Mermaid diagrams.
4. A complete frozen sample run (input + all outputs) is in examples/sample-run/ if you prefer to inspect results without running anything.
5. Demo video: https://youtu.be/F3EKEneyoqA
```

## How the project meets the main technology requirement (uses Kiro)

```
GhostAgent is built entirely with Kiro.

- Kiro Specs (spec-driven development): The entire research workflow is defined as a Spec in .kiro/specs/ghostagent-research-workflow — requirements.md defines the workflow stages in EARS format with acceptance criteria, design.md defines the agent architecture, data flow and correctness properties, and tasks.md breaks the build into an ordered, checkable task list.
- Kiro Steering: Steering documents in .kiro/steering (product, academic-style, structure, tech) define the product, the academic writing rules — including a hard no-fabricated-citations rule — the output layout and the technical conventions, and are applied to every generated output in every session.
- Kiro custom agents: Four agents in .kiro/agents (topic-analyst, spec-builder, literature-reviewer, diagram-maker) each perform one stage of the research workflow and hand work to each other through the shared Spec files, which act as long-term project memory across sessions.
- Kiro IDE: The project was developed and runs in Kiro, and all configuration lives in the /.kiro directory at the repository root, making the setup reproducible and extensible.
```

## Disclosure of pre-existing code or work

```
GhostAgent was created new for this hackathon. No pre-existing project code was reused. The repository contains Kiro configuration (Specs, steering documents and custom agent definitions), documentation and a sample run, all authored for this project during the hackathon. The only external component is Kiro itself. Demo video narration and subtitles were produced with AI tools during the hackathon.
```

## Repository checklist (verify before submitting)

- [ ] Repository is **public** on GitHub (not GitLab / Bitbucket).
- [ ] `LICENSE` (MIT) is in the root and the license shows in the About section.
- [ ] `/.kiro` is at the repository root and is **not** listed in `.gitignore`.
- [ ] README's demo link points to the real demo video.
- [ ] Submitter country of residence is your actual country.
- [ ] The selected Category matches the project, and the "Best Student
      Project" sponsor prize (if entered) names the same category.

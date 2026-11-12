# Tasks — GhostAgent Research Workflow

Implementation plan for the workflow itself. Each task is executed by the
agent named in brackets and checked against `requirements.md`.

## 1. Configuration foundation

- [x] 1.1 Create the `.kiro` layout at the repository root: `specs/`, `steering/`, `agents/` _(Requirement 5)_
- [x] 1.2 Write `steering/product.md` with the product definition and feature list _(Requirement 5)_
- [x] 1.3 Write `steering/academic-style.md` including the no-fabricated-citations rule and the `[source needed]` marker convention _(Requirements 3, 6)_
- [x] 1.4 Write `steering/structure.md` fixing the per-topic output layout and `<topic-slug>` naming _(Requirement 5)_
- [x] 1.5 Write `steering/tech.md` fixing Markdown + Mermaid as the only output formats _(Requirement 4)_

## 2. Agents

- [x] 2.1 Define `agents/topic-analyst.json`: scope refinement, 3–5 research questions, confirmation gate _(Requirement 1)_
- [x] 2.2 Define `agents/spec-builder.json`: generates the per-topic Research Spec from a confirmed Topic Brief _(Requirement 2)_
- [x] 2.3 Define `agents/literature-reviewer.json`: theme/gap framework + reading plan, citation discipline enforced in its prompt _(Requirements 3, 6)_
- [x] 2.4 Define `agents/diagram-maker.json`: study architecture + procedure diagrams, Mermaid self-validation step _(Requirement 4)_

## 3. Workflow Spec

- [x] 3.1 Write this Spec: `requirements.md` in EARS format with acceptance criteria per stage _(Requirements 1–6)_
- [x] 3.2 Write `design.md` with the architecture diagram, component interfaces, data models and correctness properties P1–P5 _(Requirement 5)_
- [x] 3.3 Maintain this `tasks.md` as the execution checklist; tasks complete only in dependency order (P5)

## 4. Documentation and examples

- [x] 4.1 Write `README.md`: problem, features, Kiro usage write-up, project structure, getting started _(Requirement 5)_
- [x] 4.2 Write `docs/ARCHITECTURE.md` and `docs/USER_GUIDE.md` with the full stage walkthrough _(Requirements 1–4)_
- [x] 4.3 Produce `examples/sample-run/`: one complete frozen run (input, topic brief, framework, diagrams) as the golden example _(Requirements 1, 3, 4)_
- [x] 4.4 Verify the sample run: diagrams render as valid Mermaid; framework contains `[source needed]` markers and no invented citations (P2) _(Requirements 3, 4, 6)_

## 5. Submission readiness

- [x] 5.1 Add the MIT `LICENSE` and confirm it is visible from the repository About section
- [x] 5.2 Confirm `.gitignore` does not ignore `.kiro/` and that the directory sits at the repository root
- [ ] 5.3 Record the demo video from a real run of the workflow and link it in `README.md`
- [ ] 5.4 Final pass: every acceptance criterion in `requirements.md` demonstrated by the sample run or the demo

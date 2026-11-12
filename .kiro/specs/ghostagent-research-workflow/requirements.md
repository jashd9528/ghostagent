# Requirements — GhostAgent Research Workflow

## Introduction

GhostAgent is an agentic research workflow that runs in Kiro. It takes a
student's one-sentence thesis idea and produces, in order: a scoped topic
brief, a research Spec (requirements, design, tasks), a literature review
framework, and academic diagrams in Mermaid. Multiple specialised agents
perform the stages, coordinated through shared Spec files and steering
documents so that output stays consistent across sessions.

## Glossary

- **Topic Brief**: the document that fixes the refined topic, scope and research questions.
- **Research Spec**: the per-topic requirements / design / tasks trio generated for the student's own thesis.
- **Framework**: the literature review framework document, organised by theme and research gap.
- **Steering**: the Markdown rules under `.kiro/steering/` that constrain all generated output.
- **Session Log**: the running record of generated outputs and student edits for one topic.

## Requirements

### Requirement 1 — Topic intake and scoping

**User story:** As a student, I want to enter a rough thesis idea in one
sentence, so that I get back a scoped topic I can actually work on.

#### Acceptance criteria

1. WHEN a student submits a free-text topic idea, THE `topic-analyst` agent SHALL produce a Topic Brief containing a refined topic statement, explicit in-scope and out-of-scope lists, 3–5 research questions, and definitions of key terms.
2. WHEN the Topic Brief is produced, THE workflow SHALL pause for student confirmation before any further stage runs.
3. IF the student edits the scope, THEN THE workflow SHALL update the Topic Brief in place and use the edited version for all later stages.

### Requirement 2 — Research Spec generation

**User story:** As a student, I want my confirmed topic turned into a
requirements / design / tasks Spec, so that my thesis has an agreed structure
before I write anything.

#### Acceptance criteria

1. WHEN a Topic Brief is confirmed, THE `spec-builder` agent SHALL generate a Research Spec containing `requirements.md`, `design.md` and `tasks.md` for the student's topic.
2. THE `design.md` SHALL include a chapter plan and a method outline consistent with the research questions in the Topic Brief.
3. THE `tasks.md` SHALL order tasks so that every task depends only on outputs of earlier tasks, and SHALL express each task as a checkable item.
4. WHEN the student changes the chapter plan in `design.md`, THE workflow SHALL treat the edited Spec as authoritative for all subsequent generation.

### Requirement 3 — Literature review framework

**User story:** As a student, I want a literature review framework organised
by theme and gap, so that I know what to read and how the review will argue.

#### Acceptance criteria

1. WHEN a Research Spec exists, THE `literature-reviewer` agent SHALL produce a Framework whose top-level sections correspond to themes derived from the research questions.
2. FOR each theme, THE Framework SHALL state the main debate, what is established, the open gap, and how the thesis addresses the gap.
3. THE Framework SHALL include a reading plan with search terms and a reading order.
4. THE workflow SHALL NOT invent citations; wherever a source is required but unknown, THE Framework SHALL contain the literal marker `[source needed]`.

### Requirement 4 — Academic diagrams

**User story:** As a student, I want diagrams of my study design and
procedure, so that I can include them in my proposal without drawing tools.

#### Acceptance criteria

1. WHEN a Research Spec design exists, THE `diagram-maker` agent SHALL produce a study architecture diagram and a research procedure flow diagram in Mermaid syntax.
2. EACH diagram SHALL be valid Mermaid that renders without errors in a standard Mermaid renderer.
3. EACH diagram SHALL carry a caption stating what it shows and which Spec section it visualises.

### Requirement 5 — Consistency and long-term context

**User story:** As a student, I want every output to follow the same academic
style and terminology even weeks apart, so that my documents read as one work.

#### Acceptance criteria

1. THE workflow SHALL apply the steering documents in `.kiro/steering/` to every generated output in every session.
2. WHEN a new session starts for an existing topic, THE workflow SHALL resume from the existing Spec and Session Log rather than regenerating from scratch.
3. THE workflow SHALL record every generated or regenerated output in the Session Log with its date and the triggering change.

### Requirement 6 — Academic integrity

**User story:** As a student, I want the tool to structure my research without
fabricating scholarship, so that the work I submit is honestly mine.

#### Acceptance criteria

1. THE workflow SHALL produce plans, structures and frameworks only; it SHALL NOT present generated text as a finished thesis chapter.
2. THE workflow SHALL phrase field claims as guidance to verify, never as sourced facts.
3. IF an agent cannot ground a statement in the Topic Brief, the Spec, or steering, THEN THE agent SHALL mark it as a suggestion or omit it.

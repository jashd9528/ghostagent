# GhostAgent — User Guide

## Who this is for

Students starting a graduation thesis (or a similar long research project) who
have a rough topic idea but no structure yet. You need the free
[Kiro IDE](https://kiro.dev) and this repository — nothing else.

## Setup (2 minutes)

1. Clone this repository, or download it as a ZIP and unzip it.
2. In Kiro, choose **File → Open Folder** and select the project folder.
3. Confirm the configuration loaded: the Specs panel shows
   **ghostagent-research-workflow**, and the Steering panel lists
   `product`, `academic-style`, `structure` and `tech`.

No API keys, accounts or installs are needed.

## Running the workflow

### Step 1 — Enter your topic

Open a Kiro chat in this workspace and write one sentence, for example:

> Help me plan my thesis: the impact of AI tools on college students' learning habits.

The `topic-analyst` agent replies with a **topic brief**: a tightened topic
statement, what is in and out of scope, 3–5 research questions, and key terms.

**Your action:** read the scope. Edit anything wrong ("exclude high-school
students", "focus on self-reported habits, not grades") and confirm.

### Step 2 — Generate the Spec

Ask Kiro to continue (or invoke the `spec-builder` agent). You get a research
Spec for *your* topic:

- `requirements.md` — what the thesis must establish, with acceptance criteria;
- `design.md` — chapter plan, method outline, and the workflow diagram;
- `tasks.md` — the work broken into ordered tasks you can check off.

**Your action:** approve or adjust the chapter plan in `design.md`. Later steps
follow this file, so five minutes here saves hours later.

### Step 3 — Literature review framework

The `literature-reviewer` agent produces a framework organised by theme:
for each theme — the main debate, what is already known, the open gap, and how
your thesis addresses it — plus a reading plan (search terms, databases, order
of reading). Slots that need a real reference are marked `[source needed]`.

**Your action:** work through the reading plan, replace `[source needed]`
markers with sources you have actually read.

### Step 4 — Diagrams

The `diagram-maker` agent writes `diagrams.md` with Mermaid diagrams of your
study design and procedure. Paste any Mermaid block into a Mermaid renderer
(or view it on GitHub) to get the rendered academic diagram for your proposal.

### Step 5 — Work the task list

Open `tasks.md` and work (or ask Kiro to work) task by task. Because every
agent reads the same Spec and steering, outputs stay consistent even across
sessions weeks apart. Progress = checked boxes, and the session log records
what changed.

## Sample run

[`examples/sample-run/`](../examples/sample-run/) contains a complete frozen
run for the topic *"The impact of AI tools on college students' learning
habits"*: the input, topic brief, literature review framework and diagrams.
Compare your first run against it to see the expected shape of each output.

## Tips

- **One topic per workspace folder.** The Spec is the project's memory; mixing
  two theses in one folder mixes their contexts.
- **Change structure in the Spec, not in outputs.** If the chapter plan
  changes, edit `design.md` and regenerate the affected output — never patch
  five files by hand.
- **Keep steering honest.** If your school has a specific citation style, add
  it to `.kiro/steering/academic-style.md` once; every output will follow it.

## FAQ

**Does GhostAgent write my thesis for me?**
No. It plans and structures the research: questions, design, review framework,
diagrams and tasks. The writing — and the responsibility for it — stays with
you. See *Academic integrity rules* in [ARCHITECTURE.md](ARCHITECTURE.md).

**Does it invent references?**
No. Unknown sources are emitted as `[source needed]` on purpose.

**Can I use it for a topic outside the sample's field?**
Yes. The workflow is discipline-neutral; add field-specific terminology to a
steering file if you need tighter guidance.

**What if I only want one stage (e.g. just diagrams)?**
Invoke that single agent (`diagram-maker`) with your existing design text.
Stages are independent by design.

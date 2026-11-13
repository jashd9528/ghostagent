# GhostAgent — User Guide

This guide covers research generation in Kiro and local state management with Python 3.10+. Kiro's own installation and authentication requirements apply.

## Visual frontend

Open `frontend/index.html` directly. Four ready planning stages do not mean the ten research tasks are complete. Sample confirmation is explicitly simulated.

- **Import project:** select exactly one topic folder or multiple Markdown/state files. Files stay local. With state JSON, original-byte hashes and upstream dependencies determine freshness; this is not structural validation. Without state, documents are untracked. Do not select multiple topics.
- **Research Spec:** switch Requirements / Design / Tasks, edit Markdown and save browser drafts. Task checkboxes enforce prerequisites; clearing a task also clears dependent completions. No formal commit occurs until submitted from the connected Workflow page.
- **Literature and diagrams:** browse themes, render all three sample Mermaid diagrams, zoom and export SVG. Editing keeps raw Markdown. Rendering errors are shown with source rather than presented as success.
- **Context:** inspect recorded events, rules and document structure. Draft workspace JSON is an archival export, not a manager state or supported topic import format.
- **New research:** save an idea and export an initialization request JSON. This only records input; initialize and generate research through the existing Python/Kiro workflow.

### Connected workflow mode

Run `python -B workflow_server.py` from the repository root, then open the workspace address printed by the launcher. This mode serves the UI and a local API bound only to loopback. It requires no extra packages. Use `--port` if the default address is occupied. Stop it with Ctrl+C in its terminal.

1. Open **Workflow**, select a topic from the project output directory, or create a new topic using a unique kebab-case identifier and research idea. Creation writes input, manager state and session log, not generated research.
2. The frozen sample is read-only. **Copy sample** creates an independent input and topic brief; it does not copy approval or downstream completion. Prepare later stages manually or through Kiro.
3. Edit drafts in the normal document pages or open **Edit and submit candidate** for any stage. Spec submissions include all three documents; diagrams can be edited here as Mermaid Markdown. Save candidates to browser storage if not ready to submit.
4. Review every candidate, enter a change reason and explicitly submit. The manager validates and publishes the stage, updates events and returns refreshed status. Original protected student-edit contents override candidates. Errors preserve the browser candidate and leave rejected stages unpublished.
5. After topic submission, open **Review and confirm committed topic**, read the actual formal brief and tick the explicit approval checkbox. Confirmation binds its exact hash; it is not automatically granted by copying or opening a topic.
6. Run **Full validation** to inspect errors and warnings. An incomplete research has actionable missing-stage errors. Source-needed and renderer warnings remain visible even on a structural pass.

Refresh preserves pending candidates and their captured fingerprints. If another editor or Kiro changes documents, submission rejects the stale base. Use **Read latest files and compare**, inspect the original text beside each candidate, merge required changes and tick the reconciliation acknowledgement before resubmitting. Do not simply force old content through using a new token. Task checkboxes remain drafts until the full Spec is submitted.

Connected drafts are scoped by topic ID and retain their original stage bases across brief changes. Offline drafts remain scoped by topic and brief hash. Browser persistence depends on storage availability and workspace origin; export important drafts before clearing browser data. Switching topics keeps saved drafts; unfinished modal typing should be saved first. After a timeout, refresh formal state before retrying because publication may already have completed.

The bridge exposes only the frontend assets and configured output topic operations, not arbitrary shell commands or filesystem paths. Same-origin checks and a per-process mutation token restrict browser writes. Kiro generation is available only through the separate explicit generation action described below. It is a single-user local tool, not an authenticated public or multi-user server. Never expose it publicly.

### Generate with Kiro CLI

1. Install a compatible Kiro CLI and configure its headless authentication outside the browser. Start the server in that configured environment. The runtime panel detects CLI availability but an available CLI is not proof of successful authentication.
2. For Windows plus WSL use `python -B workflow_server.py --kiro-wsl Ubuntu-24.04`. The selected distribution must start normally and contain the CLI plus its required credentials. Native installations can use `--kiro-executable` with an executable path. Shell command strings and batch wrappers are not accepted.
3. Open or create a writable topic. Click **Generate with Kiro** on a stage and optionally supply revision requirements. Only formal files are included; browser drafts are not implicitly sent. Dependencies and hash-bound scope approval are enforced before downstream generation.
4. Inspect status and actual stdout/stderr logs. No percent progress is invented. Active-job polling updates both the dashboard indicator and an open log dialog, including its terminal status or error message. Cancel a running job when needed. Jobs time out after 600 seconds by default (`--generation-timeout`, up to 1800). A Kiro request for clarification is shown as needs-input, not success.
5. Open a completed candidate for review. Opening does not overwrite existing drafts or publish files. Saving explicitly replaces that stage's browser draft. Submit with a reason using the existing workflow controls. The captured base stays pinned; changes during generation make the candidate stale and require reconciliation.
6. After a topic candidate is committed, separately review and confirm its exact scope before generating the Spec. Remaining stages likewise require individual review and submission. Source verification remains separate.

Task records and candidate outputs persist in `output/.kiro-jobs/`. After a server restart unfinished jobs become interrupted; completed candidates remain available. The generated CLI agent has no tools/MCP and works in a per-job runtime folder with a supplied snapshot. Global CLI hooks or policies are still part of the user's Kiro environment. Do not use the normal stage agents here: those are for interactive Kiro sessions and include manager-commit instructions. CLI errors and authentication failures are visible; installing the bridge does not install or authenticate Kiro.

### Offline candidate exports

Direct HTML preview still supports local imports, Markdown exports and candidate ZIPs. Each ZIP contains `<stage>/` in manager-relative layout and `candidate-manifest.json` with the captured fingerprint. Review and submit via the manager CLI if not using connected mode. Refresh the embedded sample with `python -B frontend/export_sample.py` after sample changes. Mermaid 10.9.5 remains bundled for offline rendering.

## Setup

Open the repository root in Kiro. Use `research-coordinator` as the entry point. The agent definitions target IDE 1.0 / CLI V3. Check that your Kiro installation loads the JSON and tools before relying on live generation. The local manager requires only Python's standard library.

## Stage 1 — Topic and approval

Provide a subject and population in one sentence. If either is unknown, the agent asks one question. The topic analyst picks a stable kebab-case slug and initializes `output/<slug>` using `init --idea "..."`.

Every command uses this prefix from the repository root:

```sh
python ghostagent.py --topic output/my-topic --json status
```

The JSON gives `next`, `brief_hash` and a `based_on` fingerprint per stage. The agent captures a stage token before generating candidates. Topic candidate: `.candidates/topic/topic-brief.md` inside the topic folder. Required sections are Refined topic statement, Scope, Research questions and Key terms; include In scope and Out of scope lists and 3–5 numbered RQs.

Submit with `commit topic --source output/my-topic/.candidates/topic --based-on <token> --reason "Initial topic"`. Replace placeholders with actual output; do not run them literally. Review the written brief, explicitly confirm or request revisions. Only after approval run `confirm --hash <reviewed-brief-hash>`. The hash prevents confirmation of a changed version. The manager records an assertion, not an authenticated identity.

## Stage 2 — Research Spec

Capture the `spec` token, read the confirmed brief, and prepare all three candidates under `.candidates/spec/research-spec/`:

- `requirements.md`: Requirements section, every RQ and EARS-style SHALL criteria.
- `design.md`: Chapter plan, Method outline, Procedure and a fenced Mermaid flowchart.
- `tasks.md`: Tasks section with `- [ ] T1 ... Depends on: none.` and later tasks referring only to earlier IDs. Completed tasks cannot depend on unfinished tasks.

Use `commit spec --source output/my-topic/.candidates/spec --based-on <token> --reason "Initial Research Spec"`. Review feasibility with a supervisor; a committed plan is not ethics approval.

## Stages 3 and 4 — Review framework and diagrams

Literature candidate: `.candidates/literature/literature-review-framework.md`. Use `## Theme ...` sections covering every RQ. Each theme includes Main debate, Established, Gap and This thesis labels; finish with Reading plan. Hypothetical gaps and all unknown field claims need `[source needed]` and careful verification wording.

Diagram candidate: `.candidates/diagrams/diagrams.md`. Include Study architecture and Research procedure sections, two Mermaid flowcharts, and captions referencing the corresponding Research Spec design sections. Actually render them separately before claiming rendering acceptance.

Commit with the appropriate stage name, source folder and captured token. Literature and diagrams both depend on the complete Spec and topic brief. Neither depends on the other. Use `validate` after both are committed. A nonzero exit code means validation or a command failed; source-needed notes and unverified-rendering warnings do not make a structurally complete plan fail.

## Resume and revise

Start every new session with `status` and read `session-log.md`, the current brief and Research Spec. `ready` means the committed bytes and input dependencies match; `modified` means someone changed an output; `stale` means dependencies or confirmation changed; `untracked` means files exist without a stage commit; `missing` means at least one artifact is absent.

For an edited brief, reconcile a topic candidate, commit it and ask the student to approve the resulting scope again. For an edited Spec, copy all three current documents into a candidate set, reconcile changes, and commit spec. Regenerate affected downstream artifacts. A completed stage is not regenerated merely because the session changed. Research task checkboxes track the student's study, not software stage completion.

A stale candidate is rejected if current inputs, outputs or approval differ from its captured token. Do not fetch a fresh token solely to force old content through: reread and reconcile first. If a brief and student-edited design conflict, the coordinator must ask which version is intended; Python cannot resolve semantic contradictions.

## Preserve student edits

Wrap protected text in `<!-- student-edit:stable-id -->` and `<!-- /student-edit -->`. Keep the same markers in candidates. The current final block wins over candidate block contents. Missing, duplicate, nested or unclosed markers reject the whole stage before publication. For anonymous `student-edit` blocks, the nearest heading is the identity, so heading changes must be reconciled deliberately.

Outside-block edits are detected by hashes but not automatically merged. Agents must read and incorporate them. Keep important manual decisions in named blocks. The manager does not create historical backups.

## Transaction recovery

Only the manager writes final artifacts, `.ghostagent-state.json` and the session log. It locks manager operations, prevalidates a complete candidate stage, writes a journal, publishes documents and log, writes state last, then removes the journal. The next command rolls an interrupted transaction forward if every existing file still matches either its before or after hash. Conflicting outside edits stop recovery without overwriting those edits. Preserve the entire folder and reconcile conflicts rather than deleting state or forcing a commit. Do not read midway through a writer as if it were a committed snapshot.

## Frozen example

`examples/sample-run` includes the original idea, topic brief, research requirements/design/tasks, literature framework, diagrams, manager state and event log. Approval is explicitly simulated in its event history. `python ghostagent.py --topic examples/sample-run validate` validates the frozen structure. The example is a proposed self-report study, not collected data, real student consent or an executed Kiro run. Git attributes keep its Markdown and state files in LF form on every platform so byte hashes remain stable after cloning. The manager's persistent `.ghostagent.lock` is local runtime data and should be excluded from source commits.

## Exit codes

- 0: command succeeded; validate found no blocking structural errors.
- 1: validate found incomplete, modified or structurally invalid work.
- 2: rejected operation, conflicting candidate, malformed state or file-system error.

`--json` goes before the subcommand and is suitable for agent consumption. No network calls are made by the manager.

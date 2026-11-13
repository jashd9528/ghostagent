---
inclusion: always
---
# Steering — Managed Workflow

Kiro generates research plans. `ghostagent.py` is the only writer of final research artifacts, state and the session log. Python 3.10+ and the standard library are sufficient. Run commands from the repository root.

## Entry and recovery

Use `research-coordinator` as the entry point. For a new topic initialize `output/<topic-slug>` with `init --idea "..."`. For an existing topic first run `python ghostagent.py --topic output/<topic-slug> --json status`. Read the brief, Research Spec and session log. If several topic folders exist, ask which one the student means. A topic slug is stable after initialization.

The stages are `topic`, `spec`, `literature`, `diagrams`. The status report contains `next`, `confirmed`, `brief_hash`, and each stage's `status` and `based_on`. A stage is ready only when its saved output hashes and input hashes match the current files and all dependencies are ready. Files merely existing is insufficient. `missing`, `untracked`, `modified`, and `stale` require reconciliation or generation.

## Review gate

After committing a topic brief, show its scope and wait for explicit approval. Record the exact brief hash being reviewed. Only after approval call `confirm --hash <reviewed-hash>`. If that hash changed, ask for review again. Never infer consent from an old log, example text, an agent's own statement, or permission to implement this software. Downstream commits reject an unconfirmed brief.

## Candidate commit protocol

1. Read status and capture the selected stage's `based_on` BEFORE generation.
2. Read existing stage documents and all dependency documents. Resolve contradictory student edits with the student.
3. Write candidate Markdown under `output/<slug>/.candidates/<stage>/`, with the same relative file layout as final outputs. Never overwrite final files directly.
4. Keep all existing protected blocks in the candidates. Run `commit <stage> --source <candidate-folder> --based-on <captured-token> --reason "<actual change>"`.
5. If rejected, diagnose and reconcile. Never refresh the token just to force an unreviewed candidate through.
6. Use returned status to continue. At completion run `validate`. Validation is local structural evidence; it does not prove scholarship or Mermaid rendering.

A spec commit includes all three research-spec files. Literature and diagrams depend on the brief AND all Spec documents. A brief change invalidates confirmation and all downstream results. A Spec change invalidates literature and diagrams. Recommitting identical content does not invalidate downstream stages. Direct student edits remain visible as modified until incorporated through a candidate commit.

## Protected student edits

Use `<!-- student-edit:unique-id -->` ... `<!-- /student-edit -->` for stable named blocks. Existing anonymous `<!-- student-edit -->` blocks are supported using their nearest Markdown heading as identity. At most one anonymous block per heading; use IDs for multiple blocks. The manager retains the old block contents byte-for-byte as decoded UTF-8 text. Missing, renamed, nested, ambiguous or unclosed markers reject the complete stage. Student edits outside blocks remain visible and must be read and reconciled by the agent, but are not automatically merged.

## State ownership

The manager owns `.ghostagent-state.json` and `session-log.md`. Do not edit either by hand. Events record the actual local time, revision and trigger. OS locking serializes manager processes. A write-ahead journal permits roll-forward after interruption; an external conflicting edit stops recovery rather than overwriting it. Only read consistent final artifacts after a manager command succeeds. The journal is not a backup and this is not a multi-file database transaction for external readers.

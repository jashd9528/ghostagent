# Steering — Technical Conventions

## Runtime

Kiro custom agents generate research Markdown. A Python 3.10+ standard-library command, `ghostagent.py`, manages workflow state and structural validation. No application server, database, external API, or third-party Python dependency is needed. Kiro's own installation, authentication and service requirements still apply.

## Formats

- Research artifacts are GitHub-flavoured Markdown; diagrams are fenced Mermaid flowcharts.
- Agent definitions use current Kiro IDE 1.0 / CLI V3 JSON fields `name`, `description`, `prompt`, `tools`, `resources`; tool tags are `read`, `write`, `shell`.
- Older Kiro versions may require configuration migration. Loading in the actual target Kiro runtime must be checked separately.
- Machine state and recovery journal are JSON. The session log is managed Markdown.
- Documents use relative repository paths; generated state contains no machine-specific absolute paths.

## Writes and validation

Follow workflow.md. Only the manager publishes final artifacts. It preserves student-edit blocks, validates required sections, RQ references, task order and basic Mermaid fences/headers. It cannot validate scholarly truth, research quality, full Mermaid grammar or rendering. Explicitly report these limits.

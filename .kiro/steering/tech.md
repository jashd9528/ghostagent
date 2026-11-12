# Steering — Technical Conventions

## Runtime

- GhostAgent runs entirely inside Kiro (IDE or CLI). There is no separate
  server, database or build step.
- All configuration is declarative: Specs (Markdown), steering (Markdown)
  and custom agents (JSON) under `.kiro/`.

## Formats

- All documents are GitHub-flavoured Markdown.
- All diagrams are Mermaid code blocks inside Markdown. No binary image
  files are generated or committed for diagrams.
- Agent definitions are JSON with the fields: `name`, `description`,
  `prompt`, `tools`, `resources`.

## Constraints

- No external network services are required for the core workflow.
- Outputs must remain valid if the repository is cloned fresh: no absolute
  paths, no machine-specific references inside generated documents.
- When regenerating an existing output, preserve student edits made inside
  sections marked `<!-- student-edit -->` … `<!-- /student-edit -->`.

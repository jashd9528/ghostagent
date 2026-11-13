# GhostAgent 👻

Turn a thesis idea into a scoped, reviewable research plan using Kiro agents and a dependency-free Python workflow manager.

GhostAgent generates a topic brief, a per-topic Research Spec, a thematic literature review framework and Mermaid research diagrams. Kiro supplies the research reasoning; `ghostagent.py` enforces scope confirmation, tracks content dependencies and publishes protected candidate documents. It produces plans, not a finished thesis or verified scholarship.

## Visual research workspace

Open `frontend/index.html` directly for the screenshot-inspired, dark research workspace: four agent cards, Requirements / Design / Tasks views, dependency-aware task drafts, literature outline, local Mermaid rendering and project history. The interface supports Chinese and English and adapts to narrow screens. Use the top-bar language selector: Auto (IP), 中文 or English. Auto uses an IP country lookup (CN/HK/MO/TW → Chinese; other regions → English), falls back to browser language if lookup fails, and respects saved manual choices. Research documents and raw logs remain in their original language.

For real workflow operations, run `python -B workflow_server.py` from the repository root and open the workspace address printed by the launcher. The **Workflow** page opens existing `output/<slug>` topics, creates new ones, reviews and confirms the exact committed brief, submits full-stage candidates, refreshes status and runs validation. The built-in sample is read-only; copying it seeds only a topic and does not inherit simulated approval. The Kiro generation panel launches a candidate-only Kiro CLI session; review the generated documents before formal submission.

Opening the HTML directly retains offline draft/import/export mode. In connected mode, edits remain browser drafts until explicit stage submission. Candidate fingerprints remain pinned across refreshes; stale candidates require side-by-side reconciliation. Manager validation, dependency checks, protected student-edit blocks, locks and recovery are reused for formal writes. Source warnings are displayed, not treated as verified research.

Refresh the embedded sample after approved sample changes with `python -B frontend/export_sample.py`. The exporter validates the sample before writing. Mermaid 10.9.5 is bundled under `frontend/vendor/` with its upstream license for offline rendering. This is an interpretation of the demo screenshots, not a pixel-identical reproduction or an implementation of their statistical analysis displays.

### Kiro generation from the workspace

Install a Kiro CLI version supporting `chat --v3 --no-interactive --agent` and configure its own headless authentication (`KIRO_API_KEY` in the server environment where required). Credentials are not entered in the browser or stored in this repository. Click **Re-detect**, generate one stage, inspect live logs, then **Review candidate** and submit. Generation never implies scope approval or source verification.

The launcher detects `kiro-cli` on PATH or accepts `--kiro-executable <executable>`. On Windows, explicitly select an installed Linux CLI with `--kiro-wsl Ubuntu-24.04` and optionally its Linux executable path. The WSL environment must have its own required credentials. `--generation-timeout` sets a 10–1800 second limit (default 600). An editor-only installation is insufficient.

Jobs persist under `output/.kiro-jobs/`, retain the generation-time fingerprint, and support cancellation, polling, restart interruption detection and stale candidate rejection. A dedicated generated agent has no built-in tools or MCP servers; it receives a fixed formal snapshot via stdin and returns a bounded JSON candidate envelope. It is not an OS sandbox; locally configured Kiro hooks and global policies still apply. No trust-all-tools flag is passed. Raw model output and research context are local job data; do not publish the output directory.

## Requirements

- Python 3.10 or newer. No third-party Python packages are needed.
- Kiro for AI generation, with its own authentication and service requirements.
- Agent JSON targets Kiro IDE 1.0 / CLI V3 tool tags (`read`, `write`, `shell`). Older installations may need migration. Actual Kiro loading is not established by a local Python check.

The optional loopback-only workflow bridge uses Python standard-library HTTP; no database or API key is required. The manager also works independently of Kiro if you supply your own candidate documents.

## Quick start in Kiro

1. Open this repository in Kiro.
2. Select the `research-coordinator` custom agent and describe your research idea. If your Kiro surface does not support agent delegation, the coordinator follows stage prompts sequentially in the same session.
3. Review the generated topic brief. Explicitly approve its current scope before downstream work starts.
4. The coordinator commits the Research Spec, review framework and diagrams through the manager, then reports validation and any limitations.
5. In a later session, name the topic and ask to continue. The coordinator reads persisted status instead of regenerating completed stages.

Five definitions live in `.kiro/agents/`: the coordinator, `topic-analyst`, `spec-builder`, `literature-reviewer`, and `diagram-maker`. Every role follows `.kiro/steering/workflow.md`.

## Run the manager directly

Run commands from the repository root:

```sh
python ghostagent.py --topic output/my-topic init --idea "How do AI tools relate to undergraduate learning habits?"
python ghostagent.py --topic output/my-topic --json status
```

Generate a topic candidate at `output/my-topic/.candidates/topic/topic-brief.md`. Capture `stages.topic.based_on` from status before generation, then submit it:

```sh
python ghostagent.py --topic output/my-topic commit topic --source output/my-topic/.candidates/topic --based-on <captured-token> --reason "Initial scoped plan"
```

After the student explicitly reviews and approves that version, use its `brief_hash`:

```sh
python ghostagent.py --topic output/my-topic confirm --hash <reviewed-brief-sha256>
```

For `spec`, `literature` and `diagrams`, use the same candidate/commit protocol and the corresponding stage token. A spec candidate contains all three `research-spec/` documents. Tokens above are placeholders: copy actual values from your topic's status. In a shell replace angle-bracket placeholders before executing.

```sh
python ghostagent.py --topic output/my-topic validate
python ghostagent.py --topic examples/sample-run validate
```

`status` returns the next stage and `ready`, `missing`, `untracked`, `modified` or `stale` states. Direct edits are detected. Brief edits require recommit and renewed approval; Spec edits stale both downstream artifacts. Unrelated ready stages are retained. Completion means the planning artifacts are current, not that the student's research tasks are finished.

## Student edit protection

Use a stable named block inside any generated research document:

```markdown
<!-- student-edit:method-decisions -->
My supervisor's method decisions belong here.
<!-- /student-edit -->
```

The manager merges original protected contents into a candidate. Missing, renamed, nested or ambiguous blocks reject the entire stage. Anonymous legacy blocks are supported by their enclosing heading. Edits outside protected blocks must be reconciled by the agent and are not automatically merged.

## Project structure

```text
ghostagent.py                 # executable state manager, Python standard library
.kiro/agents/                 # coordinator + four research roles
.kiro/steering/               # product, style, layout, technology, workflow protocol
.kiro/specs/ghostagent-research-workflow/  # specification of this software
docs/                        # architecture and full operating guide
examples/sample-run/          # complete illustrative research-planning snapshot
output/<topic-slug>/           # generated research artifacts, state and candidate data (ignored)
```

The sample contains input, all seven research/log artifacts and machine state. Its scope confirmation is explicitly simulated for fixture construction. It is not evidence of a real student review or an executed Kiro session. Repository attributes preserve LF endings for this byte-hashed snapshot, including Windows checkouts. The manager creates `.ghostagent.lock` as local runtime data; do not include that lock file in source commits.

## Validation and limits

The manager checks hashes, review binding, stage dependencies, protected blocks, required headings, RQ references, task order, and basic Mermaid fences/headers. It serializes its own processes with an OS lock and uses a recoverable write-ahead journal. It does not authenticate the person approving a scope, assess academic truth, validate every Mermaid construct or perform source searches. A `confirm` command records the caller's assertion of student approval.

Use a real Mermaid renderer for rendering acceptance, a real Kiro session for runtime acceptance and the supervisor for research feasibility and ethics. Source-needed placeholders are expected in a planning framework and are not verified citations.

See [User guide](docs/USER_GUIDE.md), [Architecture](docs/ARCHITECTURE.md) and the workflow acceptance checklist for details.

## Demo

Existing project demo link: https://youtu.be/F3EKEneyoqA

This link is retained from the original project. Its content has not been checked against the new manager; it is not validation evidence for this implementation.

## License

MIT — see [LICENSE](LICENSE).

# Devpost Submission Texts — GhostAgent

Draft external-facing project description. Verify platform eligibility and historical facts before submission. This implementation has not been submitted or published by the workflow manager.

## Testing instructions

```text
Install Python 3.10+ and open the repository in Kiro. Kiro's authentication and service requirements apply. Agent JSON targets IDE 1.0 / CLI V3.

For a local structural check without AI generation, run:
python ghostagent.py --topic examples/sample-run validate

For live generation, select research-coordinator in Kiro and provide a research idea. Review the generated scope and explicitly confirm it. The coordinator uses the local manager to publish a Research Spec, literature review framework and diagrams. See docs/USER_GUIDE.md for exact candidate/commit commands and manual operation.

The frozen sample includes the input, all research artifacts, state and session log. Its approval is explicitly simulated fixture data, not a real student's review or evidence of a Kiro session.

Existing project demo link: https://youtu.be/F3EKEneyoqA
The video has not been checked against the updated implementation.
```

## Technology description

GhostAgent uses Kiro Specs to define the workflow, steering to define research and collaboration rules, and a coordinator plus four custom research agents to generate candidates. A Python standard-library manager enforces hash-bound scope approval, stage dependencies, stale-output detection, protected student edits, event logging and interrupted-publication recovery. Kiro remains responsible for AI research planning; the local manager requires no third-party Python packages or database. An optional loopback-only Python bridge connects the visual workspace to formal workflow operations.

The file-based visual workspace in `frontend/index.html` provides a screenshot-inspired agent dashboard, Spec editing, dependency-aware research-task drafts, literature navigation, local Mermaid rendering and SVG/candidate exports. It embeds a manager-validated sample and can inspect a selected topic folder. Direct-file preview keeps edits as browser drafts. Starting `workflow_server.py` enables opening/creating local topics, explicit hash-bound scope confirmation, complete-stage submission and validation through the same manager. Draft editing itself never publishes files or executes Kiro. A separate explicit Kiro generation action launches a tool-less, candidate-only CLI session, displays real logs and preserves its original base fingerprint. Generated output still requires review and formal submission; runtime CLI and authentication requirements apply. The frozen sample is read-only; copies do not inherit simulated approval. Run `python -B frontend/export_sample.py` to refresh the embedded sample after approved changes.

## Development-history disclosure

The original repository contained Kiro configuration, documentation and partial sample artifacts. This revision adds executable Python lifecycle management, a coordinator, updated stage protocols and a complete illustrative fixture. Confirm the original creation dates, hackathon eligibility and any required AI-use disclosure against the actual project history before submitting. No claim is made here that all work was created during a particular event.

## Submission checklist

- [ ] Confirm GitHub repository visibility and MIT license display.
- [ ] Confirm .kiro and the executable manager are included in the published repository.
- [ ] Demonstrate live execution in the stated Kiro version.
- [ ] Render the Mermaid diagrams and review all sources and limitations.
- [ ] Verify the demo describes this version.
- [ ] Check residence, category, dates and other eligibility against actual facts.

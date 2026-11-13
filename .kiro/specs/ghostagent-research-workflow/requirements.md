# Requirements — GhostAgent Research Workflow

GhostAgent turns a thesis idea into a reviewable research plan. Kiro generates candidates; a Python 3.10+ standard-library manager enforces local lifecycle rules.

## Requirement 1 — Topic intake and scope review

1. WHEN a subject or population cannot be identified, THE topic analyst SHALL ask one clarification rather than invent it.
2. WHEN a topic is generated, THE brief SHALL include refined statement, In scope and Out of scope lists, 3–5 consecutive RQs and key terms.
3. WHEN a brief is committed, THE coordinator SHALL request explicit approval of the exact current scope before later stages.
4. WHEN approval is recorded, THE manager SHALL bind it to the reviewed SHA256 and reject a mismatched hash.
5. IF brief bytes change, THE workflow SHALL block downstream commits until recommit and renewed approval.

## Requirement 2 — Research Spec

1. WHEN a current confirmed brief exists, THE spec builder SHALL submit requirements, design and tasks as one candidate stage.
2. THE requirements SHALL cover every RQ using EARS-style criteria; design SHALL include Chapter plan, Method outline, Procedure and a Mermaid flowchart.
3. THE tasks SHALL contain named checkboxes with dependencies only on earlier tasks; completed tasks SHALL NOT depend on unfinished tasks.
4. IF student-edited design and brief contradict, THE coordinator SHALL ask the student to resolve the semantic conflict before generation.

## Requirement 3 — Literature and academic integrity

1. WHEN a ready Spec exists, THE literature agent SHALL produce themes covering every RQ, each with Main debate, Established, Gap and This thesis, plus a Reading plan.
2. THE agents SHALL NOT invent citation strings; unverified field assertions, including proposed gaps, SHALL be hedged and marked `[source needed]`.
3. THE system SHALL describe outputs as plans and frameworks, not completed thesis chapters or verified findings.
4. THE manager SHALL disclose that citation heuristics do not prove provenance or scholarly truth.

## Requirement 4 — Diagrams

1. WHEN current brief and Spec dependencies exist, THE diagram agent SHALL produce Study architecture and Research procedure sections with Mermaid flowcharts and captions identifying design sections.
2. THE manager SHALL reject missing fences/headers/captions and SHALL NOT call these checks full syntax or rendering validation.
3. BEFORE claiming rendering acceptance, THE operator SHALL actually render all diagram blocks in a Mermaid renderer.

## Requirement 5 — State and recovery

1. THE manager SHALL expose init, status, confirm, commit and validate with machine-readable JSON and documented nonzero errors.
2. WHEN a session resumes, THE coordinator SHALL read state, log and Research Spec; it SHALL retain ready stages and select the next incomplete stage.
3. WHEN dependencies or outputs change, THE manager SHALL derive modified/stale states from content hashes and reject outdated candidate fingerprints.
4. WHEN publishing, THE manager SHALL serialize its own processes, prevalidate the complete stage, journal planned writes and replace state last.
5. AFTER interrupted publication, THE next command SHALL roll forward only if every file matches its before/after hash; outside-edit conflicts SHALL stop recovery.
6. THE manager SHALL record ordered dated events and SHALL NOT silently overwrite manually edited logs.

## Requirement 6 — Student edits and evidence

1. WHEN regenerating an artifact, THE manager SHALL preserve matched named or legacy anonymous student-edit block contents.
2. IF a protected block is missing, renamed, nested, ambiguous or unclosed, THE manager SHALL reject the complete candidate stage.
3. THE agent SHALL read and reconcile manual edits outside blocks; THE manager SHALL NOT claim automatic preservation outside blocks.
4. THE frozen fixture SHALL include input, all seven research/log artifacts and machine state; simulated approval SHALL be explicitly labelled.
5. THE documentation SHALL distinguish local structural checks from real Kiro execution, source verification and Mermaid rendering.

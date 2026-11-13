window.GHOST_SAMPLE = {
  "title": "AI Tools & Students’ Learning Habits",
  "sample": true,
  "verified": true,
  "report": {
    "topic": "ai-tools-learning-habits",
    "revision": 6,
    "confirmed": true,
    "brief_hash": "0e31dd2212d94f0a24104dedf31a762d142103da24ed05a51b8bd2cde7b89060",
    "next": "complete",
    "stages": {
      "topic": {
        "status": "ready",
        "based_on": "69fafe5b516e195d080f19dbd6b1ebb6897b33fc8ef23ef67c435c0e0c1dd12a"
      },
      "spec": {
        "status": "ready",
        "based_on": "8d7e57505ae4a3933faa46f83a4e35b6bf58ecac416e3e83ecfd370f2afc8258"
      },
      "literature": {
        "status": "ready",
        "based_on": "84bdd8f7e4f1c759e5508129131fd2c868a76fdb990165a27d25864313d7a454"
      },
      "diagrams": {
        "status": "ready",
        "based_on": "0c97084bc81d75ede600674d310a59698e05988c015a1cd534c74e7923f00b37"
      }
    }
  },
  "events": [
    {
      "action": "init",
      "detail": "Recorded the student's research idea; no research content generated.",
      "revision": 1,
      "time": "2026-11-12T23:58:55-08:00"
    },
    {
      "action": "commit:topic",
      "detail": "Build illustrative fixture, not a live Kiro run.",
      "revision": 2,
      "time": "2026-11-12T23:58:55-08:00"
    },
    {
      "action": "fixture-confirmation",
      "detail": "SIMULATED REVIEW for the frozen fixture only. No actual student approval is asserted.",
      "revision": 3,
      "time": "2026-11-12T23:58:55-08:00"
    },
    {
      "action": "commit:spec",
      "detail": "Build illustrative fixture, not a live Kiro run.",
      "revision": 4,
      "time": "2026-11-12T23:58:55-08:00"
    },
    {
      "action": "commit:literature",
      "detail": "Build illustrative fixture, not a live Kiro run.",
      "revision": 5,
      "time": "2026-11-12T23:58:55-08:00"
    },
    {
      "action": "commit:diagrams",
      "detail": "Build illustrative fixture, not a live Kiro run.",
      "revision": 6,
      "time": "2026-11-12T23:58:55-08:00"
    }
  ],
  "documents": {
    "input.md": "# Research Input\n\nHelp me plan my thesis: the impact of AI tools on college students' learning habits.\n",
    "topic-brief.md": "# Topic Brief — The Impact of AI Tools on College Students' Learning Habits\n\nIllustrative Stage 1 artifact for testing the managed workflow. Confirmation in the fixture is simulated; no actual student approval or Kiro run is asserted.\nTopic slug: `ai-tools-learning-habits`\n\n## Refined topic statement\n\nThis thesis investigates how the regular use of generative AI tools (such as\nchat-based assistants) is associated with changes in the learning habits of\nundergraduate students, and how students themselves perceive that relationship.\n\n## Scope\n\n**In scope**\n\n- Undergraduate students at a single university.\n- Self-reported learning habits: study planning, note-taking, problem-solving\n  approach, revision behaviour, and help-seeking.\n- Generative AI tools used for study purposes.\n\n**Out of scope**\n\n- High-school or postgraduate populations.\n- Measured academic performance (grades) as an outcome variable.\n- Detection of AI-generated coursework or academic-misconduct policy.\n\n## Research questions\n\n- **RQ1** — How frequently, and for which study activities, do undergraduate\n  students use generative AI tools?\n- **RQ2** — Which learning habits do students report having changed since\n  they began using AI tools, and in what direction?\n- **RQ3** — How do students perceive the effect of AI tools on their own\n  learning, and what concerns, if any, do they express?\n\n## Key terms\n\n- **Generative AI tool** — a chat-based or embedded AI assistant that\n  produces text responses to user prompts, used by the student for study.\n- **Learning habit** — a recurring, self-reported study behaviour (planning,\n  note-taking, problem-solving, revision, help-seeking).\n- **Perceived effect** — the student's own judgement of whether and how a\n  habit has changed, as distinct from a measured behavioural change.\n",
    "research-spec/requirements.md": "# Research Requirements — AI Tools and Learning Habits\n\nIllustrative Stage 2 Research Spec derived from the scoped topic brief. These are requirements for a proposed study, not empirical findings.\n\n## Requirements\n\n### RQ1 — Use by study activity\n\nWHEN eligible participants complete the questionnaire, THE study SHALL record frequency of Generative AI tool use for study planning, note-taking, problem-solving approach, revision behaviour, and help-seeking separately.\n\nAcceptance: the instrument includes a defined recall period, a non-user option and one frequency item per activity; the results report each item with its denominator and missing responses.\n\n### RQ2 — Self-reported changes\n\nWHEN participants report use of a Generative AI tool, THE study SHALL ask which Learning habits they report changing since first use and the direction of each change.\n\nAcceptance: each activity has increased, decreased, unchanged and unsure options with clear wording; interviews explore examples. Reporting distinguishes self-reported change from observed change and avoids causal claims.\n\n### RQ3 — Perceived effect and concerns\n\nWHEN participants describe their Perceived effect, THE study SHALL collect perceived benefits, concerns and uncertainty linked to the same five Learning habits.\n\nAcceptance: questionnaire and interview prompts map to the activity list; analysis covers positive, negative and mixed accounts, without treating Perceived effect as measured performance.\n\n### Ethics and scope\n\nWHEN any recruitment or collection begins, THE researcher SHALL first obtain the institutionally required ethics determination and use reviewed information and consent materials.\n\nAcceptance: participation is voluntary; contact details for interviews are collected separately from survey responses; no grades or unnecessary direct identifiers are collected; access, retention and withdrawal limits are documented before launch.\n",
    "research-spec/design.md": "# Research Design — AI Tools and Learning Habits\n\nIllustrative Stage 2 plan for RQ1–RQ3. The design uses a single-university questionnaire and follow-up semi-structured interviews; it does not establish causal effects.\n\n## Chapter plan\n\n1. Introduction: scope, RQ1–RQ3 and terms from topic-brief.md.\n2. Literature review: use by activity, self-reported changes and Perceived effect.\n3. Methodology: recruitment, instruments, ethics and analysis.\n4. Findings: descriptive questionnaire summaries and interview themes mapped to the RQs.\n5. Discussion: compare supported findings with verified literature and explain limitations.\n6. Conclusion: answer the RQs within the stated scope.\n\n## Method outline\n\nRecruit volunteer undergraduate students from one university after the required ethics review. Determine a feasible recruitment target with the supervisor rather than inventing a statistically justified sample size. Eligibility, recruitment channels and the final target must be specified before recruitment.\n\nThe questionnaire asks about Generative AI tool use during the last four weeks for the five Learning habits in the brief (RQ1). It asks respondents to describe direction of change since first use, with unchanged and unsure choices (RQ2), and Perceived effect and concerns for those same activities (RQ3). Non-users can answer relevant perception questions and skip change-since-use questions. Interview prompts seek concrete examples and contradictory cases.\n\nKeep the questionnaire response dataset and interview transcript dataset separate. Summarise questionnaire frequency and missingness descriptively for RQ1 and RQ2. Code de-identified interviews thematically for RQ2 and RQ3 and compare the two evidence streams at the level of RQs, not by unconsented individual linkage. A separate opt-in contact form is not linked to survey responses. Obtain separate interview consent, explain withdrawal limits, minimise identifiers and document restricted access and the approved retention period.\n\n<!-- student-edit:method-decisions -->\nSupervisor decisions pending: recruitment target, approved storage location, retention period and final questionnaire wording. Do not treat these as approved merely because the planning workflow is complete.\n<!-- /student-edit -->\n\n## Procedure\n\nConfirm the topic; prepare the Research Spec and a source-verification reading plan; draft instruments and ethics materials; obtain the required ethics determination; pilot and revise under the approved process; recruit and obtain consent; collect questionnaire responses and interviews; de-identify, summarise and code; integrate by RQ; write and review the thesis.\n\n```mermaid\nflowchart TD\n    A[\"Confirm topic and Research Spec\"] --> B[\"Verify literature and draft instruments\"]\n    B --> C[\"Obtain ethics determination\"]\n    C --> D[\"Pilot and revise within approved process\"]\n    D --> E[\"Recruit and obtain consent\"]\n    E --> F[\"Collect questionnaire and interview data\"]\n    F --> G[\"De-identify and analyse separate datasets\"]\n    G --> H[\"Integrate by RQ1–RQ3 and write findings\"]\n```\n\n## Limitations\n\nThe single-university volunteer sample is not representative of all undergraduates. Recall and self-selection may bias reports. Cross-sectional self-reports and retrospective accounts cannot establish whether AI use caused Learning habit changes. Grades, observed behaviour and misconduct detection remain out of scope. Proposed literature gaps remain hypotheses until sources are read.\n",
    "research-spec/tasks.md": "# Research Tasks — AI Tools and Learning Habits\n\nIllustrative Stage 2 task plan. Workflow fixture completion is not completion of these student research activities. All research tasks remain unchecked.\n\n## Tasks\n\n- [ ] T1 Review scope, RQ1–RQ3 and supervisor feasibility. Depends on: none.\n- [ ] T2 Read and verify the literature by theme; revise provisional gaps. Depends on: T1.\n- [ ] T3 Finalise instruments, sampling target, consent, retention and analysis plan. Depends on: T2.\n- [ ] T4 Obtain the institutionally required ethics determination. Depends on: T3.\n- [ ] T5 Pilot and revise instruments within the approved process. Depends on: T4.\n- [ ] T6 Recruit volunteers and obtain consent. Depends on: T5.\n- [ ] T7 Collect questionnaire responses and interviews separately. Depends on: T6.\n- [ ] T8 De-identify data, summarise questionnaire responses and code interviews. Depends on: T7.\n- [ ] T9 Integrate evidence by RQ and write findings and discussion. Depends on: T8.\n- [ ] T10 Review scope, sources, limitations and final submission with supervisor. Depends on: T9.\n",
    "literature-review-framework.md": "# Literature Review Framework — AI Tools and Learning Habits\n\nIllustrative Stage 3 planning framework for RQ1–RQ3, aligned with the Research Spec. All field claims below are questions or hypotheses to verify; no sources have been supplied or independently verified.\n\n## Theme 1 — Generative AI tool use by activity (RQ1)\n\n- **Main debate:** investigate whether answer-seeking or study-support uses predominate and how survey wording changes that interpretation. [source needed]\n- **Established:** establish from sources what is actually known about undergraduate use, recall periods and activity categories; no prevalence estimate is assumed here. [source needed]\n- **Gap:** provisional hypothesis to verify: some studies may aggregate use rather than distinguish the five Learning habits. Do not assert novelty without reading those studies. [source needed]\n- **This thesis:** records frequency for study planning, note-taking, problem-solving approach, revision behaviour and help-seeking separately, with a four-week recall period. Revise the proposed contribution if the literature already provides this detail.\n\n## Theme 2 — Reported changes in Learning habits (RQ2)\n\n- **Main debate:** compare claims about cognitive offloading and learning support; assess what methods can support each interpretation. [source needed]\n- **Established:** verify which studies use self-reports, observed behaviour or longitudinal designs; do not assume one evidence type dominates. [source needed]\n- **Gap:** provisional hypothesis to verify: activity-specific direction of self-reported change and uncertainty may not always be distinguished. [source needed]\n- **This thesis:** asks direction of change for each Learning habit, including unchanged and unsure, and seeks examples in interviews. It does not investigate desired changes or establish causal effects.\n\n## Theme 3 — Perceived effect and concerns (RQ3)\n\n- **Main debate:** investigate perceived support, uncertainty, skill concerns and integrity concerns without presuming their prevalence or balance. [source needed]\n- **Established:** verify how prior instruments define and measure Perceived effect; distinguish participant judgements from measured outcomes. [source needed]\n- **Gap:** provisional hypothesis to verify: some perception accounts may not link concerns to specific Learning habits. [source needed]\n- **This thesis:** ties perception prompts to the same five Learning habits and integrates interview and survey evidence at the RQ level without unconsented record linkage.\n\n## Reading plan\n\n| Order | Search terms | Where | Feeds |\n| --- | --- | --- | --- |\n| 1 | generative AI undergraduate study habits activity frequency survey | ERIC, education databases, Google Scholar | RQ1 |\n| 2 | cognitive offloading AI learning self-report longitudinal scaffolding | ERIC, education databases, Google Scholar | RQ2 |\n| 3 | generative AI student perceptions study habits concerns interviews | Education databases, Google Scholar | RQ3 |\n| 4 | institution generative AI education ethics survey consent guidance | Institutional and official guidance | Methods and ethics |\n\nRecord the actual query, date, inclusion criteria, method, population and relevant claim for each source read. Replace each `[source needed]` only with a supplied and checked source that supports that exact claim; otherwise revise or remove the claim. Revise gaps after reading, before calling them contributions. This plan has not performed a literature search.\n",
    "diagrams.md": "# Diagrams — AI Tools and Learning Habits\n\nIllustrative Stage 4 diagrams derived from research-spec/design.md. The manager checks fences and flowchart headers, not full rendering; actual rendering must be checked separately.\n\n## Study architecture\n\nCaption: separate datasets and RQ-level integration; visualises research-spec/design.md, \"Method outline\".\n\n```mermaid\nflowchart TD\n    Q[\"Questionnaire: Generative AI tool use and Learning habits\"] --> QS[\"De-identified questionnaire response dataset\"]\n    I[\"Consented semi-structured interviews\"] --> IS[\"De-identified interview transcript dataset\"]\n    QS --> A[\"Descriptive frequencies and missingness: RQ1 and RQ2\"]\n    IS --> B[\"Thematic coding: RQ2 and RQ3\"]\n    A --> C[\"Integrate by research question, without individual record linkage\"]\n    B --> C\n    C --> D[\"Findings and discussion within self-report limitations\"]\n```\n\n## Research procedure\n\nCaption: sequence of the planned study, including ethics and consent; visualises research-spec/design.md, \"Procedure\".\n\n```mermaid\nflowchart LR\n    S1[\"Confirm topic and Research Spec\"] --> S2[\"Verify literature and draft instruments\"]\n    S2 --> S3[\"Obtain ethics determination\"]\n    S3 --> S4[\"Pilot and revise within approved process\"]\n    S4 --> S5[\"Recruit and obtain consent\"]\n    S5 --> S6[\"Collect separate questionnaire and interview data\"]\n    S6 --> S7[\"De-identify, summarise and code\"]\n    S7 --> S8[\"Integrate by RQ1–RQ3 and write findings\"]\n```\n",
    "session-log.md": "# Session Log\n\nManaged workflow events. Research content and student review remain separate.\n\n## 1 — 2026-11-12T23:58:55-08:00 — init\n\nRecorded the student's research idea; no research content generated.\n\n## 2 — 2026-11-12T23:58:55-08:00 — commit:topic\n\nBuild illustrative fixture, not a live Kiro run.\n\n## 3 — 2026-11-12T23:58:55-08:00 — fixture-confirmation\n\nSIMULATED REVIEW for the frozen fixture only. No actual student approval is asserted.\n\n## 4 — 2026-11-12T23:58:55-08:00 — commit:spec\n\nBuild illustrative fixture, not a live Kiro run.\n\n## 5 — 2026-11-12T23:58:55-08:00 — commit:literature\n\nBuild illustrative fixture, not a live Kiro run.\n\n## 6 — 2026-11-12T23:58:55-08:00 — commit:diagrams\n\nBuild illustrative fixture, not a live Kiro run.\n"
  },
  "validation": {
    "ok": true,
    "warnings": [
      "literature-review-framework.md: unverified source slots remain (expected for a planning framework).",
      "Mermaid checks are structural only; rendering is not verified by this command.",
      "Academic validity, source truth and actual Kiro execution require human/runtime review."
    ]
  }
};

# Diagrams — AI Tools and Learning Habits

Illustrative Stage 4 diagrams derived from research-spec/design.md. The manager checks fences and flowchart headers, not full rendering; actual rendering must be checked separately.

## Study architecture

Caption: separate datasets and RQ-level integration; visualises research-spec/design.md, "Method outline".

```mermaid
flowchart TD
    Q["Questionnaire: Generative AI tool use and Learning habits"] --> QS["De-identified questionnaire response dataset"]
    I["Consented semi-structured interviews"] --> IS["De-identified interview transcript dataset"]
    QS --> A["Descriptive frequencies and missingness: RQ1 and RQ2"]
    IS --> B["Thematic coding: RQ2 and RQ3"]
    A --> C["Integrate by research question, without individual record linkage"]
    B --> C
    C --> D["Findings and discussion within self-report limitations"]
```

## Research procedure

Caption: sequence of the planned study, including ethics and consent; visualises research-spec/design.md, "Procedure".

```mermaid
flowchart LR
    S1["Confirm topic and Research Spec"] --> S2["Verify literature and draft instruments"]
    S2 --> S3["Obtain ethics determination"]
    S3 --> S4["Pilot and revise within approved process"]
    S4 --> S5["Recruit and obtain consent"]
    S5 --> S6["Collect separate questionnaire and interview data"]
    S6 --> S7["De-identify, summarise and code"]
    S7 --> S8["Integrate by RQ1–RQ3 and write findings"]
```

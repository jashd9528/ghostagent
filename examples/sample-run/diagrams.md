# Diagrams — AI Tools and Learning Habits

Produced by `diagram-maker` (Stage 4) from the research design.

## Study architecture

*Caption: components of the planned study and the flow of data between them.
Visualises research-spec/design.md, "Method outline".*

```mermaid
flowchart TD
    A[Questionnaire<br/>AI use by study activity] --> C[Response dataset]
    B[Semi-structured interviews<br/>habit change and perceptions] --> C
    C --> D[Quantitative summary<br/>frequencies per activity - RQ1]
    C --> E[Thematic coding<br/>habit change - RQ2<br/>perceptions - RQ3]
    D --> F[Findings chapter]
    E --> F
    F --> G[Discussion<br/>against literature review themes 1-3]
```

## Research procedure

*Caption: the study executed in order. Visualises research-spec/design.md,
"Procedure".*

```mermaid
flowchart LR
    S1[Confirm topic brief] --> S2[Generate research Spec]
    S2 --> S3[Build literature review framework]
    S3 --> S4[Draft questionnaire and interview guide]
    S4 --> S5[Collect responses]
    S5 --> S6[Analyse: summary + thematic coding]
    S6 --> S7[Write findings and discussion]
```

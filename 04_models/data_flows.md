# Data Flow Diagrams

> Where HCP data comes from, where it is stored and where it goes. DFD notation adapted to Mermaid: rectangles = external entities, rounded boxes = processes, cylinders = data stores.
> Fictional case.

## 1. Context diagram (level 0)

```mermaid
%%{init: {'theme':'base','themeVariables':{'fontFamily':'Arial','primaryColor':'#E3EEFA','primaryBorderColor':'#3B6EA8','primaryTextColor':'#1E2A38','lineColor':'#4A5A70','secondaryColor':'#E2F3F1','tertiaryColor':'#F7F9FC','edgeLabelBackground':'#FFFFFF'}}}%%
flowchart LR
    REP["Field reps<br/>(both companies)"]
    STW["Data stewards"]
    TRA["Transparency team"]
    REF["Third-party<br/>reference database"]
    NPPES["US national NPI registry"]
    PAYS["Spend and event systems"]
    REG["Regulators<br/>CMS Open Payments,<br/>French public platform,<br/>national EFPIA platforms"]

    SYS(["HCP master data<br/>solution"])

    REP -- "new doctor details, searches" --> SYS
    SYS -- "candidates, golden records" --> REP
    REF -- "reference doctor data, RPPS" --> SYS
    NPPES -- "NPI verification" --> SYS
    PAYS -- "payments with source doctor key" --> SYS
    STW -- "match decisions, overrides, unmerges" --> SYS
    SYS -- "review queue with reasons" --> STW
    SYS -- "disclosure extract, change flags" --> TRA
    TRA -- "disclosure reports" --> REG
    classDef ext fill:#E3EEFA,stroke:#3B6EA8,color:#1E2A38
    classDef proc fill:#E2F3F1,stroke:#2A7F8E,color:#1E2A38
    classDef store fill:#EEF1F5,stroke:#4A5A70,color:#1E2A38
    classDef sys fill:#E2F3F1,stroke:#2A7F8E,stroke-width:2px,color:#1E2A38
    class REP,STW,TRA,REF,NPPES,PAYS,REG ext
    class SYS sys
```

The solution never sends data to regulators directly. The Transparency team stays responsible for what is published.

## 2. Level 1

```mermaid
%%{init: {'theme':'base','themeVariables':{'fontFamily':'Arial','primaryColor':'#E3EEFA','primaryBorderColor':'#3B6EA8','primaryTextColor':'#1E2A38','lineColor':'#4A5A70','secondaryColor':'#E2F3F1','tertiaryColor':'#F7F9FC','edgeLabelBackground':'#FFFFFF'}}}%%
flowchart TB
    REP["Field reps"]
    STW["Data stewards"]
    TRA["Transparency team"]
    REF["Reference database"]
    NPPES["NPI registry"]
    PAYS["Spend and event systems"]
    CRM["PharmaCo CRM,<br/>BioCo CRM"]

    P1(["1.0 Capture and<br/>validate doctor"])
    P2(["2.0 Match and merge"])
    P3(["3.0 Steward review"])
    P4(["4.0 Publish golden record"])
    P5(["5.0 Produce disclosure extract"])

    D1[("D1 Golden records<br/>and identifiers")]
    D2[("D2 Source records<br/>cross-reference")]
    D3[("D3 Candidate pairs<br/>and review queue")]
    D4[("D4 Merge event log")]
    D5[("D5 Publication basis")]
    D6[("D6 Payment links")]

    REP -- "doctor details" --> P1
    NPPES -- "NPI check" --> P1
    P1 -- "validated source record" --> D2
    P1 -- "new record event" --> P2
    REF -- "reference records" --> D2

    D2 -- "records to compare" --> P2
    D1 -- "existing golden records" --> P2
    P2 -- "pairs, scores, outcomes" --> D3
    P2 -- "merges" --> D1
    P2 -- "merge events" --> D4

    D3 -- "pairs to review" --> P3
    STW -- "decisions, unmerges" --> P3
    P3 -- "decision labels" --> D3
    P3 -- "merges, unmerges" --> D1
    P3 -- "merge events" --> D4

    D1 -- "golden records" --> P4
    P4 -- "updates within 15 min" --> CRM
    CRM -- "searches" --> P1

    PAYS -- "payments" --> D6
    D6 -- "payments by source record" --> P5
    D2 -- "source to golden mapping" --> P5
    D5 -- "consent or legal basis" --> P5
    D4 -- "changes since last extract" --> P5
    P5 -- "extract with flags" --> TRA
    classDef ext fill:#E3EEFA,stroke:#3B6EA8,color:#1E2A38
    classDef proc fill:#E2F3F1,stroke:#2A7F8E,color:#1E2A38
    classDef store fill:#EEF1F5,stroke:#4A5A70,color:#1E2A38
    classDef sys fill:#E2F3F1,stroke:#2A7F8E,stroke-width:2px,color:#1E2A38
    class REP,STW,TRA,REF,NPPES,PAYS,CRM ext
    class P1,P2,P3,P4,P5 proc
    class D1,D2,D3,D4,D5,D6 store
```

## 3. Data stores

| Store | Content | Owner | Retention |
|---|---|---|---|
| D1 Golden records and identifiers | One record per doctor, NPI, RPPS, reference ID | Data Governance Lead | While the doctor is in scope, plus legal retention |
| D2 Source records cross-reference | Every source record and its golden record | Data Governance Lead | As D1 |
| D3 Candidate pairs and review queue | Pairs, scores, outcomes, steward decisions | Data Governance Lead | Used as training labels; retention agreed with DPO (NFR-05) |
| D4 Merge event log | Immutable history of merges and unmerges | Chief Compliance Officer | At least as long as disclosure records must be kept |
| D5 Publication basis | Consent or legal basis per doctor, country, year | Chief Compliance Officer | As disclosure records |
| D6 Payment links | Link between each payment and its source record | Transparency Analyst | As disclosure records |

## 4. Personal data note

D1, D2, D3 and D5 hold personal data of doctors. Access follows NFR-02. Model training reads D2 and D3 only within the purpose agreed with the DPO (NFR-05).

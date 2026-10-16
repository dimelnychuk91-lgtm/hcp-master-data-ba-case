# Data Model: HCP Master Data

> Conceptual and logical model for the HCP master. Attribute-level detail: [data dictionary](data_dictionary.md).
> The model is vendor-neutral: an MDM platform implements it as configuration.
> Fictional case.

## 1. Conceptual model

What the business talks about, in its own words.

```mermaid
%%{init: {'theme':'base','themeVariables':{'fontFamily':'Arial','primaryColor':'#E3EEFA','primaryBorderColor':'#3B6EA8','primaryTextColor':'#1E2A38','lineColor':'#4A5A70','secondaryColor':'#E2F3F1','tertiaryColor':'#F7F9FC','edgeLabelBackground':'#FFFFFF'}}}%%
flowchart LR
    HCP["Doctor (HCP)<br/>golden record"]
    SRC["Source record<br/>in CRM, events, spend"]
    ID["Identifier<br/>NPI, RPPS, reference ID"]
    HCO["Organisation (HCO)"]
    CON["Publication basis<br/>consent or legal obligation"]
    PAY["Payment<br/>transfer of value"]
    MATCH["Candidate pair"]
    EVT["Merge event"]

    SRC -- "describes" --> HCP
    HCP -- "is identified by" --> ID
    HCP -- "practises at" --> HCO
    HCP -- "has, per country and year" --> CON
    PAY -- "is made to" --> HCP
    MATCH -- "compares two" --> SRC
    EVT -- "changes" --> HCP
```

**Key business rules shown by the model**

- A doctor has **one** golden record and **one or more** source records.
- A payment is linked to a source record in the system that made it, and through it to exactly one golden record (BR-02).
- Publication basis is held **per country and reporting year**: the same doctor can consent in one year and withdraw in the next.
- Merge events are never deleted (NFR-01).

## 2. Logical model

```mermaid
%%{init: {'theme':'base','themeVariables':{'fontFamily':'Arial','primaryColor':'#E3EEFA','primaryBorderColor':'#3B6EA8','primaryTextColor':'#1E2A38','lineColor':'#4A5A70','secondaryColor':'#E2F3F1','tertiaryColor':'#F7F9FC','edgeLabelBackground':'#FFFFFF'}}}%%
erDiagram
    HCP ||--|{ SOURCE_RECORD : "described by"
    HCP ||--o{ HCP_IDENTIFIER : "identified by"
    HCP ||--o{ AFFILIATION : "has"
    HCO ||--o{ AFFILIATION : "has"
    HCP ||--o{ PUBLICATION_BASIS : "has"
    SOURCE_RECORD ||--o{ PAYMENT : "receives"
    SOURCE_RECORD ||--o{ CANDIDATE_PAIR : "record A"
    SOURCE_RECORD ||--o{ CANDIDATE_PAIR : "record B"
    CANDIDATE_PAIR ||--o| STEWARD_DECISION : "resolved by"
    HCP ||--o{ MERGE_EVENT : "changed by"
    MERGE_EVENT ||--|{ MERGE_EVENT_RECORD : "moves"
    SOURCE_RECORD ||--o{ MERGE_EVENT_RECORD : "moved in"

    HCP {
        string hcp_id PK
        string status "active, merged, inactive"
        string survivor_hcp_id FK "set when merged"
        string first_name
        string last_name
        string specialty_code
        string country_code
        string primary_address
        datetime last_updated
    }
    SOURCE_RECORD {
        string source_record_id PK
        string source_system "PHARMACO_CRM, BIOCO_CRM, EVENTS, SPEND, REFDB"
        string source_key
        string hcp_id FK
        string first_name
        string last_name
        string address
        string specialty_source_code
        datetime received_at
    }
    HCP_IDENTIFIER {
        string hcp_id FK
        string id_type "NPI, RPPS, REFDB"
        string id_value
        string source_system
        boolean verified
    }
    HCO {
        string hco_id PK
        string name
        string type "hospital, clinic, teaching hospital"
        string country_code
    }
    AFFILIATION {
        string hcp_id FK
        string hco_id FK
        date start_date
        date end_date
    }
    PUBLICATION_BASIS {
        string hcp_id FK
        string country_code
        int reporting_year
        string basis "consent, no consent, legal obligation"
        date recorded_on
        string evidence_ref
    }
    PAYMENT {
        string payment_id PK
        string source_record_id FK
        date payment_date
        decimal amount
        string currency
        string nature "fee, travel, meal, grant"
        string reporting_cycle
    }
    CANDIDATE_PAIR {
        string pair_id PK
        string record_a_id FK
        string record_b_id FK
        string rule_applied "NPI_EXACT or none"
        decimal model_score
        string model_version
        string outcome "auto merged, review, not duplicate"
        datetime created_at
    }
    STEWARD_DECISION {
        string pair_id FK
        string decision "same doctor, different doctors"
        string reason_code
        string comment
        string steward_id
        datetime decided_at
    }
    MERGE_EVENT {
        string event_id PK
        string event_type "merge, unmerge"
        string hcp_id FK
        string actor "rule, model, steward id"
        decimal model_score
        string model_version
        decimal threshold
        string reason
        datetime event_at
    }
    MERGE_EVENT_RECORD {
        string event_id FK
        string source_record_id FK
        string from_hcp_id
        string to_hcp_id
    }
```

## 3. UML class diagram

The same domain in UML notation, with multiplicities, composition, the affiliation association class and enumerations.
Source: [class_domain.puml](src/class_domain.puml).

![Domain class diagram](img/class_domain.svg)

Lifecycles of HCP and candidate pair: [state machines](state_machines.md).

## 4. Design decisions in the model

| Decision | Why | Alternative rejected |
|---|---|---|
| **Payments link to the source record, not directly to the golden record** | When a merge is undone, payments follow their source record to the correct doctor automatically (BR-09) | Linking payments to the golden record would need a manual re-assignment on every unmerge |
| **Merged golden records are kept with status `merged` and a pointer to the survivor** | A system that still holds the old ID can be redirected; history stays readable | Deleting merged records would break references in both CRMs |
| **Identifiers in a separate entity** | A doctor can have NPI, RPPS and a reference ID at the same time, each with its own source and verification | Columns per identifier type would need a schema change for every new country |
| **Publication basis per country and year** | Consent can change by year; France has a legal basis instead of consent (BR-10) | One consent flag on the doctor cannot express either |
| **Merge event plus moved records** | Unmerge needs to know exactly which source records moved where (NFR-01) | A single "merged with" field loses the history after a second merge |
| **Candidate pairs are stored, including "not duplicate"** | They become training labels and explain past decisions (DEC-08) | Storing only merges gives no negative examples, the problem we found in discovery |

## 5. What the model leaves out on purpose

- Full HCO hierarchy (parent organisations, networks): out of scope (DEC-01).
- Patient data: never part of HCP master data.
- Contact details used only for marketing: not needed for matching or reporting (NFR-05).

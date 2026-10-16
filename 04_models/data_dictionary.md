# Data Dictionary

> Attribute-level definitions for the [logical data model](data_model.md).
> **Survivorship** says which value wins on the golden record when sources disagree. Full logic: [matching rules](matching_rules.md), section 4.
> **Owner** is accountable for the meaning and quality of the attribute (see [RACI](../05_governance/raci.md)).
> Fictional case.

Legend: **M** mandatory, **C** conditional, **O** optional.

## HCP (golden record)

| Attribute | Definition | Type | M/C/O | Sources | Survivorship | Owner | Quality rule |
|---|---|---|---|---|---|---|---|
| hcp_id | Unique ID of the doctor in the master. Never reused | string(12) | M | MDM | generated | Data Governance Lead | Unique, immutable |
| status | `active`, `merged`, `inactive` | enum | M | MDM | n/a | Data Governance Lead | `merged` requires survivor_hcp_id |
| survivor_hcp_id | Golden record this one was merged into | string(12) | C | MDM | n/a | Data Governance Lead | Set only when status = `merged`; points to an `active` record |
| first_name | Given name, without titles | string(100) | M | all | Reference database, then most recent CRM value | Country steward | No titles ("Dr.", "Prof."); diacritics kept |
| last_name | Family name, without titles | string(100) | M | all | Reference database, then most recent CRM value | Country steward | As first_name |
| specialty_code | Main specialty, from the single PharmaCo code list | string(10) | M | all, mapped | Reference database, then CRM | Data Governance Lead | Value exists in the code list |
| country_code | Country of practice, ISO 3166-1 alpha-2 | string(2) | M | all | Most recent verified affiliation | Country steward | US, DE or FR in phase 1 |
| primary_address | Main address of practice, standardised | structured | M | all | Most recent verified source | Country steward | Passes country address standardisation |
| last_updated | Time of last change to the golden record | datetime | M | MDM | generated | n/a | System time, UTC |

## SOURCE_RECORD

| Attribute | Definition | Type | M/C/O | Sources | Survivorship | Owner | Quality rule |
|---|---|---|---|---|---|---|---|
| source_record_id | ID of this record inside the MDM | string(16) | M | MDM | n/a | Data Governance Lead | Unique |
| source_system | System the record came from | enum | M | MDM | n/a | Enterprise Architect | One of the registered source systems |
| source_key | The record's own ID in the source system | string(50) | M | source | n/a | System owner | Unique within source_system |
| hcp_id | Golden record this source record belongs to | string(12) | M | MDM | n/a | Country steward | Points to an `active` HCP |
| first_name, last_name, address, specialty_source_code | Values as received from the source, unchanged | various | as source | source | not applicable: kept as received | System owner | Stored as received for audit |
| received_at | Time the MDM last received this record | datetime | M | MDM | n/a | n/a | UTC |

## HCP_IDENTIFIER

| Attribute | Definition | Type | M/C/O | Sources | Survivorship | Owner | Quality rule |
|---|---|---|---|---|---|---|---|
| id_type | `NPI` (US), `RPPS` (France), `REFDB` (third-party reference ID) | enum | M | MDM | n/a | Data Governance Lead | Registered type |
| id_value | Identifier value | string(20) | M | source | One active value per id_type per doctor | Country steward | NPI: 10 digits with valid check digit. RPPS: 11 digits |
| source_system | Where the identifier came from | enum | M | MDM | n/a | n/a | Registered source |
| verified | Checked against the official registry or reference database | boolean | M | MDM | n/a | Country steward | NPI verified against the national registry before go-live |

**Rule:** a US HCP must have one verified NPI (BR-03). Two HCPs cannot share the same active NPI.

## HCO and AFFILIATION

| Attribute | Definition | Type | M/C/O | Sources | Survivorship | Owner | Quality rule |
|---|---|---|---|---|---|---|---|
| hco_id | ID of the organisation | string(12) | M | MDM | generated | Data Governance Lead | Unique |
| name | Standardised organisation name | string(200) | M | CRMs, reference DB | Reference database | Country steward | Standardised form |
| type | `hospital`, `clinic`, `teaching hospital`, `other` | enum | M | reference DB | Reference database | Data Governance Lead | Teaching hospital flag required for US reporting |
| affiliation.start_date | Date the doctor started practising at the organisation | date | M | CRMs, reference DB | Earliest verified | Country steward | Not in the future |
| affiliation.end_date | Date the doctor stopped practising there | date | O | CRMs, reference DB | Most recent verified | Country steward | After start_date |

## PUBLICATION_BASIS

| Attribute | Definition | Type | M/C/O | Sources | Survivorship | Owner | Quality rule |
|---|---|---|---|---|---|---|---|
| country_code | Country whose disclosure rules apply | string(2) | M | consent system | n/a | Chief Compliance Officer | Phase 1 country |
| reporting_year | Year of the disclosure report | int | M | consent system | n/a | Chief Compliance Officer | Current or past year |
| basis | `consent`, `no consent`, `legal obligation` | enum | M | consent system, rules | **Most restrictive wins** on merge until a steward confirms | Chief Compliance Officer | `legal obligation` only where the law requires disclosure (France) |
| recorded_on | Date the basis was recorded | date | M | consent system | n/a | Chief Compliance Officer | Not in the future |
| evidence_ref | Reference to the signed consent or the legal basis | string(50) | C | consent system | n/a | Chief Compliance Officer | Required when basis = `consent` |

## PAYMENT

Held in spend and event systems; listed here because the master must link to it.

| Attribute | Definition | Type | M/C/O | Sources | Owner | Quality rule |
|---|---|---|---|---|---|---|
| payment_id | ID of the payment in the source system | string(30) | M | spend, events | System owner | Unique within source |
| source_record_id | HCP source record that received the payment | string(16) | M | MDM link | Transparency Analyst | Every in-scope payment is linked (BR-02) |
| amount, currency | Value of the transfer | decimal, ISO 4217 | M | spend, events | Transparency Analyst | Reconciles with finance |
| nature | Category used in disclosure | enum | M | spend, events | Chief Compliance Officer | Mapped to each regulator's categories |
| reporting_cycle | Disclosure cycle the payment belongs to, and whether it is open | string | M | reporting | Transparency Analyst | Used by the open-cycle rule (BR-07) |

## CANDIDATE_PAIR, STEWARD_DECISION, MERGE_EVENT

| Attribute | Definition | Type | M/C/O | Owner | Quality rule |
|---|---|---|---|---|---|
| candidate_pair.rule_applied | `NPI_EXACT`, `NPI_CONFLICT` or none | enum | M | Data Governance Lead | Set before scoring |
| candidate_pair.model_score | Calibrated score, 0 to 1 | decimal(4,3) | C | ML Team | Present when no rule applied |
| candidate_pair.model_version | Version of the model that scored the pair | string | C | ML Team | Registered version |
| candidate_pair.outcome | `auto merged`, `review`, `not duplicate`, `merged by rule` | enum | M | Data Governance Lead | Consistent with thresholds in force |
| steward_decision.reason_code | Reason from a fixed list, e.g. `same NPI`, `same address and name`, `different specialty`, `different person confirmed` | enum | M | Data Governance Lead | From the list |
| merge_event.actor | `rule`, `model` or steward ID | string | M | Data Governance Lead | Never empty |
| merge_event.threshold | Auto-merge threshold in force at the time | decimal(4,3) | C | Chief Compliance Officer | Present when actor = `model` |
| merge_event (all) | Immutable once written | n/a | n/a | Chief Compliance Officer | No update or delete (NFR-01) |

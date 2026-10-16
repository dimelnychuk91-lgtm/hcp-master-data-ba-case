# Traceability Matrix

> From business goals to requirements, decisions, stories, design artifacts and tests.
> Read left to right: why a requirement exists, where it is designed, how it is accepted.
> Fictional case.

## 1. Goals to requirements

| Goal | Business requirements | Non-functional |
|---|---|---|
| G1 Fewer disputes | BR-02, BR-06, BR-07, BR-08, BR-09, BR-10, BR-11, BR-13, BR-16 | NFR-01, NFR-02 |
| G2 Fewer duplicates | BR-01, BR-03, BR-04, BR-05, BR-06, BR-08, BR-11, BR-14, BR-15, BR-16 | NFR-04, NFR-05 |
| G3 Coordinated field work | BR-04, BR-12 | NFR-03, NFR-06 |

## 2. Requirements to design and acceptance

| Req | Short name | Source | Decision | User stories | Designed in | Accepted by |
|---|---|---|---|---|---|---|
| BR-01 | One golden record per doctor | S1, S5 | DEC-11 | US-04, US-05 | [Data model](../04_models/data_model.md) | US-05 AC 1–6 |
| BR-02 | Every payment linked to one golden record | S2, S6 | DEC-11 | US-10 | Data model §4, [DFD](../04_models/data_flows.md) P5 | US-10 AC 1–2 |
| BR-03 | No NPI, no US record | S3 | DEC-03 | US-03 | [API](../04_models/mdm_api.yaml) 422/409, [activity](../04_models/activity_search_before_create.md) | US-03 AC 1–3 |
| BR-04 | Search before create | S1, S7 | DEC-05 | US-01, US-02 | Activity diagram, [sequence 1](../04_models/sequence_diagrams.md), API search, 428 | US-01 AC 1–4, US-02 AC 1–3 |
| BR-05 | BioCo one-off load with dry run and rollback | S4, S5 | DEC-05 | US-04 | Sequence 2, [matching rules](../04_models/matching_rules.md) §3 | US-04 AC 1–4 |
| BR-06 | Rules for NPI, model for the rest, three outcomes | S5, S9 | DEC-06 | US-05 | Matching rules §1, [ML requirements](ml_requirements.md) §2 | US-05 AC 1–6, ML-AC-01–03 |
| BR-07 | Auto-merge ≤ 0.1% wrong; open-cycle payments to steward | S2 | DEC-07 | US-05 | Matching rules R5–R6, ML requirements §5 | US-05 AC 4, ML-AC-01, BRD §11 audit |
| BR-08 | Steward queue with reasons | S8 | DEC-09 | US-07, US-09 | Data model (candidate pair, decision), ML requirements §6 | US-07 AC 1–4, ML-AC-05 |
| BR-09 | Unmerge with payment reassignment | S2 | DEC-10 | US-08 | Matching rules §5, data model §4 | US-08 AC 1–3 |
| BR-10 | Consent or legal basis per country and year | S2, S10 | DEC-10 | US-11 | [Data dictionary](../04_models/data_dictionary.md) publication basis, matching rules §4 | US-11 AC 1–4 |
| BR-11 | Affiliations with dates | S6 | DEC-01 | US-15 | Data model (affiliation) | US-15 AC 1–3 |
| BR-12 | See the other field force | S1, S7 | DEC-11 | US-13 | API `alsoEngagedBy` | US-13 AC 1–2 |
| BR-13 | Extract from golden records, changes flagged | S2, S6 | DEC-10 | US-10, US-12 | DFD P5, data model (merge event) | US-10 AC 3, US-12 AC 1–2 |
| BR-14 | Data quality indicators | S1, S5 | DEC-04 | US-09, US-14 | [Governance](../05_governance/raci.md) §5 | US-09 AC 1–2, US-14 AC 1 |
| BR-15 | Named owner and local stewards | S5 | DEC-04 | n/a (organisational) | Governance §1–2 | Steering Committee sign-off of roles |
| BR-16 | Matching quality monitored, pause on drop | S2, S9 | DEC-06 | US-04, US-14 | ML requirements §8, governance §3 | US-14 AC 2 |
| NFR-01 | Immutable audit of merges | S2 | DEC-10 | US-06 | Data model (merge event), data dictionary | US-06 AC 1–3, ML-AC-07 |
| NFR-02 | Role-based access | S10 | DEC-10 | US-11 | API OAuth scopes, DFD §4 | Security test: access by role |
| NFR-03 | Sync to CRMs ≤ 15 min, to reporting daily | S4 | DEC-11 | n/a | DFD P4 | Integration test |
| NFR-04 | Search ≤ 2 s for 95% | S7 | DEC-05 | US-01 | API search, sequence 1 | US-01 AC 3, ML-AC-06 |
| NFR-05 | Training data use per DPO opinion | S10 | DEC-08 | n/a | ML requirements §3.1, §7 | ML-AC-08 |
| NFR-06 | 99.5% availability in field hours | S7 | DEC-11 | n/a | Activity diagram (search down) | Operational acceptance test |

## 3. Requirements to use cases, screens and UAT

| Req | Use case | Wireframe | UAT scenarios |
|---|---|---|---|
| BR-02 | UC-12 | | UAT-13 |
| BR-03 | UC-02, UC-03 | CRM search | UAT-04, UAT-05 |
| BR-04 | UC-01, UC-02 | CRM search | UAT-01, UAT-02, UAT-03, UAT-06 |
| BR-05 | UC-04, UC-05 | | UAT-15 |
| BR-06 | | | UAT-07, UAT-08 |
| BR-07 | UC-10 | Steward review | UAT-08, BRD §11 audit |
| BR-08 | UC-07 | Steward review | UAT-09 |
| BR-09 | UC-08 | | UAT-10 |
| BR-10 | UC-09 | | UAT-11, UAT-12 |
| BR-12 | UC-01 | CRM search | UAT-01 |
| BR-13 | UC-11, UC-12 | Steward review | UAT-13, UAT-14 |
| BR-14 | UC-06 | Steward review | UAT-16 |
| NFR-01 | UC-11 | | UAT-09, UAT-14 |
| NFR-02 | | | UAT-17 |
| NFR-04 | UC-01 | | UAT-01 |

Links: [use cases](../04_models/use_cases.md), [wireframes](wireframes.md), [UAT scenarios](uat_scenarios.md).

## 4. Coverage check

| Check | Result |
|---|---|
| Every goal has at least one requirement | Yes |
| Every business requirement traces to a goal and a stakeholder | Yes |
| Every requirement is designed in at least one artifact | Yes |
| Every **M** requirement has acceptance criteria | Yes. BR-15 is organisational and accepted by Steering Committee sign-off |
| Requirements without a user story | BR-15 (organisational), NFR-03, NFR-05, NFR-06 (tested outside stories) |
| Stories without a requirement | None |

## 5. Constraints in the design

| Constraint | Where it shows |
|---|---|
| C1 No US field screen changes in Q1 | Story releases 1a / 1b, business case roadmap, DEC-12 |
| C2 Budget set next cycle | Business case §7 cost ranges |
| C3 Both CRMs stay in phase 1 | DFD P4 publishes to both CRMs, API used by both |

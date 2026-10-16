# Business Requirements Document: Trusted HCP Master Data

> **Version:** 1.0, end of discovery (week 6). **Status:** submitted to the Steering Committee together with the [business case](../02_strategy/business_case.md).
> **Scope of this document:** option 3 from the business case (MDM hub with phase 0), phase 1 markets US, Germany, France.
> Fictional case.

## 1. Purpose

This document states what the business needs from the HCP master data solution, independent of the vendor that will be selected.
It is detailed enough for the MDM, data platform and ML teams to estimate the work.
Technical detail lives in the linked models: [data model](../04_models/data_model.md), [matching rules](../04_models/matching_rules.md), [ML requirements](ml_requirements.md), [MDM API](../04_models/mdm_api.yaml).

## 2. Business goals

| ID | Goal | Baseline | Target |
|---|---|---|---|
| G1 | Fewer disputes from doctors after publication of disclosure reports | 40 per cycle | < 10 |
| G2 | Fewer duplicate HCP records | ~12% of active records | < 2% |
| G3 | No uncoordinated calls on the same doctor by reps of both companies | not measured | 0 in phase 1 markets |

## 3. Scope

**In scope**
- HCP master data for doctors active in the US, Germany and France.
- The link between a doctor and the organisation where they practise (affiliation).
- Source systems: PharmaCo CRM, BioCo CRM, event management, expense and spend systems, third-party reference database.
- Consumers: both CRMs, disclosure reporting.
- One-off load and matching of BioCo records.
- Steward review process and data ownership roles.

**Out of scope**
- Full HCO domain: hospital hierarchies, pharmacies, distributors.
- Markets other than the US, Germany and France (phase 2).
- Replacing either CRM.
- Vendor selection (separate step after approval).
- Natural-language (LLM) explanations of matches (DEC-09).

## 4. Stakeholders

Full map with interests and engagement: [stakeholder map](../01_discovery/stakeholder_map.md).

| ID | Role | Interest in this document |
|---|---|---|
| S1 | VP Commercial Operations | Sponsor, Data Owner, approves scope |
| S2 | Chief Compliance Officer | Approves rules that affect disclosure |
| S3 | Former BioCo Head of Commercial | US field process, NPI rule |
| S4 | Enterprise Architect | Integration and platform fit |
| S5 | Data Governance Lead | Ownership, stewardship, data quality |
| S6 | Transparency Analyst | Disclosure reporting |
| S7 | Country Commercial Leads | Field adoption |
| S8 | Data Stewards | Review queue, labels |
| S9 | ML Team | Matching model |
| S10 | Data Protection Officer | Lawful use of personal data |

## 5. Current state (AS-IS), in short

HCP records are created independently in each system. Once a year the Transparency team exports payments into spreadsheets, matches doctors by surname and city, reviews about 3,000 doubtful pairs by hand and uploads the result to regulator portals. The cycle takes about six weeks and keeps no record of why records were matched.
Detailed process: [AS-IS and TO-BE processes](../04_models/process_as_is_to_be.md).

## 6. Business requirements

Priority: **M** must, **S** should, **C** could (MoSCoW, agreed with S1 and S2).

| ID | Requirement | Priority | Goal | Source | Decision |
|---|---|---|---|---|---|
| BR-01 | The organisation shall hold one golden record for each doctor in scope, linked to every source record that describes that doctor | M | G2 | S1, S5 | DEC-11 |
| BR-02 | Every payment or transfer of value in disclosure scope shall be linked to exactly one golden record before the disclosure report is produced | M | G1 | S2, S6 | DEC-11 |
| BR-03 | A US doctor record shall not be created without a valid NPI | M | G2 | S3 | DEC-03 |
| BR-04 | Before a new doctor is created in either CRM, the user shall be shown existing records that may describe the same doctor | M | G2, G3 | S1, S7 | DEC-05 |
| BR-05 | BioCo doctor records shall be loaded and matched once, with a dry run, sampled manual review and the ability to roll back the load | M | G2 | S4, S5 | DEC-05 |
| BR-06 | Records with the same NPI shall be merged by rule. All other candidate pairs shall be scored and routed to one of three outcomes: merge automatically, review by a steward, not a duplicate | M | G1, G2 | S5, S9 | DEC-06 |
| BR-07 | Automatic merges by the model shall produce at most 1 wrong merge per 1,000. A model-scored pair that touches a record with payments in an open reporting cycle shall go to a steward. Merges by an exact national identifier (NPI, RPPS) proceed automatically and notify the Transparency team | M | G1 | S2 | DEC-07 |
| BR-08 | Stewards shall review candidate pairs in a queue that shows why the pair was proposed, and record a decision with a reason | M | G1, G2 | S8 | DEC-09 |
| BR-09 | A steward shall be able to undo a wrong merge, and payments linked to the merged record shall be reassigned to the correct doctor | M | G1 | S2 | DEC-10 |
| BR-10 | The golden record shall carry each doctor's consent status for individual publication per country and reporting year. Where disclosure is a legal obligation (France), the legal basis shall be recorded instead of consent | M | G1 | S2, S10 | DEC-10 |
| BR-11 | The golden record shall hold the doctor's current affiliations to organisations, with start and end dates | S | G1, G2 | S6 | DEC-01 |
| BR-12 | A rep shall see whether the doctor is also engaged by the other company's field force, and who the contact owner is | S | G3 | S1, S7 | DEC-11 |
| BR-13 | The disclosure extract shall be produced from golden records, and the Transparency team shall see which merges and unmerges changed a doctor's total since the last extract | M | G1 | S2, S6 | DEC-10 |
| BR-14 | The Data Owner shall see data quality indicators: duplicate rate, review queue size and age, automatic merge accuracy from sampled audits | S | G2 | S1, S5 | DEC-04 |
| BR-15 | Each phase 1 country shall have a named local data steward, and the Data Owner role shall be formally assigned | M | G2 | S5 | DEC-04 |
| BR-16 | Matching quality shall be monitored after go-live, and a drop in quality shall trigger review of thresholds before further automatic merges | S | G1, G2 | S2, S9 | DEC-06 |

## 7. Non-functional requirements

| ID | Requirement | Priority | Source | Decision |
|---|---|---|---|---|
| NFR-01 | Every merge and unmerge is logged: who or what made it, when, on what basis, model score, model version and threshold in force. The log cannot be edited | M | S2 | DEC-10 |
| NFR-02 | Access to HCP records is role-based: reps see doctors in their territory, stewards see their country queue, consent data is visible only to Compliance and stewards | M | S10 | DEC-10 |
| NFR-03 | Changes to a golden record reach both CRMs within 15 minutes and the reporting store within one day | S | S4 | DEC-11 |
| NFR-04 | Search before create returns candidates within 2 seconds for 95% of searches, so it does not slow down field work | M | S7 | DEC-05 |
| NFR-05 | Use of EU doctors' personal data for model training follows the DPO's written opinion: purpose limited to matching, minimum attributes, defined retention | M | S10 | DEC-08 |
| NFR-06 | Search and create are available during field working hours in all phase 1 time zones, 99.5% per month | S | S7 | DEC-11 |

## 8. Constraints

| ID | Constraint | Effect |
|---|---|---|
| C1 | No changes to US field CRM screens from January to March (product launch) | US search before create starts in Q2 (DEC-12) |
| C2 | Implementation budget is set in the next budget cycle; discovery provides a cost range only | Business case section 7 |
| C3 | Both CRMs stay in use during phase 1 | Integration in both directions (NFR-03) |

## 9. Assumptions

- The third-party reference database licence covers Germany and France.
- NPI values in BioCo records are valid; a sample check is planned in phase 0.
- Stewards for the central team can be staffed from the current Transparency and Commercial Operations teams.

## 10. Dependencies

- DPO written opinion before ML requirements are final (NFR-05).
- CCO written confirmation of the 0.1% tolerance (BR-07).
- Vendor selection before detailed design.

## 11. Acceptance

The business accepts phase 1 when:
- all **M** requirements pass UAT using the acceptance criteria in [user stories](user_stories.md);
- a sampled audit of 1,000 automatic merges finds no more than 1 wrong merge;
- the first disclosure extract from golden records reconciles with the payment systems.

End-to-end acceptance scenarios: [UAT scenarios](uat_scenarios.md). Traceability from goals to tests: [traceability matrix](traceability_matrix.md).

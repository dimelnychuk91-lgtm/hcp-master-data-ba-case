# Decision Log

> Decisions made during the six-week discovery. Each entry records the context, the decision, the alternatives we rejected and why, who decided, and what it traces to.
> Goals G1–G3 and options are defined in the [business case](business_case.md). Findings F1–F6 are in the [interview summaries](../01_discovery/interview_summaries.md).
> Fictional case.

## Index

| ID | Decision | Status | Decided by | Week |
|---|---|---|---|---|
| [DEC-01](#dec-01-scope-hcp-plus-affiliation-only) | Scope: HCP master data plus HCP-to-HCO affiliation only | Agreed | VP Commercial Ops | 1 |
| [DEC-02](#dec-02-phase-1-markets-us-germany-france) | Phase 1 markets: US, Germany, France | Agreed | VP Commercial Ops, CCO | 1 |
| [DEC-03](#dec-03-npi-as-the-us-reference-key) | BioCo NPI is the US reference key; "no NPI, no record" for US | Agreed | Data Governance Lead, former BioCo Head of Commercial | 3 |
| [DEC-04](#dec-04-data-ownership-model) | Data ownership model with Data Owner, stewards, Compliance veto | Agreed | Steering Committee | 4 |
| [DEC-05](#dec-05-matching-in-two-modes) | Matching in two modes: initial load and steady state | Agreed | Data Governance Lead, Enterprise Architect | 4 |
| [DEC-06](#dec-06-hybrid-matching-rules-plus-ml) | Hybrid matching: rules for exact NPI, ML model for the rest | Agreed | Enterprise Architect, ML Team, CCO | 4 |
| [DEC-07](#dec-07-auto-merge-tolerance) | Auto-merge tolerance 0.1%; model-scored pairs with open-cycle payments always to a steward | **Pending written confirmation** | CCO | 5 |
| [DEC-08](#dec-08-training-labels) | Training labels from a steward sample; past files as weak labels only | Agreed | ML Team, Data Governance Lead | 4 |
| [DEC-09](#dec-09-no-llm-explanations-in-phase-1) | Merge explanations from model features; LLM explanations rejected for phase 1 | Agreed | CCO, ML Team | 5 |
| [DEC-10](#dec-10-mandatory-non-functional-requirements) | Mandatory non-functional requirements for audit and privacy | Agreed | CCO, DPO | 5 |
| [DEC-11](#dec-11-recommended-option) | Recommend option 3 (MDM hub) with phase 0 | **Pending Steering Committee** | Steering Committee | 6 |
| [DEC-12](#dec-12-phasing-around-the-q1-launch) | Phasing around the Q1 US launch freeze | **Pending Steering Committee** | Steering Committee | 6 |

---

## DEC-01. Scope: HCP plus affiliation only

**Context.** Disclosure reports are about individual doctors, but US reporting also covers teaching hospitals, and a doctor's place of practice is one of the strongest matching attributes.

**Decision.** In scope: HCP master data and the link "this doctor works at this organisation". Out of scope: the full HCO domain (hospital hierarchies, pharmacies, distributors).

**Alternatives rejected.**
- *HCP only:* weaker matching without place of practice; teaching hospitals in US reports left unmanaged.
- *Full HCP and HCO:* roughly doubles the scope and the stakeholder group, with no direct link to G1–G3.

**Traces to:** G1, G2.

## DEC-02. Phase 1 markets: US, Germany, France

**Context.** The company operates in about 40 markets with different disclosure rules.

**Decision.** Phase 1 covers the US, Germany and France.

**Alternatives rejected.**
- *US only:* covers one regulatory logic and misses the EU consent problem, so phase 2 would need new requirements.
- *All markets:* cannot be specified to estimation quality in six weeks.

**Why these three:** the US brings Open Payments and all BioCo records; France brings disclosure by law on a public government platform; Germany brings consent-based disclosure with aggregate publication when consent is missing.

**Traces to:** G1, G2.

## DEC-03. NPI as the US reference key

**Context.** BioCo keys US doctors on NPI and does not allow a record without one; its duplicate rate is about 2% against about 12% overall (F4). PharmaCo uses internal IDs.

**Decision.** NPI is the reference key for US doctors in the master. The rule "no NPI, no record" becomes a master data rule for the US.

**Alternatives rejected.**
- *PharmaCo internal ID as the key:* no external validation, and it is exactly the identifier that let duplicates appear.
- *Third-party reference database ID only:* adds a licence dependency and does not cover all doctors that reps meet.

**Effect on stakeholders:** the strongest objection of the former BioCo Head of Commercial (T1) becomes his contribution to the solution.

**Traces to:** G2, root cause layer 1.

## DEC-04. Data ownership model

**Context.** Nobody owns HCP records today (root cause layer 3).

**Decision.**

| Role | Who | Responsibility |
|---|---|---|
| Data Owner | VP Commercial Operations | Decides rules and budget for HCP master data |
| Key consumer with veto | Chief Compliance Officer | Veto on rules that affect disclosure reports |
| Data Stewards | Central team plus one local steward per phase 1 country | Review doubtful matches, maintain rules, label pairs |
| Custodian | IT | Runs the platform, not responsible for content |

**Alternatives rejected.**
- *IT as owner:* IT runs the platform but cannot decide what a correct doctor record is.
- *Compliance as owner:* Compliance consumes the data but does not create it; owning it would slow the field without fixing entry.

**Traces to:** G1, G2, root cause layer 3. Detailed RACI: [governance](../05_governance/raci.md).

## DEC-05. Matching in two modes

**Context.** Merging the BioCo base is a one-off load of many records; new doctors from the field arrive a few at a time every day. The two problems need different controls.

**Decision.**
- *Initial load:* batch matching, confidence thresholds, sampled manual review, rollback plan.
- *Steady state:* search before create. A rep cannot create a doctor until the system has shown similar existing records.

**Alternative rejected.** *One matching process for both:* either too slow for the field or too loose for a bulk load.

**Traces to:** G2, G3, root cause layer 2.

## DEC-06. Hybrid matching: rules plus ML

**Context.** In the US an exact NPI match is close to certain. EU records have no NPI, and names, spellings and addresses vary. The annual reconciliation reviews about 3,000 doubtful pairs by hand (F5).

**Decision.** Exact NPI matches merge by rule, with no model. An ML model scores the remaining candidate pairs into three bands: auto-merge, steward review, not a duplicate.

**Alternatives rejected.**
- *Rules only:* EU and fuzzy cases fall into a manual queue of thousands of pairs per cycle.
- *ML only:* adds model risk where a deterministic key already works, and makes simple merges harder to explain to auditors.

**Traces to:** G1, G2. Requirements: [ML requirements](../03_requirements/ml_requirements.md), [matching rules](../04_models/matching_rules.md).

## DEC-07. Auto-merge tolerance

**Context.** In the last cycle two different doctors with the same name were merged and a payment was reported against the wrong person (F1). For Compliance a false merge is worse than a missed duplicate.

**Decision.** At most 1 false merge per 1,000 automatic merges by the model (0.1%). A model-scored pair that touches a record with reported payments in an open reporting cycle goes to a steward, whatever the score. Merges by an exact national identifier (same NPI or RPPS) still proceed automatically, because the identifier is certain, and the Transparency team is notified so the report in progress reflects the change.

**Alternatives rejected.**
- *No automatic merges:* steward workload would not fit the team size.
- *Looser tolerance (1%):* about 10 wrong-person merges per 1,000, not acceptable after the incident.
- *Send every open-cycle merge to a steward, including exact NPI matches:* adds review work for merges that are certain, and delays the report without reducing risk.

**Trade-off made explicit:** a stricter threshold means more pairs in the review band and more steward hours. The band will be sized to steward capacity.

**Status:** agreed verbally by the CCO, written confirmation pending.

**Traces to:** G1.

## DEC-08. Training labels

**Context.** Past reconciliations left final files but no record of why records were matched and no examples of "not a duplicate" (F5).

**Decision.** Stewards label a sample of record pairs in phase 0. Past reconciliation files are used only as weak labels.

**Alternative rejected.** *Train on past reconciliation results only:* labels are incomplete and one-sided, and they include the wrong-person merge.

**Traces to:** G2. Dependency: DPO opinion on using HCP data for training (DEC-10).

## DEC-09. No LLM explanations in phase 1

**Context.** Stewards need to see why two records were proposed as a match.

**Decision.** Explanations come directly from the model's features: NPI match, address match, specialty match, name similarity.

**Alternative rejected.** *An LLM writes the explanation in natural language:* useful for readability, but generated text can be inaccurate, and in a compliance setting every explanation must be exactly what the model used. Can be revisited after phase 1.

**Traces to:** G1.

## DEC-10. Mandatory non-functional requirements

**Context.** Merges change what is reported to regulators and to the public; EU doctors' data is personal data under GDPR.

**Decision.** The following are mandatory in phase 1:
- audit trail of every merge and unmerge: who or what, when, model score, model version, threshold;
- unmerge of wrongly merged records, with correction of linked payments;
- tracking of each doctor's consent to individual publication;
- role-based access to HCP records;
- agreed refresh frequency from master to consuming systems.

**Alternative rejected.** *Leave NFRs to the implementation team:* audit and consent are business rules, not technical choices.

**Traces to:** G1.

## DEC-11. Recommended option

**Context.** Four options compared on six weighted criteria agreed before scoring. See the [business case](business_case.md), sections 4–6.

**Decision.** Recommend option 3, MDM hub with phase 0. Weighted score 3.95 against 3.30 (tactical) and 2.65 (CRM consolidation).

**Alternatives rejected.**
- *Do nothing:* risk grows every cycle; board commitment cannot be met.
- *Tactical only:* cleans duplicates once a year, does not stop new ones.
- *CRM consolidation:* one CRM, but duplicates return without matching and ownership; most disruptive for US reps in the launch year.

**Limit of the recommendation:** if the committee only wants a safer next report, the tactical option is rational (sensitivity, business case section 6).

**Traces to:** G1, G2, G3.

## DEC-12. Phasing around the Q1 launch

**Context.** A new oncology product launches in the US in Q1; no changes to US field CRM screens from January to March (constraint C1).

**Decision.** Q1: MDM hub set-up, BioCo batch load, EU markets. Q2: US search before create.

**Alternative rejected.** *Start with the US, where the data and the penalties are:* would collide with the launch and turn both the sponsor and the former BioCo Head of Commercial against the project.

**Traces to:** G2, G3.

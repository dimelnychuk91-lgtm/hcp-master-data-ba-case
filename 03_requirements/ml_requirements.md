# ML Requirements: HCP Matching Model

> **For:** ML / Data Science team (S9). **Approvers:** Chief Compliance Officer (S2) for thresholds, Data Governance Lead (S5) for labels, DPO (S10) for use of personal data.
> Business context: [BRD](BRD.md), decisions [DEC-06 to DEC-09](../02_strategy/decision_log.md). Rule logic outside the model: [matching rules](../04_models/matching_rules.md).
> Fictional case.

## 1. Business problem

The same doctor exists as several records across five systems. When one doctor is split across records, their payment total is reported in parts and the doctor disputes it. When two different doctors are merged, a payment is reported against the wrong person, which is a legal risk.

Exact NPI matches are handled by a rule (BR-06). **The model handles everything else:** EU records without NPI, US records where NPI is missing on one side, and fuzzy cases where names, spellings and addresses differ.

## 2. What the model must do

For each candidate pair of HCP records, return:
- a **score** from 0 to 1 that behaves like a probability that both records describe the same doctor (calibrated, see section 6);
- the **attributes that contributed** to the score, for the steward screen (BR-08, DEC-09).

The model does **not** decide. The score is turned into an outcome by business-owned thresholds (section 5).

The same model serves both matching modes (DEC-05):
- **Batch:** scoring all candidate pairs in the BioCo load.
- **Online:** ranking candidates for search before create within the 2-second limit (NFR-04).

## 3. Data

### 3.1 Sources and attributes

Completeness figures are estimates from the discovery data profiling sample.

| Attribute | Sources | Completeness | Quality issues found | Use in model |
|---|---|---|---|---|
| First and last name | all | ~100% | Spelling variants (Müller / Mueller), transliteration, titles inside the name field ("Dr. Prof.") | Yes, after normalisation |
| NPI (US) | BioCo CRM, PharmaCo CRM, spend | BioCo ~100%, PharmaCo ~60% | Missing in PharmaCo records created before 2020 | Rule first; as a feature when one side has it |
| RPPS (France) | reference database, PharmaCo CRM | ~70% | Not captured in the event system | Rule first; feature otherwise |
| Reference database ID | PharmaCo CRM | ~85% EU, ~40% US | Not present in BioCo | Feature |
| Address of practice | all | ~95% | Outdated after moves; free-text formats differ by system | Yes, after standardisation |
| Specialty | all | ~90% | Each system uses its own code list | Yes, after mapping to one list |
| Affiliation (organisation) | CRMs, reference database | ~75% | Organisation names not standardised | Yes |
| Email, phone | CRMs | < 30% | Sparse, often shared office numbers | **No.** Low value and sensitive (data minimisation, NFR-05) |
| Date of birth | not held | n/a | n/a | **No.** Not collected, not needed |

### 3.2 Data preparation required before training

- Name normalisation: remove titles, unify diacritics and transliteration.
- Address standardisation per country.
- One specialty code list, with a mapping table owned by the Data Governance Lead.
- Organisation name standardisation for affiliations.

These are data quality requirements on the input, not modelling tasks. They are owned by the data platform team and are a dependency for the ML team.

### 3.3 Candidate generation (blocking)

Comparing every record with every other is not feasible. Candidate pairs are generated within the same country by surname phonetic key and postcode area.
**Requirement:** blocking must keep at least 99% of true duplicate pairs from the labelled set. A duplicate lost at blocking can never be found by the model.

## 4. Labels: what is the right answer

**Right answer:** a pair is a duplicate if both records describe the same natural person practising as a doctor.

**Problem:** past reconciliations left no record of why records were matched, and no examples of pairs that were judged *not* to be the same doctor (F5). They also contain the known wrong-person merge (F1).

**Decision (DEC-08):**
- Past reconciliation results are used **only as weak labels**, for example to pre-select pairs for labelling.
- Stewards label **about 3,000 pairs in phase 0**, stratified by country and by score range, including hard cases: same name and city, different doctors.
- **10% of pairs are labelled twice** by different stewards. Agreement must be at least 95%; disagreements are resolved by the Data Governance Lead and used to improve the labelling guide.
- After go-live, every steward decision becomes a new label (US-07).

## 5. Thresholds and human in the loop

Two thresholds split pairs into three bands:

| Band | Outcome | Who sets the threshold |
|---|---|---|
| Score ≥ auto-merge threshold | Merged automatically | CCO, on the ML team's proposal |
| Between the two thresholds | Steward review | Data Owner and Data Governance Lead, within steward capacity |
| Score < review threshold | Not a duplicate | Data Governance Lead |

**Override rules that the model cannot bypass** (see [matching rules](../04_models/matching_rules.md)):
- different valid NPIs or different valid RPPS: never merge;
- payments in an open reporting cycle: a model-scored pair always goes to a steward (BR-07).

### 5.1 Model metrics in business terms

| Model metric | What it means for the business | Target |
|---|---|---|
| **Precision of the auto-merge band** | Out of 1,000 automatic merges, how many put two different doctors together. Each one can mean a payment reported on the wrong person | ≥ 99.9% (DEC-07) |
| **Recall of auto + review bands** | Share of true duplicates the system catches. Each missed one keeps a doctor's total split across records, which leads to disputes (G1) and keeps the duplicate rate up (G2) | ≥ 95% |
| **Size of the review band** | Steward hours per week | Fits steward capacity (section 5.2) |

**The trade-off the business decides:** lowering the review threshold catches more duplicates but costs more steward hours. Raising the auto-merge threshold reduces wrong merges but moves more pairs into review. The ML team shows these curves; the business picks the point.

### 5.2 Steward capacity check (planning assumption)

- One steward reviews about 40 pairs per working day with the side-by-side screen.
- Expected steady-state review volume: to be measured in the first month; the review threshold is set so that the queue does not grow week on week.
- BioCo initial load: review volume is planned as a one-off peak with temporary steward support.

## 6. Quality requirements for the model

- **Calibration:** among pairs scored around 0.9, about 90% should be true duplicates. Thresholds only mean something if scores are calibrated.
- **Explainability:** for every score, the top contributing attributes are returned in plain terms for stewards (same NPI, similar name, same address, different specialty). No LLM-generated text (DEC-09).
- **Consistency across countries:** precision and recall are reported **per country**. Name similarity may work worse for some name origins and transliterations; a country below target blocks automatic merging in that country, not everywhere.
- **Latency:** online scoring fits within the 2-second search limit (NFR-04).

## 7. Privacy and audit

- Training on EU doctors' data only after the DPO's written opinion (NFR-05): purpose limited to matching, only the attributes marked "Yes" in 3.1, defined retention of training sets.
- Every automatic merge logs model score, model version and thresholds in force (NFR-01), so any merge can be explained and reversed later.
- Model versions are kept, so a past decision can be reproduced.

## 8. Monitoring after go-live

| What | How often | Trigger |
|---|---|---|
| Sampled audit of automatic merges | Monthly, 500 merges | More than 1 wrong in 1,000 (cumulative): pause automatic merging in that country, review thresholds (BR-16) |
| Steward overrides of model suggestions | Weekly | Override rate rising for 3 weeks in a row: review the model |
| Score distribution of new pairs | Weekly | Clear shift from the training distribution: retraining review |
| Unmerges caused by automatic merges | Monthly | Any unmerge in a disclosure-relevant record: root cause review |

**A note on proving 0.1%.** A sample of 1,000 can show a point estimate of 1 in 1,000 but cannot prove the true rate is below it. With zero errors in about 3,000 merges the upper 95% bound reaches 0.1%. The go-live gate agreed with the CCO is the point estimate on 1,000 merges (BRD section 11); confidence then builds through the monthly audits.

## 9. Acceptance criteria for the model

| ID | Criterion |
|---|---|
| ML-AC-01 | On a held-out labelled set, precision of the auto-merge band is at least 99.9% in each phase 1 country |
| ML-AC-02 | On the same set, recall of auto + review bands is at least 95% in each country |
| ML-AC-03 | Blocking keeps at least 99% of true duplicate pairs |
| ML-AC-04 | Scores are calibrated: in each score decile, observed duplicate rate is within 5 points of the mean score |
| ML-AC-05 | Each score comes with the top contributing attributes, readable by a steward without explanation |
| ML-AC-06 | Online scoring for search before create meets the 2-second limit for 95% of searches |
| ML-AC-07 | Model version, score and thresholds are logged for every automatic merge |
| ML-AC-08 | The DPO has confirmed in writing that training data use complies with the agreed purpose and attributes |

## 10. Open questions

- Steward capacity per country after the BioCo load.
- Whether the reference database vendor allows its IDs to be used as model features under the licence.

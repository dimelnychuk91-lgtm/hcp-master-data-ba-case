# Data Governance: Ownership, RACI and Operating Rhythm

> Implements DEC-04 (ownership model) and BR-15. Removes root cause layer 3: nobody owned HCP records.
> Fictional case.

## 1. Roles

| Role | Held by | In one sentence |
|---|---|---|
| **Data Owner** | VP Commercial Operations | Decides what a correct HCP record is and funds the work |
| **Compliance (veto)** | Chief Compliance Officer | Can stop any rule that would put disclosure at risk |
| **Data Governance Lead** | Data Governance Lead | Runs the rules, the stewards and data quality day to day |
| **Central stewards** | 2–3 people from Transparency and Commercial Ops | Review queues, maintain code lists, train local stewards |
| **Local stewards** | One per phase 1 country (US, DE, FR) | Decide local cases, know local names, addresses and rules |
| **ML Team** | Data Science | Builds, monitors and proposes thresholds for the matching model |
| **Data Protection Officer** | DPO | Confirms lawful use of doctors' personal data |
| **Custodian** | IT / data platform | Runs the platform and integrations; not responsible for content |
| **Field reps** | Both field forces | Search before create, enter data correctly |

## 2. RACI

**R** responsible (does it) · **A** accountable (one per row, signs off) · **C** consulted · **I** informed

| Activity | Data Owner | CCO | DGL | Central stewards | Local stewards | ML Team | DPO | IT | Reps |
|---|---|---|---|---|---|---|---|---|---|
| Define HCP data standards and code lists | A | C | R | C | C | I | | I | |
| Approve matching rules R1–R8 | A | C | R | C | C | C | | I | |
| **Set auto-merge threshold** | C | **A** | R | I | I | C | | I | |
| Set review threshold | A | C | R | C | C | C | | I | |
| Create a new doctor | | | I | | | | | | R, A |
| Review candidate pairs | | | A | R | R | I | | | |
| Unmerge a wrong merge | | I | A | R | R | I | | | |
| Override a golden record value by hand | | | A | R | R | | | | |
| Record consent or legal basis | | A | I | R | R | | | | |
| Approve use of data for model training | C | C | C | | | R | **A** | I | |
| Retrain and release a model version | I | C | A | | | R | C | C | |
| Run monthly sampled audit of auto-merges | I | I | A | R | R | C | | | |
| Pause automatic merging after a failed audit | I | C | A, R | I | I | C | | R | |
| Run and monitor integrations | | | I | | | | | A, R | |
| Produce disclosure extract | | A | C | C | | | | I | |

*CCO keeps accountability for the extract because it is a compliance output; production is done by the Transparency team.*

## 3. Change control for rules and thresholds

1. Change proposed by any role, with a reason and the expected effect on precision, recall and steward hours.
2. DGL assesses impact; ML Team runs it on the labelled set.
3. Approval by the accountable role in the RACI. Threshold for auto-merge: CCO.
4. Change logged with an effective date. Every later merge records the threshold in force (NFR-01).
5. No threshold change during the last four weeks before a disclosure submission, unless the CCO asks for it.

## 4. Operating rhythm

| When | What | Who |
|---|---|---|
| Daily | Work country review queues | Stewards |
| Weekly | Queue size and age, steward overrides of model suggestions | DGL |
| Monthly | Data quality report: duplicate rate, queue health, sampled audit of 500 auto-merges | DGL to Data Owner and CCO |
| Before each reporting cycle | Freeze thresholds, list all merges and unmerges affecting open-cycle payments | DGL, Transparency team |
| Quarterly | Governance board: rule changes, model performance, open risks | Data Owner (chair), CCO, DGL, ML Team, DPO |

## 5. Data quality indicators

| Indicator | Definition | Target | Goal |
|---|---|---|---|
| Duplicate rate | Active golden records estimated to be duplicates, from a monthly profiling sample | < 2% | G2 |
| Auto-merge accuracy | Wrong merges per 1,000 in the monthly audit, cumulative | ≤ 1 | G1 |
| Queue age | Pairs older than 5 working days | < 50 per country | G2 |
| Disputes | Doctor disputes after publication, per cycle | < 10 | G1 |
| Linked payments | Share of in-scope payments linked to a golden record at extract time | 100% | G1 |
| US NPI coverage | US golden records with a verified NPI | 100% | G2 |
| Search usage | Share of new doctors created after a search | 100% (enforced) | G2, G3 |

## 6. Real-world note

The author ran the same model in travel-tech: one team owned the stop directory, rules were written in a team regulation, and only that team could create stops. It worked because ownership was clear, not because the tools were advanced.

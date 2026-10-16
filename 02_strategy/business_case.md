# Business Case: Trusted HCP Master Data

> **For:** Steering Committee, end of week 6 of discovery.
> **Decision requested:** approve option 3 (MDM hub with phase 0) for the next budget cycle, with the cost range below.
> Fictional case: company figures and costs are invented estimates. Regulatory facts are sourced.

## 1. Executive summary

PharmaCo reports payments to doctors from HCP data that is duplicated across two CRMs and three source systems.
Last reporting cycle this produced 40 disputes from doctors and one payment reported against the wrong person.
The annual manual reconciliation takes about six weeks and leaves no record of its decisions.

We compared four options. **We recommend option 3: an MDM hub that holds the golden record for HCPs, with a phase 0 of tactical fixes before the next reporting cycle.**
It is the only option that removes the root cause, and it scores highest in the weighted comparison (3.95 out of 5).
It is also the most expensive. Section 6 shows when a cheaper option would be the better choice.

## 2. Problem and its cost

**Root cause** (from discovery, three layers):

1. No shared identifier: BioCo keys US doctors on NPI, PharmaCo uses internal IDs and a third-party reference database, the EU has no universal doctor number.
2. Manual entry in the field: a rep cannot find a doctor and creates a new record.
3. No data ownership: nobody decides who may create or change an HCP record.

**Cost of the status quo:**

| Impact | Today | Source |
|---|---|---|
| Disputes after publication | 40 per cycle | CCO interview |
| Wrong-person reporting | 1 known incident | CCO interview |
| Manual reconciliation | ~6 weeks, ~3,000 pairs reviewed by hand, no decision log | Observation |
| Duplicate rate, active HCP records | ~12% (sample estimate) | Data profiling |
| Reps of both companies calling on the same doctor | not measured today | VP interview |

**Regulatory exposure (US).** Under Open Payments, failure to report accurately can cost $1,000–$10,000 per payment, up to $150,000 per annual submission. A knowing failure costs $10,000–$100,000 per payment, up to $1,000,000 per year. Amounts are adjusted annually. ([CMS: Audits and Penalties](https://www.cms.gov/openpayments/program-participants/reporting-entities/audits-and-penalties))
A repeated, known data problem moves the company closer to the "knowing" category every year it stays unfixed.

**EU.** In France disclosure is a legal obligation with publication on a government platform. In most other EFPIA markets, including Germany, individual publication depends on the doctor's consent, otherwise amounts are published in aggregate. ([EFPIA Disclosure Q&A, 2025](https://www.efpia.eu/media/i0yiz30d/disclosure-qa-june-2025.pdf)) A duplicate can therefore also split one doctor's consent status across records.

## 3. Goals

| ID | Goal | Baseline | Target | Owner |
|---|---|---|---|---|
| G1 | Fewer disputes after publication | 40 per cycle | < 10 | CCO |
| G2 | Fewer duplicate HCP records | ~12% | < 2% | Data Owner (VP Commercial Ops) |
| G3 | No uncoordinated calls by reps of both companies | not measured | 0 in phase 1 markets | VP Commercial Ops |

Timeline constraint: the sponsor committed to the board to deliver one customer view across both field forces by the end of the next fiscal year.

## 4. Options

| | Option | What it is |
|---|---|---|
| 0 | **Do nothing** | Keep the annual manual reconciliation. Baseline for comparison |
| 1 | **Tactical** | Keep both CRMs. Add a matching tool and a decision log to the annual reconciliation |
| 2 | **CRM consolidation** | Migrate BioCo onto the PharmaCo CRM and deduplicate during migration |
| 3 | **MDM hub + phase 0** | A dedicated MDM platform holds the HCP golden record. Both CRMs coexist and consume it. Hybrid matching: rules for exact NPI matches, an ML model for the rest. Phase 0 delivers option 1 fixes before the next reporting cycle |

**Option 0 is not acceptable:** the risk grows every cycle (section 2), and the board commitment cannot be met.

## 5. Comparison

**Criteria and weights** were agreed with the sponsor and the CCO in the options workshop (week 5), **before any option was scored**. Scores were then proposed by the BA and challenged in the same session.

| Criterion | Weight | Option 1 Tactical | Option 2 CRM consolidation | Option 3 MDM hub |
|---|---|---|---|---|
| Removes the root cause | 25% | 1 | 2 | 5 |
| Reduces reporting risk | 25% | 3 | 3 | 5 |
| Time to first value | 15% | 5 | 3 | 3 |
| Cost | 15% | 5 | 3 | 2 |
| Low disruption to field teams | 10% | 5 | 1 | 4 |
| Fit with target architecture | 10% | 3 | 4 | 3 |
| **Weighted score** | **100%** | **3.30** | **2.65** | **3.95** |

Scores: 1 = poor, 5 = strong.

**Why the scores:**

- **Option 1** is fast and cheap, and makes the next report safer. But duplicates keep being created every day; the tool only cleans them once a year.
- **Option 2** gives one CRM, which the sponsor values. But a CRM without matching rules and ownership creates new duplicates within a year. Migrating US reps in the launch year is the most disruptive path, and it throws away BioCo's working NPI control.
- **Option 3** addresses all three root cause layers: a shared key (golden record with NPI as US reference), search before create at entry, and a named owner with stewards. Phase 0 brings part of option 1's early value, but the hub itself takes longer to deliver, so time to first value scores 3, not 5. It is the most expensive, and the Enterprise Architect is cautious about adding a platform.

## 6. Sensitivity: when would we recommend something else?

The recommendation depends mostly on how much the committee values removing the root cause against cost.

- If weight moves from "removes the root cause" to "cost", option 1 catches up with option 3 when root cause drops to about **16%** and cost rises to about **24%**.
- In plain words: **if the committee only wants a safer next report and accepts the annual clean-up as permanent, option 1 is the rational choice.** If the goal is to stop the problem from coming back, option 3 is.
- Option 2 does not win under any reasonable weighting, because it scores low on both risk and disruption.

## 7. Costs and benefits (order of magnitude)

| | Option 1 | Option 2 | Option 3 |
|---|---|---|---|
| One-off cost, 18 months | €0.3–0.5M | €1.2–1.8M | €2.0–3.0M |
| Running cost per year | low | CRM licences for BioCo users | MDM subscription + 3–4 stewards |
| Main benefit | Safer next report | One CRM | Problem stops recurring, one customer view |

Estimates are ranges, not quotes. Vendor selection is a separate step after approval.

**Expected benefits of option 3:** reconciliation cycle from ~6 weeks to ~2; disputes and duplicates to the targets in section 3; one plan per doctor across both field forces; an audit trail for every merge.

## 8. Recommended roadmap

| Phase | When | Scope | Goal served |
|---|---|---|---|
| 0 | Before next reporting cycle | Matching tool and decision log for the annual reconciliation; stewards label a sample of record pairs for the model | G1 |
| 1a | Q1 | MDM hub set-up; batch load and matching of BioCo records; EU markets (Germany, France). **No changes to US field screens** (Q1 launch) | G1, G2 |
| 1b | Q2 | US search before create; NPI as US reference key; both CRMs consume the golden record | G2, G3 |
| 2 | After phase 1 review | Remaining markets | G2, G3 |

## 9. Key risks

| Risk | Impact | Mitigation |
|---|---|---|
| Wrong auto-merges | Payment reported on the wrong doctor | Auto-merge tolerance of 0.1%; model-suggested merges touching payments in an open cycle always go to a steward; unmerge and audit trail |
| Weak training labels for the matching model | Model quality below target | Steward labelling in phase 0; past reconciliation files used only as weak labels |
| BioCo field resistance | Low adoption in the US | BioCo NPI rule kept and made a master data rule; US changes start after the launch |
| Steward capacity | Review queue grows | Size the review band to steward hours; monitor queue weekly |
| GDPR limits on training data | EU model delayed | DPO opinion before ML requirements are final |

## 10. Assumptions and what discovery could not confirm

- Duplicate rate is a sample estimate, not a full profile.
- Costs are ranges built without vendor quotes.
- The CCO has not yet confirmed the 0.1% tolerance in writing.
- The board commitment date was stated by the sponsor; we did not see it in writing.

## 11. Decision requested

1. Approve option 3 with phase 0 for the next budget cycle, within the range of €2.0–3.0M.
2. Confirm VP Commercial Operations as Data Owner for HCP master data.
3. Start phase 0 now, so the next reporting cycle already benefits.

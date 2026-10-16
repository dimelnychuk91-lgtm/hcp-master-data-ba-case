# Discovery Interview Summaries

> Weeks 1–2 of discovery. One-to-one interviews and one observation session.
> Each summary was sent to the interviewee for correction within 24 hours.
> Fictional case: people, quotes and figures are invented.

## How to read this document

Each summary has the same structure: **what we heard**, **new facts**, **what it changes** (link to the [business case](../02_strategy/business_case.md) and to decisions DEC-01 to DEC-12 in the [decision log](../02_strategy/decision_log.md)), **open questions**.
Stakeholder IDs (S1–S10) refer to the [stakeholder map](stakeholder_map.md).

---

## S1. VP Commercial Operations (sponsor)

**Format:** one-to-one, 45 min, week 1. Guide: [interview_guide_S1.md](interview_guide_S1.md).

**What we heard**
- The decision he needs from discovery: which option to put into next year's budget, with a cost range and a timeline he can defend in front of the board.
- After the acquisition he committed to the board to show **one customer view across both field forces** by the end of the next fiscal year. Compliance risk is the reason the budget was approved; commercial synergy is what he is measured on.
- His first instinct was to "just move BioCo onto our CRM". When asked what that would solve for him, the answer was speed and one system to report on, not data quality.
- Success in his words: "One plan per doctor. Not two reps from two companies in the same waiting room."

**New facts**
- **Constraint C1:** a new oncology product launches in the US in Q1. No changes to the US field CRM screens between January and March.
- Implementation budget is approved in the next budget cycle; discovery must deliver a cost range, not a fixed price.

**What it changes**
- Confirms the sponsor model: budget comes from commercial, risk sits with compliance.
- C1 shapes the phasing in the business case (section 8, DEC-12): US field changes cannot start before Q2.
- His preference for CRM consolidation (option 2) must be addressed openly in the options workshop, not avoided.

**Open questions**
- Is the board commitment a date or a direction? Who would check it?

---

## S2. Chief Compliance Officer

**Format:** one-to-one, 45 min, week 1.

**What we heard**
- The 40 disputes from the last Open Payments review period were mostly **split totals**: one doctor appeared as several records, each with a part of the amount.
- The case that worried her most was the opposite: **two different doctors with the same name were merged** in the spreadsheet, and a payment was reported against the wrong person. "A missing amount is a correction. A payment on the wrong doctor is a conversation with a lawyer."
- In France disclosure is a legal obligation and goes to a public government platform. In Germany publication of individual data depends on the doctor's consent.

**New facts**
- A false merge is a higher risk for her than a missed duplicate.
- She expects every merge that affects a reported payment to be traceable: who merged, when, on what basis.

**What it changes**
- Confirms the precision priority for auto-merge (DEC-07), now with a concrete incident behind it.
- Confirms the audit trail and unmerge requirements (DEC-10).
- Her answer to "what must never be automated without manual validation": merges of records that already carry reported payments in an open reporting cycle. Agreed later as: model-scored pairs touching open-cycle payments always go to a steward; merges by an exact national identifier proceed automatically and notify the Transparency team (DEC-07).

**Open questions**
- What error rate would she accept for auto-merge? Needs a number before thresholds can be proposed (DEC-07).

---

## S3. Former BioCo Head of Commercial

**Format:** one-to-one, 45 min, week 2, before any joint session.

**What we heard**
- BioCo's US data is keyed on NPI and has a low duplicate rate (their own estimate: about 2%). He sees moving to the PharmaCo CRM as "importing their mess into our clean house".
- His real worry is the US field team during the Q1 launch: any disruption would hit his numbers.
- When asked what works better in the BioCo CRM, he named the rule that **no doctor can be created without an NPI**.

**New facts**
- The NPI rule is a working control we can reuse, not just a data attribute.

**What it changes**
- Leads to DEC-03: his position is partly right. The NPI rule becomes a requirement for US records in the master, and BioCo NPI becomes the US reference key.
- Together with C1 from S1 there is a shared interest: neither wants US field disruption in Q1. A common ground for the joint workshop.

**Open questions**
- Would he co-own the US matching rules with the central stewards?

---

## S6. Transparency Analyst (observation)

**Format:** observation of the annual reconciliation, half a day, week 2.

**What we observed**
- Payments are exported from three systems into spreadsheets and matched by surname and city.
- About 3,000 doubtful pairs are reviewed by hand each cycle. Decisions are made in the spreadsheet and not recorded anywhere.
- The whole cycle takes about six weeks; the last two are spent on corrections after internal review.

**What it changes**
- Confirms the AS-IS process and the weak-label problem (DEC-08): there is no history of why records were matched.
- The 3,000 pairs per cycle give a first estimate of the steward review load.

---

## Cross-interview findings

| # | Finding | Source | Goes into |
|---|---|---|---|
| F1 | False merges are a higher risk than missed duplicates | S2 | ML requirements, matching rules |
| F2 | No changes to US field CRM screens in Q1 (launch) | S1, S3 | Business case phasing |
| F3 | Sponsor leans to CRM consolidation for speed | S1 | Options workshop |
| F4 | BioCo "no NPI, no record" rule is a working control | S3 | Requirements, matching rules |
| F5 | About 3,000 manual review pairs per cycle, no decision log | S6 | Steward capacity, ML labels |
| F6 | Board commitment: one customer view by end of next fiscal year | S1 | Business case success criteria |

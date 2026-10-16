# Business Analysis Plan: Six-Week Discovery

> How the BA work was planned before discovery started: approach, activities, techniques, deliverables, communication and how requirements are managed.
> Fictional case.

## 1. Context and objective

| | |
|---|---|
| **Engagement** | External delivery partner, six-week discovery |
| **Sponsor** | VP Commercial Operations (S1) |
| **Objective** | Give the Steering Committee a recommended solution option and requirements detailed enough for the MDM team to estimate |
| **Out of objective** | Vendor selection, detailed technical design, implementation |

## 2. Approach

- **Predictive for discovery, adaptive for delivery.** Discovery has a fixed end date and a fixed decision to support, so activities are planned week by week. Delivery after approval will run in increments (phase 0, 1a, 1b), and requirements are written as user stories so they can be refined per release.
- **Problem before solution.** No solution option is discussed with stakeholders before week 3, when root causes are confirmed.
- **Senior stakeholders one to one first.** Joint sessions only after every position is known (stakeholder tensions T1 to T4).

## 3. Activities by week

| Week | BA activities | Elicitation techniques | Stakeholders | Output |
|---|---|---|---|---|
| 1 | Read past disclosure reports, dispute log, procedures. Interview sponsor and CCO | Document analysis, interviews | S1, S2, S6 | [Stakeholder map](stakeholder_map.md) v0.1, [interview guide](interview_guide_S1.md), first [summaries](interview_summaries.md) |
| 2 | Interview former BioCo Head of Commercial and country leads. Observe the annual reconciliation. Early check with the DPO | Interviews, observation (job shadowing) | S3, S6, S7, S10 | Interview summaries, AS-IS process draft |
| 2–3 | Profile a sample of HCP records to size the duplicate problem | Data profiling | S5, S6 | Duplicate rate estimate, data quality findings |
| 3 | Confirm root causes. Session with ML Team on data quality and labels | Root cause analysis, workshop | S5, S9 | Root cause statement, label strategy |
| 3–4 | Facilitate TO-BE process and ownership workshop | Facilitated workshop, process modelling | S1, S2, S5, S7, S8 | TO-BE process, ownership model (RACI draft) |
| 4–5 | Draft BRD, user stories, matching rules, data model | Requirements analysis, modelling | S4, S5, S9 | BRD draft, stories, models |
| 5 | Options workshop: agree criteria and weights **before** scoring | Decision analysis, weighted scoring | S1, S2, S4, S5 | Decision matrix, sensitivity analysis |
| 6 | Review package with sponsor and CCO; present to Steering Committee | Review, presentation | Steering Committee | [Business case](../02_strategy/business_case.md), [decision log](../02_strategy/decision_log.md), [BRD](../03_requirements/BRD.md) v1.0 |

## 4. Deliverables and sign-off

| Deliverable | Approver | When |
|---|---|---|
| Stakeholder map | Sponsor | Week 1, updated weekly |
| Interview summaries | Each interviewee (corrections within 24 hours) | After each interview |
| AS-IS and TO-BE processes | Data Governance Lead, Transparency team | Week 4 |
| Business case and decision log | Steering Committee | Week 6 |
| BRD, user stories, traceability | Sponsor and CCO | Week 6 |
| ML requirements | CCO (thresholds), DPO (data use), ML Team (feasibility) | Week 6, DPO opinion pending |

## 5. Communication plan

| What | To whom | How often | Format |
|---|---|---|---|
| Status: done, next, blockers, decisions needed | Sponsor | Weekly, 30 min | Short call plus one-page note |
| Open risks and compliance questions | CCO | Every two weeks | One to one |
| Requirements walkthrough | MDM team, Enterprise Architect | Weeks 4 and 6 | Working session |
| Recommendation | Steering Committee | End of week 6 | Presentation and business case |

## 6. Requirements management

- **IDs and traceability.** Goals G1 to G3, requirements BR and NFR, stories US, decisions DEC. Every requirement traces to a goal and a stakeholder ([traceability matrix](../03_requirements/traceability_matrix.md)).
- **Prioritisation.** MoSCoW, agreed with the sponsor and the CCO.
- **Change after sign-off.** A change request states the reason, affected requirements and the effect on goals; the sponsor approves, the CCO approves anything that affects disclosure.
- **Decisions** are recorded in the decision log with rejected alternatives, the same day they are made.

## 7. Risks to the BA work

| Risk | Effect on discovery | Response |
|---|---|---|
| Senior stakeholders unavailable | Week 1–2 interviews slip, recommendation late | Book all one-to-ones in week 0; sponsor asks for priority |
| Data access for profiling delayed | Duplicate rate stays a guess | Agree a sample extract on day 1; use observation results if data is late |
| Conflict between sponsor and CCO surfaces too early | Positions harden before facts are known | One-to-ones first; options discussed only after root causes are confirmed |
| Scope pressure ("add all markets", "add HCOs") | Six weeks not enough | Scope written in week 1 and confirmed by the sponsor; additions go to phase 2 |
| DPO opinion takes longer than discovery | ML requirements cannot be final | Mark as dependency; deliver ML requirements with the open item stated |

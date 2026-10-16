# Stakeholder Map

> **Version:** 0.1, before interviews (week 1). Positions are assumptions to be confirmed in one-to-one interviews.
> Fictional case. See [README](../README.md).

## 1. Power / interest grid

| | **Low interest** | **High interest** |
|---|---|---|
| **High power** | Enterprise Architect *(keep satisfied)* | VP Commercial Operations, Chief Compliance Officer, Former BioCo Head of Commercial *(manage closely)* |
| **Low power** | Country Commercial Leads *(monitor)* | Data Governance Lead, Transparency Analyst, Data Stewards, ML Team *(keep informed, involve in design)* |

Data Protection Officer sits outside the grid: low interest in the project itself, but a hard gate for using HCP data in model training.

## 2. Stakeholder profiles

| ID | Role | What they want | Influence | Expected position | Engagement |
|---|---|---|---|---|---|
| S1 | **VP Commercial Operations** (sponsor, budget, future Data Owner) | One customer view, fewer duplicate rep visits, fast visible result | Decides budget and scope | Supportive, but pushes for speed | One-to-one interview week 1. Weekly status. Steering committee chair |
| S2 | **Chief Compliance Officer** | Correct disclosure reports, no regulator or HCP disputes, audit trail | Can block go-live; veto on rules that affect disclosure | Cautious. Will not accept speed over accuracy | One-to-one interview week 1. Sign-off on matching and consent rules |
| S3 | **Former BioCo Head of Commercial** | Keep BioCo CRM and processes, protect the US team from disruption | Strong informal influence on the US field force | Resistant. Partly right: BioCo US data is keyed on NPI | One-to-one interview week 2, before any joint workshop. Involve as owner of the US reference key |
| S4 | **Enterprise Architect** | No unnecessary new platforms, fit with the target architecture | Approves solution options | Neutral to sceptical about an MDM hub | Options workshop week 5. Early review of option list |
| S5 | **Data Governance Lead** | Clear ownership, rules and stewardship | Defines policies, no budget | Strong supporter | Co-designs ownership model (RACI) in weeks 3–4 |
| S6 | **Transparency Analyst** | Fewer weeks of manual reconciliation | Low formal power, key process knowledge | Supportive | Observation of the reconciliation in week 2 |
| S7 | **Country Commercial Leads** (US, DE, FR) | No disruption to field teams | Local adoption | Neutral, worried about extra steps for reps | Short interviews week 2. TO-BE walkthrough before sign-off |
| S8 | **Data Stewards** (to be appointed) | Clear rules, manageable review queue | Low power, high operational impact | Unknown, role does not exist yet | Involve in matching rules and review queue design. Label a sample of record pairs in phase 0 |
| S9 | **ML / Data Science Team** | Labelled data, clear target metric, freedom to automate more | Builds the matching model | Supportive, may push for a wider auto-merge band | Joint session on data quality and labels (week 3). Thresholds proposed by S9, decided by S1 and S2 |
| S10 | **Data Protection Officer** | Lawful basis and purpose limits for using HCP personal data in model training | Can block training on EU data | Neutral, process-driven | Early check in week 2, written opinion before ML requirements are final |

## 3. Key tensions

| Tension | Between | How the BA handles it |
|---|---|---|
| **T1. Keep BioCo CRM vs one platform** | S3 vs S1, S4 | Interview S3 alone first. Use the valid part of the position: NPI from BioCo becomes the US reference key in the master |
| **T2. Speed vs accuracy** | S1 vs S2 | Phase 0 gives compliance a safer next reporting cycle while the MDM hub is built. Agree acceptance thresholds with S2 in writing |
| **T3. Extra steps for reps** | S7 vs S2 | Search before create must take seconds, not minutes. Measure in the TO-BE walkthrough |
| **T4. How much to merge automatically** | S9 vs S2 | Translate thresholds into business terms: a false merge is a wrong report to the regulator, a lower threshold costs steward hours. The CCO decides, the ML team advises |

## 4. Open questions for interviews

- S1: What decision do you need from this discovery, and by when?
- S2: Which errors in the last reporting cycle worried you most, and why?
- S2: What in this process must never be automated without manual validation?
- S3: What exactly works better in the BioCo CRM today?
- S4: What is the target architecture for customer data?

# HCP Master Data after an Acquisition: a Business Analysis Case

A full business analysis case from discovery to requirements: a pharma company that cannot report payments to doctors correctly because the same doctor exists as several records after an acquisition.

> **Fictional case.** Company names, people and figures are invented. Regulatory facts are real and sourced in the documents.
> The [real-world parallel](#real-world-parallel) describes my own work experience.
> I used AI (Claude) as a working partner: it drafted documents and proposed options; I set the framing, chose between options, added the real-world experience and reviewed every artifact.

## The problem in two minutes

**PharmaCo**, a global biopharma company, bought **BioCo**, a US oncology company. Eighteen months later both companies still run separate CRMs.

The same doctor now appears as several records. That matters because pharma companies must publish what they pay to doctors: in the US under Open Payments, in Europe under national rules and the EFPIA Code.

- When one doctor is **split** across records, their total is reported in parts. Last cycle: **40 disputes** from doctors.
- When two different doctors are **merged**, a payment is reported against the wrong person. It happened once, and it is the case the Compliance Officer fears most.
- The annual clean-up takes **six weeks** of spreadsheet work and leaves no record of its decisions.

**My role:** Business Analyst from an external delivery partner, six-week discovery. Output: a recommendation for the Steering Committee and requirements detailed enough for the MDM team to estimate.

## What I recommended

**An MDM hub that holds one golden record per doctor, with a quick-win phase before the next reporting cycle.**

- **Root cause first.** Duplicates come from three layers: no shared identifier, manual entry in the field, nobody owning the data. The recommendation addresses all three; cheaper options address one.
- **Four options compared on agreed weights**, including "do nothing". The MDM hub scored 3.95 / 5, the tactical fix 3.30, CRM consolidation 2.65. The sensitivity analysis shows when the cheaper option would be the right call.
- **Hybrid matching.** An exact NPI match merges by rule. An ML model scores the fuzzy cases into three bands: auto-merge, steward review, not a duplicate. Thresholds are set by Compliance, not by the ML team.
- **A false merge is worse than a missed one.** Auto-merge tolerance is 1 wrong per 1,000, and any record with payments in an open reporting cycle always goes to a person.
- **The resisting stakeholder was partly right.** BioCo's rule "no NPI, no record" became a master data rule for the US.
- **A launch freeze became part of the plan.** No US field changes in Q1, so Q1 delivers everything else.

## Artifacts

| Area | Document | What it shows |
|---|---|---|
| **Discovery** | [Stakeholder map](01_discovery/stakeholder_map.md) | 10 stakeholders, power and interest, four tensions and how each is handled |
| | [Interview guide: sponsor](01_discovery/interview_guide_S1.md) | Elicitation plan for a senior stakeholder |
| | [Interview summaries](01_discovery/interview_summaries.md) | What each stakeholder said, what it changed, six cross-interview findings |
| **Strategy** | [Business case](02_strategy/business_case.md) | Problem cost, goals with baselines, four options, weighted matrix, sensitivity, roadmap, risks |
| | [Decision log](02_strategy/decision_log.md) | 12 decisions with context, rejected alternatives and who decided |
| **Requirements** | [BRD](03_requirements/BRD.md) | Scope, 16 business and 6 non-functional requirements, constraints, acceptance |
| | [User stories](03_requirements/user_stories.md) | 15 stories in 5 epics, acceptance criteria in Given / When / Then |
| | [Wireframes](03_requirements/wireframes.md) | Two key screens: rep's search before create, steward's pair review |
| | [ML requirements](03_requirements/ml_requirements.md) | Data quality for the model, labels, thresholds, model metrics in business terms, monitoring |
| | [UAT scenarios](03_requirements/uat_scenarios.md) | 17 end-to-end acceptance scenarios, entry and exit criteria, defect severity |
| | [Traceability matrix](03_requirements/traceability_matrix.md) | Goal → requirement → decision → story → use case → screen → test |
| **Models** | [AS-IS and TO-BE processes (BPMN 2.0)](04_models/process_as_is_to_be.md) | Pools, lanes, events, gateways, message flows; `.bpmn` files open in Camunda Modeler |
| | [Use cases (UML)](04_models/use_cases.md) | Use case diagram and two full use case specifications |
| | [Activity diagram (UML)](04_models/activity_search_before_create.md) | Search before create with swimlanes |
| | [Sequence diagrams (UML)](04_models/sequence_diagrams.md) | Search before create via API; BioCo batch load with dry run and rollback |
| | [State machines (UML)](04_models/state_machines.md) | Lifecycles of the golden record and the candidate pair |
| | [Data flow diagrams](04_models/data_flows.md) | Context and level 1 DFD, data stores |
| | [Data model](04_models/data_model.md) | Conceptual model, logical ER model, UML class diagram, design decisions |
| | [Data dictionary](04_models/data_dictionary.md) | Every attribute: type, source, survivorship, owner, quality rule |
| | [Matching and survivorship rules](04_models/matching_rules.md) | Rule order, thresholds, two matching modes, unmerge |
| | [MDM API (OpenAPI 3.0)](04_models/mdm_api.yaml) | Three endpoints with business rules expressed as status codes |
| **Governance** | [Ownership and RACI](05_governance/raci.md) | Roles, RACI, change control, operating rhythm, data quality indicators |
| | [Glossary](glossary.md) | Domain and method terms in plain words |

Diagrams: BPMN 2.0 sources in [04_models/src](04_models/src) (open in Camunda Modeler or [demo.bpmn.io](https://demo.bpmn.io)); UML drawn in PlantUML; DFD, ER and rule flow in Mermaid. All render on GitHub. To view the API, paste [mdm_api.yaml](04_models/mdm_api.yaml) into [editor.swagger.io](https://editor.swagger.io).

## At a glance

![TO-BE process in BPMN 2.0](04_models/img/bpmn_to_be.svg)

## Suggested reading order

1. This page.
2. [Business case](02_strategy/business_case.md): the reasoning behind the recommendation.
3. [Decision log](02_strategy/decision_log.md): what was rejected and why.
4. [BRD](03_requirements/BRD.md) and [user stories](03_requirements/user_stories.md): what the business needs.
5. Any model that interests you.

## Real-world parallel

The core problem is one I worked on for years in travel-tech data operations.

In a bus ticket aggregator, one bus stop arrived from partners under many names: "Київ", "Київ АВ", "Kyiv", "Київ, автовокзал". Each variant split bookings and broke searches.

- Naming and registration rules were **written in a team regulation**.
- **Only my team** could create stops.
- Mismatches surfaced through customer complaints, failed bookings, partner uploads, API responses and checks in Postman.
- Day to day it was **10–20 fixes**; onboarding a new partner meant **tens of thousands** of records at once.

Two lessons from that work shaped this case: **matching needs two modes** (bulk load and daily entry), and **ownership matters more than tools**.

## Methods used

Stakeholder analysis · elicitation planning · root cause analysis · options analysis with weighted scoring and sensitivity · MoSCoW · user stories with Given / When / Then · traceability · BPMN 2.0 process modelling · UML use case, activity, sequence, class and state diagrams · use case specifications · wireframes · UAT scenarios · DFD · conceptual and logical data modelling · data dictionary · MDM matching and survivorship · ML requirements and model metrics in business terms · OpenAPI · RACI and data governance.

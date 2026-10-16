# User Stories and Acceptance Criteria

> Derived from the [BRD](BRD.md). Each story traces to business requirements (BR) and non-functional requirements (NFR).
> Acceptance criteria use Given / When / Then and are the basis for UAT.
> Fictional case.

## Story map

| Epic | Stories |
|---|---|
| E1. Capture doctors at the point of entry | US-01, US-02, US-03 |
| E2. Match and merge | US-04, US-05, US-06, US-15 |
| E3. Steward review | US-07, US-08, US-09 |
| E4. Disclosure reporting | US-10, US-11, US-12 |
| E5. Field coordination and oversight | US-13, US-14 |

Priority uses MoSCoW from the BRD. Release: **1a** = Q1 (no US field screen changes), **1b** = Q2.

---

## E1. Capture doctors at the point of entry

### US-01. Search before create

**As a** field rep, **I want** to see existing doctors that match what I typed before I create a new one, **so that** I do not create a duplicate.

Traces to: BR-04, NFR-04 · Priority: M · Release: 1a (EU), 1b (US)

**Acceptance criteria**

1. **Given** a rep enters surname, first name, city and specialty for a new doctor, **when** they start creating the record, **then** the CRM shows up to 10 candidate doctors from the golden records, ranked by match score, before the create form can be saved.
2. **Given** the candidate list is shown, **when** the rep selects a candidate, **then** the CRM links the rep's account to that golden record and no new doctor is created.
3. **Given** a search is made, **when** results are returned, **then** 95% of searches return within 2 seconds.
4. **Given** the search finds an exact NPI match, **when** results are shown, **then** that candidate is shown first and marked "same NPI".

### US-02. Create a new doctor when no match exists

**As a** field rep, **I want** to create a new doctor when none of the candidates is the right person, **so that** I can record my visit without delay.

Traces to: BR-04, BR-06 · Priority: M · Release: 1a (EU), 1b (US)

**Acceptance criteria**

1. **Given** the rep has seen the candidate list, **when** they choose "None of these", **then** the create form opens with the data they already typed.
2. **Given** the rep saves the new doctor, **when** the MDM receives it, **then** it is matched against existing golden records like any other new record (US-05).
3. **Given** the rep did not run a search in this session, **when** they try to save a new doctor, **then** the save is refused with "Search for the doctor first".

### US-03. No NPI, no US record

**As a** Compliance officer, **I want** every US doctor to have a valid NPI, **so that** US records can be matched reliably and reported correctly.

Traces to: BR-03 · Priority: M · Release: 1b

**Acceptance criteria**

1. **Given** a rep creates a doctor with country US, **when** the NPI field is empty, **then** the record cannot be saved and the message says "NPI is required for US doctors".
2. **Given** an NPI is entered, **when** it does not have 10 digits or fails the check digit, **then** the record cannot be saved and the message says "NPI is not valid".
3. **Given** an NPI is entered that already belongs to a golden record, **when** the rep saves, **then** no new doctor is created and the rep is linked to the existing golden record.

---

## E2. Match and merge

### US-04. Load BioCo doctors once

**As a** data engineer, **I want** to load all BioCo doctor records in a dry run first, then for real, with the option to roll back, **so that** a bad load never reaches reporting.

Traces to: BR-05, BR-06, NFR-01 · Priority: M · Release: 1a

**Acceptance criteria**

1. **Given** a BioCo extract, **when** a dry run is executed, **then** the system reports how many records would be merged by rule, merged automatically, sent to review and kept as new, without changing any golden record.
2. **Given** the dry run report is approved by the Data Governance Lead, **when** the real load runs, **then** the result matches the dry run counts within 1%.
3. **Given** a completed load, **when** a rollback is requested within 30 days, **then** all merges made by that load are reversed and linked payments return to their original records.
4. **Given** a random sample of 1,000 automatic merges from the dry run, **when** stewards check them, **then** no more than 1 is wrong. If more, the real load does not start and thresholds are reviewed (BR-16).

### US-05. Route candidate pairs by score

**As a** Data Governance Lead, **I want** each candidate pair to be merged by rule, merged automatically, sent to review or rejected according to agreed thresholds, **so that** stewards only see the pairs that need a human.

Traces to: BR-06, BR-07 · Priority: M · Release: 1a

**Acceptance criteria**

1. **Given** two records with the same valid NPI, **when** matching runs, **then** they are merged by rule without a model score.
2. **Given** two records with different valid NPIs, **when** matching runs, **then** they are never merged, whatever the model score.
3. **Given** a pair without a shared NPI, **when** the model score is at or above the auto-merge threshold, **then** the pair is merged automatically.
4. **Given** a pair that would be merged automatically, **when** either record has payments in an open reporting cycle, **then** the pair goes to steward review instead.
5. **Given** a pair with a score between the review and auto-merge thresholds, **when** matching runs, **then** the pair is added to the steward queue of the doctor's country.
6. **Given** a pair below the review threshold, **when** matching runs, **then** it is recorded as "not a duplicate" and not shown to stewards.

### US-06. Audit every merge

**As a** Compliance officer, **I want** every merge to record who or what made it and why, **so that** I can answer an auditor or a doctor's dispute.

Traces to: NFR-01, BR-13 · Priority: M · Release: 1a

**Acceptance criteria**

1. **Given** any merge or unmerge, **when** it is completed, **then** the log stores: records involved, time, actor (rule, model or steward name), reason, model score, model version and threshold in force.
2. **Given** a log entry, **when** anyone tries to edit or delete it, **then** the change is refused.
3. **Given** a golden record ID, **when** a Compliance officer opens its history, **then** they see all merges and unmerges in date order.

### US-15. Keep affiliations current

**As a** data steward, **I want** each doctor's affiliations to organisations to have start and end dates, **so that** matching and reporting use where the doctor practises now.

Traces to: BR-11 · Priority: S · Release: 1a

**Acceptance criteria**

1. **Given** a source system sends a new place of practice for a doctor, **when** the golden record is updated, **then** a new affiliation is added with a start date, and the previous one is kept.
2. **Given** a doctor has two current affiliations, **when** matching runs, **then** both are used as matching attributes.
3. **Given** an affiliation is ended, **when** the end date is set, **then** it is no longer used for matching but remains in history.

---

## E3. Steward review

### US-07. Review a candidate pair

**As a** data steward, **I want** to see two records side by side with the reasons they were proposed as a match, **so that** I can decide quickly and correctly.

Traces to: BR-08 · Priority: M · Release: 1a

**Acceptance criteria**

1. **Given** a pair in my queue, **when** I open it, **then** I see both records side by side with matching and differing attributes highlighted.
2. **Given** the pair was scored by the model, **when** I open it, **then** I see which attributes contributed to the score (for example: same address, similar name, same specialty, different city).
3. **Given** I decide "same doctor" or "different doctors", **when** I save, **then** a reason from a fixed list is mandatory, and a free-text comment is optional.
4. **Given** my decision is saved, **when** the pair is closed, **then** the decision is available as a training label for the matching model (DEC-08).

### US-08. Undo a wrong merge

**As a** data steward, **I want** to split a golden record that combines two different doctors, **so that** each doctor's payments are reported correctly.

Traces to: BR-09, NFR-01 · Priority: M · Release: 1a

**Acceptance criteria**

1. **Given** a golden record built from several source records, **when** I select the source records that belong to a different doctor and choose "Unmerge", **then** a new golden record is created for them.
2. **Given** the unmerge is completed, **when** payments were linked to the moved source records, **then** those payments move to the new golden record.
3. **Given** the unmerge affects a doctor with payments in an open reporting cycle, **when** it is saved, **then** the Transparency team is notified.

### US-09. Keep the queue under control

**As a** Data Governance Lead, **I want** to see the size and age of each country queue, **so that** I can move steward capacity before pairs pile up.

Traces to: BR-14 · Priority: S · Release: 1a

**Acceptance criteria**

1. **Given** the queue dashboard, **when** I open it, **then** I see per country: open pairs, pairs older than 5 working days, decisions per steward per week.
2. **Given** a country queue has more than 50 pairs older than 5 working days, **when** the daily check runs, **then** the Data Governance Lead receives an alert.

---

## E4. Disclosure reporting

### US-10. Produce the disclosure extract from golden records

**As a** Transparency analyst, **I want** the disclosure extract to group payments by golden record, **so that** each doctor's total is complete and on one line.

Traces to: BR-02, BR-13 · Priority: M · Release: 1a (EU), 1b (US)

**Acceptance criteria**

1. **Given** payments in the reporting period, **when** the extract is produced, **then** every payment is linked to exactly one golden record, and unlinked payments are listed separately for review.
2. **Given** the extract, **when** it is reconciled with the payment systems, **then** the total amount matches to the cent.
3. **Given** a doctor's total changed since the last extract because of a merge or unmerge, **when** I view the extract, **then** that doctor is flagged with a link to the change in the merge log.

### US-11. Respect consent and legal basis per country

**As a** Transparency analyst, **I want** each doctor's publication basis to be shown per country and year, **so that** I publish individually only where it is allowed.

Traces to: BR-10, NFR-02 · Priority: M · Release: 1a

**Acceptance criteria**

1. **Given** a doctor in Germany, **when** consent for individual publication for the reporting year is recorded, **then** the extract lists the doctor individually.
2. **Given** a doctor in Germany without recorded consent, **when** the extract is produced, **then** their amounts go to the aggregate line.
3. **Given** a doctor in France, **when** the extract is produced, **then** the legal basis "legal obligation" is recorded and no consent is required.
4. **Given** two records merged into one golden record carry conflicting consent statuses, **when** the golden consent status is set, **then** the more restrictive status wins until a steward confirms otherwise.

### US-12. Prepare for a doctor's dispute

**As a** Compliance officer, **I want** to see for any doctor the payments, the source records and the merge history behind their reported total, **so that** I can answer a dispute within the review period.

Traces to: BR-13, NFR-01 · Priority: S · Release: 1a

**Acceptance criteria**

1. **Given** a doctor's golden record ID or NPI, **when** I search, **then** I see the reported total, each payment with its source system and the merge history.
2. **Given** a dispute is accepted, **when** a steward corrects the record, **then** the corrected total is visible in the next extract and the change is linked to the dispute reference.

---

## E5. Field coordination and oversight

### US-13. See the other field force

**As a** field rep, **I want** to see whether a doctor is also engaged by the other company's field force and who to contact, **so that** we coordinate instead of visiting twice.

Traces to: BR-12 · Priority: S · Release: 1b

**Acceptance criteria**

1. **Given** a doctor's golden record is linked to accounts in both CRMs, **when** I open the doctor, **then** I see "Also engaged by BioCo / PharmaCo field force" and the contact owner's name.
2. **Given** I plan a visit, **when** the other field force has a visit planned within 14 days, **then** I see a warning.

### US-14. Data quality at a glance

**As the** Data Owner, **I want** a monthly view of duplicate rate, queue health and automatic merge accuracy, **so that** I know whether the investment is working.

Traces to: BR-14, BR-16 · Priority: S · Release: 1a

**Acceptance criteria**

1. **Given** the monthly report, **when** I open it, **then** I see duplicate rate by country against the target of 2%, queue size and age, and the result of the latest sampled audit of automatic merges.
2. **Given** the sampled audit finds more than 1 wrong merge per 1,000, **when** the report is published, **then** automatic merging is shown as paused and the threshold review is listed as an open action.

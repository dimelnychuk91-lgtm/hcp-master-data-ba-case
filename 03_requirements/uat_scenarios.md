# UAT Scenarios

> End-to-end scenarios for user acceptance testing of phase 1. Each scenario walks a business situation through several stories and checks the acceptance criteria along the way.
> Run by business users (reps, stewards, Transparency, Compliance) on a test environment with anonymised data. Fictional case.

## Entry and exit criteria

**Entry:** all **M** stories passed system testing; test data loaded (anonymised copy of PharmaCo and BioCo records, 3 months of payments); thresholds set from model validation.

**Exit (phase 1 accepted):**
- every scenario below passed, or failed only with defects agreed as non-blocking by the Data Owner and the CCO;
- sampled audit of 1,000 automatic merges: no more than 1 wrong (BRD, section 11);
- first disclosure extract from golden records reconciles with the payment systems to the cent.

## Scenarios

| ID | Scenario | Tester | Steps (short) | Expected result | Covers |
|---|---|---|---|---|---|
| UAT-01 | Rep finds an existing doctor | Field Rep (DE) | Search "Mueller, Köln, Oncology" → select "Anna Müller" | No new record; account linked; 95% of searches ≤ 2 s over the session | US-01, BR-04, NFR-04 |
| UAT-02 | Rep creates a new EU doctor | Field Rep (FR) | Search → "None of these" → save | Golden record created; background matching started; visit logged without waiting | US-02, BR-04 |
| UAT-03 | Rep tries to skip search | Field Rep | Open create form directly (test hook) → save | Save refused: "Search for the doctor first" | US-02 AC 3 |
| UAT-04 | US doctor without NPI | Field Rep (US) | Search → create with empty NPI | Save blocked: "NPI is required for US doctors" | US-03, BR-03 |
| UAT-05 | US doctor whose NPI already exists | Field Rep (US) | Create with an NPI held by another golden record | No new record; rep linked to the existing doctor | US-03 AC 3, R2 |
| UAT-06 | Retry after timeout | Tester with API tool | Send the same create request twice with one Idempotency-Key | One doctor created; second call returns the first result | API, BR-04 |
| UAT-07 | Namesakes with different NPIs | Data Steward | Load two "John Smith, Boston" records with different NPIs | Never merged, whatever the score | R1, US-05 AC 2 |
| UAT-08 | High score with open-cycle payments | Data Steward | Create a pair above auto-merge threshold where one record has payments in the open cycle | Pair goes to review, not auto-merged; screen shows "sent to review by rule R6" | BR-07, US-05 AC 4 |
| UAT-09 | Steward decides a pair | Data Steward | Open pair → "Same doctor" without reason → add reason → save | First save refused; second save merges and logs steward ID and reason | US-07, NFR-01 |
| UAT-10 | Undo a wrong merge with payments | Data Steward, Transparency Analyst | Unmerge a golden record that combines two doctors with payments | New golden record created; payments move with their source records; Transparency notified | US-08, BR-09 |
| UAT-11 | Consent conflict on merge | Data Steward, Compliance Officer | Merge two DE records, one with consent, one without | Golden basis is "no consent" until a steward confirms; extract puts amounts in the aggregate line | US-11 AC 2 and AC 4 |
| UAT-12 | France legal basis | Transparency Analyst | Produce extract for an FR doctor without consent record | Doctor listed individually with basis "legal obligation" | US-11 AC 3 |
| UAT-13 | Extract reconciles and flags changes | Transparency Analyst | Produce extract after UAT-09 and UAT-10 | Every payment linked to one golden record; totals match payment systems; changed doctors flagged with link to merge log | US-10, BR-02, BR-13 |
| UAT-14 | Answer a doctor's dispute | Compliance Officer | Search by NPI → open history | Reported total, each payment with source, full merge history visible | US-12, NFR-01 |
| UAT-15 | BioCo dry run and rollback | Data Engineer, Data Governance Lead | Dry run → approve → real load → roll back | Dry run writes nothing; real load within 1% of dry run counts; rollback reverses only that load and moves payments back | US-04, BR-05 |
| UAT-16 | Queue alert | Data Governance Lead | Leave more than 50 DE pairs older than 5 working days | Alert sent; dashboard shows queue age | US-09 |
| UAT-17 | Access by role | Field Rep, Data Steward | Rep tries to open consent data; FR steward opens DE queue | Both refused | NFR-02 |

## Defect severity

| Severity | Definition | Blocks acceptance? |
|---|---|---|
| Critical | Wrong-person merge, payment lost or wrongly assigned, consent ignored | Yes |
| High | A **M** acceptance criterion fails without workaround | Yes |
| Medium | Workaround exists, no effect on disclosure | Data Owner and CCO decide |
| Low | Cosmetic | No |

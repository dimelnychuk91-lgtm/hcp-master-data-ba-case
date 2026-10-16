# Glossary

Terms used across the case, in plain words.

| Term | Meaning in this case |
|---|---|
| **Affiliation** | The link between a doctor and an organisation where they practise, with start and end dates |
| **Auto-merge** | A merge made by the system without a person, when the model score is above the agreed threshold |
| **Blocking** | Pre-selecting which records to compare, so the system does not compare every record with every other |
| **Calibration** | A model is calibrated when a score of 0.9 really means about a 90% chance of being the same doctor |
| **Candidate pair** | Two records that might describe the same doctor and need a decision |
| **CCO** | Chief Compliance Officer |
| **Data Owner** | The business role that decides what a correct HCP record is and funds the work (VP Commercial Operations) |
| **Data steward** | A person who reviews doubtful pairs and maintains the data rules for a country |
| **DGL** | Data Governance Lead |
| **Disclosure / transparency reporting** | Publishing payments and other transfers of value from pharma companies to doctors |
| **DPO** | Data Protection Officer, responsible for lawful use of personal data under GDPR |
| **Dry run** | A trial load that calculates what would happen without changing any data |
| **EFPIA Code** | European pharma industry code that requires disclosure of transfers of value to doctors; individual publication usually needs the doctor's consent |
| **Golden record** | The single trusted record of a doctor, built from all source records |
| **HCO** | Healthcare organisation: hospital, clinic, teaching hospital |
| **HCP** | Healthcare professional; in this case, a doctor |
| **Human in the loop** | Doubtful cases are decided by a person, not by the model |
| **Idempotency-Key** | A key sent with a request so that a retry does not create a second record |
| **MDM** | Master data management: keeping one trusted version of core business entities |
| **NPI** | National Provider Identifier, the 10-digit US number for healthcare providers |
| **Open Payments** | The US federal programme (Sunshine Act) under which manufacturers report payments to doctors and teaching hospitals |
| **Open reporting cycle** | A disclosure period whose report has not yet been submitted; changes to it need extra care |
| **Precision** | Of the records the system merged, the share that really were the same doctor |
| **Publication basis** | The legal ground for publishing a doctor's data individually: consent, or a legal obligation (France) |
| **Recall** | Of all true duplicates, the share the system found |
| **RPPS** | French national directory number for healthcare professionals |
| **Source record** | A doctor's record as it exists in one source system (CRM, events, spend) |
| **Survivorship** | The rule that decides which value wins on the golden record when sources disagree |
| **Unmerge** | Splitting a golden record that wrongly combines two doctors |

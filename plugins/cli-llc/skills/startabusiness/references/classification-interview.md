# Inception classification interview

## Gather facts conversationally

Start with “Describe your first sale: who pays, what they receive, and where you deliver it.” Then resolve the missing facts one question at a time:

1. Identify the products or services sold, customer type, and delivery method.
2. Identify the activity expected to generate most revenue; record projections as projections. Ask for actual activity and revenue when the business already operates.
3. Identify country/state of formation if chosen, actual operating locations, and where customers receive products/services.
4. Identify number and types of owners, ownership structure, and tax-residency countries when needed for the filing analysis. Do not request taxpayer IDs or identity documents in chat. Do not assume citizenship or location establishes tax residency.
5. Identify planned employees, contractors, inventory, and products/services that may need sales-tax or licensing review. Record taxability as unresolved until checked under the applicable jurisdiction's rules.

Reuse established facts instead of repeating the interview. If ownership, revenue, or geography is undecided, mark it pending and continue independent preparation. Do not assign a personal identity, industry, jurisdiction, or election from the template author's profile.

## Keep classification records separate

| Record | Evidence and selection method |
|---|---|
| NAICS | Read official Census definitions, inclusion/exclusion notes, and applicable edition. Classify the actual establishment activity. Resolve multiple activities or establishments explicitly rather than forcing a whole enterprise into one unsupported code. |
| IRS business activity | Identify the applicable return and tax year first. Read that return's official instructions and selection rule, including its measure of principal activity. Confirm the code is present in that list; document differences from NAICS. |
| Legal entity and tax status | Record legal organization, formation status, ownership, default federal treatment if established, and elections separately. Confirm eligibility, filing/effective dates, and evidence before describing an election as effective. |
| Bookkeeping | Propose an internal chart of accounts appropriate to the accounting system. Label numbers as internal conventions, not government industry codes; map accounts to tax reporting separately and verify that mapping for the return/year. |

Do not assume Schedule C applies to every one-person business, a registered LLC must file a corporate return, or a nonprofit exemption follows from mission branding. Use the owner's type and applicable official rules to identify the filing path. For special ownership, cross-border facts, or unclear treatment, flag the exact issue for qualified review instead of guessing.

## Verify candidates

Retrieve current official sources before supplying specific code numbers or tax guidance. Start with:

- Census NAICS search and manuals: https://www.census.gov/naics/
- IRS LLC classification overview: https://www.irs.gov/businesses/small-businesses-self-employed/limited-liability-company-llc
- IRS forms and instructions: https://www.irs.gov/forms-instructions
- Schedule C instructions when that return applies: https://www.irs.gov/instructions/i1040sc

Use the user's required filing year, not automatically the current calendar year or the newest published instructions. Do not treat a proposed future NAICS revision as adopted. If the relevant instructions are unpublished or inaccessible, leave the IRS code pending and record the limitation; do not claim an older edition is final for a future return.

Propose a primary candidate and alternatives only when needed. Explain how the facts match the definition and what unresolved fact would change the choice. Never select a code solely to seek lower taxes, favorable insurance, or eligibility benefits.

## Record provenance and review

Use existing configuration conventions. For each classification, include:

- `system`, `code` or nullable value, and `label`.
- `edition`, `tax_year`, and `form` where applicable; use null for inapplicable or unknown values.
- `source_url`, `retrieved_at`, and a brief `rationale`.
- `facts_basis` as actual or projected, with unresolved assumptions.
- Separate `definition_check`, `founder_fact_review`, and `professional_review` statuses.
- `status` as pending, proposed, or confirmed, with confirmation basis and date. Do not imply professional review occurred unless it did.

Classify internal bookkeeping accounts separately, including the internal scheme version and any verified reporting mappings. Code strings should preserve leading zeros where relevant.

Keep raw interview answers and sensitive evidence in a private destination. A GitHub repository is not automatically private. If no private destination is available, persist only redacted public-safe records and identify private persistence as pending.

Revalidate when the operating model, dominant activity, ownership, jurisdictions, return, tax year, or code edition changes. Preserve prior classifications and the reason for the change rather than silently overwriting historical filing records.

## Completion

Return the facts understood, proposed classifications with official references, missing decisions, and the next useful preparation step. Industry-code selection does not establish legal formation, tax registration, permits, an election, or authority to file.

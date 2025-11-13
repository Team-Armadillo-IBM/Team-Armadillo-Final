# Mock Bank Auto Loan Policy (Global)
- **Document ID:** AutoLoanPolicy_Global_2025
- **Effective Date:** January 1, 2025
- **Product:** Auto Loans
- **Region:** Global
- **Policy Owner:** Global Compliance and Risk Governance

## Section 1 – Eligibility Criteria
- **Credit Score or Equivalent (POL-G-001):** Applicants must meet the local credit scoring or creditworthiness standard equivalent to a FICO score of 700 or above. Quote: "Applicants must demonstrate creditworthiness comparable to a FICO score of 700."
- **Debt-to-Income Ratio (POL-G-002):** The borrower’s DTI must not exceed 0.35 (35%) or local regulatory equivalent.
- **Loan-to-Value Ratio (POL-G-003):** The LTV must not exceed 0.90 (90%) of the appraised vehicle value unless explicitly allowed by local regulation or covered by additional collateral.
- **Employment Verification (POL-G-004):** Applicants must provide verifiable income documentation compliant with local labor and data protection laws.
- **Sanctions and KYC (POL-G-005):** All borrowers must pass Know Your Customer and sanctions screening under the jurisdiction’s applicable financial regulations.

## Section 2 – Interest Rate Bands (POL-G-006)
| Risk Tier | Creditworthiness | APR Band (%) | Conditions |
| --- | --- | --- | --- |
| Low Risk | ≥ 750 FICO-equivalent | 3.5 – 5.0 | Auto-pay, compliant jurisdiction |
| Medium Risk | 700 – 749 FICO-equivalent | 5.1 – 7.0 | Auto-pay, standard region |
| Elevated Risk | 650 – 699 FICO-equivalent | 7.1 – 9.0 | Requires supervisor approval |

Local subsidiaries may adjust rates to comply with central bank lending thresholds and consumer credit directives.

## Section 3 – Required Documentation (POL-G-007)
Required documentation must align with the jurisdiction’s financial compliance requirements.
1. Proof of Income or Tax Documentation
2. Verified Employment or Business Registration
3. Government-Issued Identification and Proof of Residence
4. Vehicle Purchase Agreement or Import/Export Certificate (if applicable)
5. KYC and Sanctions Screening Confirmation

## Section 4 – Compliance and Governance (POL-G-008)
All global risk assessment activities must log operations to the Governance Ledger with region codes and anonymized identifiers to maintain cross-border compliance.

Each event should include:
- Application ID
- Region
- Input and Output Hashes
- UTC Timestamp
- Responsible Entity Code

Example:
```
governance_log("risk_scored_global", {"application_id": "A-INT-2031", "region": "EU", "hash_in": "...", "hash_out": "..."})
```

## Section 5 – Data Privacy and Localization (POL-G-009)
Data used for risk scoring must comply with the strictest applicable privacy framework, such as GDPR (EU), CCPA (U.S.), LGPD (Brazil), or PDPA (Singapore). Personally identifiable information must not leave the jurisdiction of origin unless transferred under legally recognized data adequacy agreements.

## Section 6 – Policy Revision History
| Version | Date | Summary of Changes |
| --- | --- | --- |
| 1.0 | Jan 2025 | Initial global harmonized policy aligned to AI-assisted lending models - Bank Policy that should be referred to to make the decisions for applications, chat should output loan decisions based on this. |

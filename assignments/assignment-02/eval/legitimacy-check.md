I ran my legitimacy agent on 2 job posting
1. Real : `jobs/canonical.json`
2. Fake : `jobs/nexora.json`

It correctly analyzed and captured clearly key points to check the legitimacy of the jobs :
I put the result in `data/analysis/legitimacy-analysis-fake` for fake posting and `data/analysis/legitimacy-analysis-green` for real posting analysis


Fake posting (Nexora): Agent flagged red (95% confidence) : caught no verifiable company presence, a $200 "refundable" deposit, WhatsApp/Telegram-only hiring, requests for ID/banking pre-offer, and pay math that didn't add up. Agree — solid, well-supported call.

Real posting (Canonical): Agent flagged green (95% confidence) : matched the live listing on Canonical's actual careers page, verified a 30-year domain, and found no PII/payment requests anywhere. the strongest evidence (matching the real domain's live posting) backs this up well.
# Phase 3: Application Advisor — Specification

## Goal
A CLI/TUI tool that takes a new job posting PDF and produces a single HTML
application report (`reports/application-report.html`), using everything
already built in Phase 1 and Phase 2.

## Input
A command-line argument pointing to a new job posting PDF. 

## Requirement 1: TUI input
Accept a new job posting PDF path as a CLI argument.

## Requirement 2: Extract the new posting
Reuse Phase 1 logic exactly — do not reimplement:
- `helper.pdf_extraction` for PDF → text
- `tools.assess_job_tool` + `schema.job_schema.JobSchema` for structured extraction
- `tools.web_search_tool` for company research
- `src/prompts/JOB-ANALYSIS-PROMPT.md` as the agent's system prompt
Output: structured JSON for this one new posting (same shape as `data/jobs/*.json`).

## Requirement 3: Legitimacy Agent
Takes the job json produced from Requirement 2 , and use tht to investigate:
Tools : [web_search tool , and new WHOIS lookup whois_lookup tool]
New agent, new tools, new schema , PROMPT — none of this exists yet.

### New tool: WHOIS lookup
- Input: a domain name (e.g. `acmecorp.com`)
- Output: registrant organization (if available), registration date,
  expiration date, registrar, country
- Must handle errors gracefully: domain not found, WHOIS data redacted by
  privacy services (registration date is often still visible even when
  other fields are redacted — treat that field as the most reliable signal)

### New schema: `schema/legitimacy_schema.py`
Structured legitimacy assessment including:
- An overall verdict (green/yellow/red or a confidence score)
- A list of specific signals found (both red and green flags), each with
  supporting evidence
- A recommendation to the user, in plain language

You can make the schema better this si to give you the idea , since this schema will be used to get the information later

### New tool: `assess_legitimacy_tool`
Same pattern as `assess_job_tool`/`assess_market_tool` — forces the agent
to stop and organize its findings into the legitimacy schema, only after
it has finished researching. Do not call this before research is complete.

### New prompt: `src/prompts/LEGITIMACY-PROMPT.md`
Follow the same structure as existing prompts (`<role>`, `<input>`, `<output>`,
`<tools>`, `<flow>`, `<grounding_rules>`, `<error_handling>`). The flow should
instruct the agent to:
1. Read the new posting's JSON (from Requirement 2) for company name, contact
   info, compensation, and posting content.
2. Use `web_search_tool` to check for the company's web presence, LinkedIn
   page, news coverage, employee reviews (Glassdoor/Indeed), and whether the
   job appears on the company's own careers page.
3. Use the WHOIS tool to check the company's domain registration date and
   related info.
4. Weigh red flags against green flags (see list below) before concluding.
5. Call `assess_legitimacy_tool` with the complete structured verdict.

Red flags to instruct the agent to consider:
- Sensitive PII requested upfront (SSN/SIN, banking info, gov ID, DOB)
- Little to no verifiable web presence
- Domain registered very recently (via WHOIS)
- Contact email domain doesn't match the company
- Job not listed on the company's official careers page
- Compensation dramatically above market rate (compare to Phase 1 market data)
- Upfront payment, equipment purchases, or "training fees" required
- Extremely vague/generic job description
- Posting exists on job boards but company has no other online footprint

Green flags to instruct the agent to consider:
- Established web presence with history (site, LinkedIn, news, reviews, Wayback Machine)
- Domain registered for years (via WHOIS)
- Job listed on the company's own careers page
- Contact email matches company domain
- Salary consistent with Phase 1 market data
- Specific, detailed requirements tied to real technologies/projects
- Employee reviews present on Glassdoor/Indeed

## Requirement 4: Fit / Application Analysis

Load, read-only  do NOT regenerate or re-run any prior phase's pipeline:
- `data/analysis/market-analysis.json` (Phase 1)
- `data/resume/resume.json` (Phase 2)
- This posting's structured JSON, produced in Requirement 2

Analyze the new posting against the resume and market context using a new
agent with `web_search_tool` available, for verifying specific facts needed
in cover letter guidance or interview prep (e.g. confirming a recent company
announcement or product launch).

### New schema: `schema/application_analysis_schema.py`
Define `ApplicationAnalysisSchema` with these top-level sections:
- `fit_assessment`: fit score (0-100), a recommendation band, encouraging
  recommendation text, a full requirement-by-requirement breakdown (Met /
  Partially Met / Gap with evidence), and an overall narrative assessment.
- `resume_adaptation`: a list of specific, concrete resume tailoring suggestions
  tied to this exact posting — never generic advice.
- `cover_letter_guidance`: a list of specific talking points for this role/company.
- `interview_prep`: likely questions, skills to review, company research points,
  and talking points connecting the candidate's experience to this posting.

have these detailed fields , I provided overall idea make sure if we have right fiedls the our later report will be better since it will using this schema to create the report , so add the fields properly. and can include whatever you think is necessary


### New tool: `assess_application_tool`
Follows the same pattern as `assess_job_tool`/`assess_market_tool`/
`assess_legitimacy_tool` — forces the agent to stop and organize its complete
analysis into `ApplicationAnalysisSchema` only after it has finished comparing
the posting against the resume/market/gap data and completed any needed research.
Saves the structured result to `data/analysis/application-analysis.json` via the
existing `PathContext` pattern.

### Fit scoring constraint
The scoring system must actively counter candidates under-applying. Never
produce a flat "you are not qualified, don't apply" verdict for a reasonable
match. Use bands roughly like:
| Score | Band | Recommendation |
|---|---|---|
| 80%+ | Strong fit | Definitely apply |
| 50-80% | Good fit | Meets core requirements — apply and highlight strengths |
| 30-50% | Stretch | Worth applying if the role is exciting — here's how to position |
| <30% | Growth target | Significant gaps — treat as a growth target, not an immediate application |
Exact ranges/labels are flexible, but the tone must always encourage a reasonable candidate to apply, per the assignment's framing that postings describe ideal candidates, not minimum requirements.

### New Prompt: `APPLICATION-ANALYSIS-PROMPT.md`

write full instructions , which tools you are given and all everything for requirement 4 


## Requirement 5: HTML Application Report

Generate a single-page HTML + CSS report (self-contained, visually polished),
saved to `reports/application-report.html`. Built deterministically from the
already-validated structured data (Requirement 3's `LegitimacySchema` output
and Requirement 4's `ApplicationAnalysisSchema` output) — do not have an LLM
re-author this content freeform; render it directly from the structured JSON
already produced, to guarantee the report matches the data exactly.

Must include, in this exact order:

1. **Legitimacy Assessment** — shown FIRST, before any application advice.
   - Display the overall verdict prominently (green/yellow/red or confidence score)
   - List the specific signals found (red and green flags) with their evidence
   - If the verdict indicates the posting may be fraudulent, the section must
     lead with a clear, visually unmissable warning (e.g. a red banner) —
     the remaining sections still render below it (still useful context),
     but it must be obvious the user should not submit personal information.

2. **Fit Assessment** — from `fit_assessment`:
   - Fit score and recommendation band, displayed prominently
   - Requirement-by-requirement breakdown (Met / Partially Met / Gap) with evidence
   - Overall narrative assessment
   - Recommendation text must read as encouraging, per the fit scoring constraint in Req 4

3. **Resume Adaptation** — from `resume_adaptation`: each suggestion with its reason, specific to this posting.

4. **Cover Letter Guidance** — from `cover_letter_guidance`: each point with its reason.

5. **Interview Prep** — from `interview_prep`: likely questions, skills to review, company research points, talking points — each as its own labeled subsection.

### Format constraints
- Single HTML file, inline `<style>` (no external CSS files)
- Visually polished — clear section headings, readable typography, use color
  purposefully (e.g. green/yellow/red for the legitimacy verdict, a visual
  score indicator for fit score)
- Do not use emojis , instead make the report visually appealing with proper CSS 
- Report must be generated even when the legitimacy verdict is negative —
  never suppress the other sections, only ensure the warning is prominent
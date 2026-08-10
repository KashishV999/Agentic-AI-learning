# Phase 2

## What This Phase Does

Phase 2 takes the candidate's resume, turns it into a structured record, and
compares that record against the market analysis from Phase 1. The goal is
to show where the candidate already matches the market, where the gaps are,
and what actions would improve competitiveness.

## Flow

1. The phase starts with the candidate's resume as a PDF.

2. The resume goes through the `pdf_extraction` helper, which extracts raw
   text so the LLM can read and analyze the resume content.

3. That text is passed to the Resume Extraction Agent (`Assistant`,
   `RESUME-ANALYSIS-PROMPT.md`), which reads the full resume and extracts
   skills, work experience, education, certifications, projects, and
   accomplishments.

   Tools:
   - `assess_resume_tool` — the structured output step. Organizes the resume
     into `ResumeSchema`, validates it, and saves the structured resume JSON.

4. Once the resume is extracted, the phase loads two structured inputs
   together: the resume JSON from this phase, and the market analysis JSON
   from Phase 1.

5. Those two go to the Resume Gap Analysis Agent (`Assistant`,
   `RESUME-GAP-ANALYSIS-PROMPT.md`), which compares the resume against the
   market analysis and answers four questions: what strengths already match
   the market, what gaps are missing or underrepresented, what unique value
   the candidate has, and what action plan to follow next.

   Tools:
   - `web_search_tool` — used when the agent needs concrete, current details
     for recommendations, like certification names or time/cost estimates.
   - `assess_gap_analysis_tool` — the structured output step. Organizes the
     comparison into `GapAnalysisSchema` and saves the structured gap
     analysis JSON.
   - `save_disk_tool` — saves a Markdown version of the gap analysis once
     the structured analysis is complete.

6. The phase ends with a structured resume profile and a structured gap
   analysis. The gap analysis is what later helps explain how the candidate
   should improve or position themselves.

## Main Helpers and Schema

- `pdf_extraction` — converts the resume PDF into text for the LLM.
- `save_disk` — writes outputs to disk.
- `debug_logging` — adds optional debug traces when enabled.
- `ResumeSchema` — defines the structured resume format.
- `GapAnalysisSchema` — defines strengths, gaps, unique value, and the action plan.

## Output Summary

- One structured resume JSON
- One structured gap analysis JSON
- Intended Markdown gap analysis report

## Important Note

The runtime saves the structured gap analysis JSON. The gap analysis agent
is also configured with `save_disk_tool`, so a Markdown report is expected
as well.
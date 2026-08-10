# Phase 3

## What This Phase Does

Phase 3 is the application advisor pipeline. It takes one new target job posting, checks whether that posting looks legitimate, checks how well the candidate fits it, and then produces a final report that helps the candidate decide how to apply and how to tailor the application.

## Flow

1. The phase starts with one new target job posting as a PDF.
   This is the specific job the candidate is now considering applying to.

2. That PDF is passed through the `pdf_extraction` helper.
   Just like earlier phases, this helper converts the PDF into text so the LLM can read and analyze the posting content.

3. The extracted text is passed to the first agent: the job extraction agent.
   Prompt file: `JOB-ANALYSIS-PROMPT.md`

   This agent reuses the existing job extraction logic from earlier work. Its job is to turn the target posting into the same structured job format used elsewhere in the project.

   Tools used by this agent:

   - `web_search_tool`
     Used to research the company and gather supporting context around the posting.
   - `assess_job_tool`
     Used as the structured output step. It forces the result into the `JobSchema`, validates it, and saves the structured job JSON file.

4. Once the target posting is structured, the system combines it with the already available background context from the earlier phases.
   That background context is the structured resume.json and the earlier market analysis.json.

5. The structured target posting and market context are passed to the second agent: the legitimacy analysis agent.
   Prompt file: `LEGITIMACY-PROMPT.md`

   This agent investigates whether the posting looks trustworthy, suspicious, or risky.

   Tools used by this agent:

   - `web_search_tool`
     Used to verify the company website, careers page, public presence, reviews, and related evidence.
   - `whois_lookup_tool`
     Used to inspect the verified company domain and gather WHOIS evidence such as registration timing and registrar details.
   - `assess_legitimacy_tool`
     Used as the structured output step. It organizes the result into the `LegitimacySchema`, validates it, and saves the legitimacy analysis JSON.

6. The structured target posting, the structured resume, and the market analysis are passed to the third agent: the application analysis agent.
   Prompt file: `APPLICATION-ANALYSIS-PROMPT.md`

   This agent decides how strong the candidate fit is and how the candidate should approach the application.

   Tools used by this agent:

   - `web_search_tool`
     Used when recent company context would improve application guidance, especially for cover letter or interview preparation.
   - `assess_application_tool`
     Used as the structured output step. It forces the analysis into the `ApplicationAnalysisSchema`, validates it, and saves the application analysis JSON.

7. After both structured analyses are ready, they are passed to the fourth agent: the report rendering agent.
   Code-level name: `Application Report Renderer`
   Prompt file: `APPLICATION-REPORT-PROMPT.md`

   This agent does not do new research. It simply reads the validated legitimacy analysis and validated application analysis and turns them into one final HTML report.

   Tools used by this agent:

   - No function tools
     It returns the full HTML directly, and the project saves that HTML to disk afterward.

8. The phase ends with three main outputs.
   One structured legitimacy analysis, one structured application analysis, and one final HTML application report.

## Main Helpers and Schema

- `pdf_extraction`
  Converts the target posting PDF into text for the LLM.
- `save_disk`
  Saves the final HTML report.
- `debug_logging`
  Adds optional debug traces when enabled.
- `JobSchema`
  Defines the structured target posting format.
- `LegitimacySchema`
  Defines the legitimacy investigation output.
- `ApplicationAnalysisSchema`
  Defines fit assessment, resume adaptation, cover letter guidance, and interview prep.

## Output Summary

- One structured job JSON for the target posting
- One structured legitimacy analysis JSON
- One structured application analysis JSON
- One final HTML application report

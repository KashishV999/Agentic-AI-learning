# Phase 1

Phase 1 is the job market analysis phase. It takes raw job postings, turns
each one into a structured record, then analyzes all the records together to
understand what the market is asking for. By the end, the system has
structured data for every posting plus one combined market analysis in both
JSON and Markdown form.

## Flow

### Agent 1 — Job Extraction

1. The phase starts with a raw job posting PDF.

2. The PDF goes through the `pdf_extraction` helper, which extracts raw text
   from it — the LLM needs plain text, not a binary file.

3. That text is passed to the Job Extraction Agent (`JOB-ANALYSIS-PROMPT.md`),
   which reads one posting at a time and pulls out the key job details.

4. This agent has two tools:
   - `web_search_tool` — researches the hiring company for extra context.
   - `assess_job_tool` — the structured thinking step. It forces the agent
     to organize everything into `JobSchema` before saving anything.

5. `assess_job_tool` validates the result against `JobSchema`, so the agent
   has to produce a complete structured record, not loose text. Once it
   passes validation, the system saves a structured job JSON file.

6. This repeats for every posting — PDF to text, through the Job Extraction
   Agent, saved as its own structured JSON file.

### Agent 2 — Market Analysis

7. Once all postings are processed, the script loads every extracted job
   JSON file. From here on, the system works with clean structured data
   instead of raw PDFs.

8. That combined data goes to the Market Analysis Agent
   (`JOB-MARKET-ANALYSIS-PROMPT.md`), which looks across all postings for
   patterns — recurring skills, experience expectations, salary signals,
   industry representation, common role structure.

9. This agent has two tools:
   - `assess_market_tool` — the structured thinking step, organizing findings
     into `MarketSchema` before saving.
   - `save_disk_tool` — writes a human-readable Markdown report once the
     structured analysis is done.

10. The phase ends with two outputs: the aggregated market analysis as
    structured data, and a Markdown report built from the same findings.

- Prompt files: `JOB-ANALYSIS-PROMPT.md`, `JOB-MARKET-ANALYSIS-PROMPT.md`
- Tools: `web_search_tool`, `assess_job_tool`, `assess_market_tool`, `save_disk_tool`
- Helper: `pdf_extraction`
- Schemas: `JobSchema`, `MarketSchema`
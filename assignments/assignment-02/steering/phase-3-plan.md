# Phase 3 Implementation Plan

  ## Summary

  Build phase_3.py as a CLI-only pipeline that accepts a new job PDF, reuses the existing Phase 1 extraction
  components for a single posting, runs two new agents (legitimacy and application analysis), and renders a
  deterministic HTML report at reports/application-report.html.

  ## Existing Reuse

  These are the existing repo surfaces I would import and reuse directly:

  - src/helper/pdf_extraction.py: pdf_extraction
  - src/helper/get_file_contents.py: get_file_contents
  - src/helper/save_disk.py: save_disk
  - src/config.py: PROMPTS_FOLDER, JOBS_JSON_FOLDER, RESUME_JSON_FOLDER, ANALYSIS_FOLDER, REPORTS_FOLDER
  - src/tools/web_search_tool.py: web_search_tool
  - src/tools/assess_job_tool.py: assess_job_tool
  - src/tools/save_disk_tool.py: save_disk_tool pattern for report writes
  - src/schema/job_schema.py: JobSchema
  - src/prompts/JOB-ANALYSIS-PROMPT.md: canonical reused job-extraction prompt
  - Read-only artifacts: data/analysis/market-analysis.json and data/resume/resume.json

  I would not modify src/phases/phase_1.py. Phase 3 will recreate only the minimal runtime wiring it needs
  while reusing the same helper/tool/schema/prompt building blocks already used by Phase 1.

  ## Implementation Steps

  1. Build standalone Phase 3 job-extraction wiring
      - In phase_3.py, add local runtime setup matching the existing Phase 1 pattern: model provider setup,
        PathContext, prompt loading, and single-posting extraction flow.

      - Reuse pdf_extraction, assess_job_tool, web_search_tool, JobSchema, and JOB-ANALYSIS-PROMPT.md.
      - Save the extracted posting as data/jobs/<input-stem>.json.
      - Leave phase_1.py unchanged.

  2. Add legitimacy analysis primitives
      - Add schema/legitimacy_schema.py with verdict, confidence, recommendation, and evidence-backed signal
        entries.

      - Add tools/whois_lookup_tool.py using python-whois, returning normalized fields plus graceful error/
        redaction status.

      - Add tools/assess_legitimacy_tool.py following the existing schema-save pattern.
      - Add src/prompts/LEGITIMACY-PROMPT.md.

  3. Add application-analysis primitives
      - Add schema/application_analysis_schema.py with:
          - fit_assessment
          - resume_adaptation
          - cover_letter_guidance
          - interview_prep

      - Include nested requirement breakdown entries with status (Met / Partially Met / Gap) and evidence.
      - Add tools/assess_application_tool.py.
      - Add src/prompts/APPLICATION-ANALYSIS-PROMPT.md with the encouraging fit-band policy.

  4. Implement deterministic HTML rendering
      - Add a pure Python renderer that reads structured legitimacy + application JSON and writes reports/
        application-report.html via save_disk.

      - Enforce section order from the spec.
      - Always render all sections; if legitimacy is negative, prepend a prominent warning banner.

  5. Implement phase_3.py orchestration
      - CLI: python3 src/phases/phase_3.py /path/to/new-job.pdf
      - Flow:
          - validate input path
          - extract posting to data/jobs/<input-stem>.json
          - run legitimacy agent to data/analysis/legitimacy-analysis.json
          - run application agent using market-analysis.json, resume.json, and the new posting JSON, saving
            data/analysis/application-analysis.json

          - render final HTML report

      - Fail fast on missing required prior artifacts; do not regenerate earlier phases.

  6. Validation and acceptance pass
      - Manual run with a known job PDF.
      - Verify every output file exists and matches the expected schema/section order.
      - Check one suspicious posting case to confirm the red warning still leaves the rest of the report
        visible.

  ## Public Interfaces / Additions

  - New CLI entrypoint: python3 src/phases/phase_3.py <job-posting.pdf>
  - New structured outputs:
      - data/analysis/legitimacy-analysis.json
      - data/analysis/application-analysis.json
      - reports/application-report.html

  - New symbols:
      - whois_lookup_tool
      - assess_legitimacy_tool
      - assess_application_tool

  ## Test Plan

  - Happy path: valid PDF, prior Phase 1/2 artifacts present, all three new outputs created.
  - Missing prerequisite files: clear error if market-analysis.json or resume.json is absent.
  - WHOIS edge cases: nonexistent domain, privacy-redacted domain, malformed domain.
  - Legitimacy negative case: red verdict banner renders first, remaining advice still renders.
  - Fit-band checks: examples near band boundaries still produce encouraging recommendation text.
  - Determinism check: given the same structured JSON inputs, the HTML renderer emits the same content.

  ## Assumptions

  - src/prompts/JOB-ANALYSIS-PROMPT.md remains the canonical reused prompt; the spec’s JOB-SYSTEM-PROMPT.md
    name is treated as outdated.

  - The extracted Phase 3 posting is persisted alongside existing job JSONs at data/jobs/<stem>.json.
  - Phase 3 is CLI-only; no interactive TUI beyond the required command-line PDF argument.
  - gap-analysis.json is not a required Phase 3 input unless the spec is expanded later.
  - WHOIS support will be added as a new Python dependency rather than relying on a system-installed whois
    binary.
  # Phase 3 Report Rendering Revision

  ## Summary

  Replace the current code-rendered HTML report with a final report-generation agent that takes only the
  validated LegitimacySchema and ApplicationAnalysisSchema JSON outputs and returns a polished single-file HTML
  report. Keep the existing extraction, legitimacy, and application-analysis pipeline intact; only the final
  rendering stage changes.

  ## Key Changes

  - Add a new report-rendering prompt that:
      - accepts only the two structured JSON inputs
      - enforces the exact Phase 3 section order
      - requires inline CSS and polished HTML
      - forbids inventing facts or using any source outside the provided JSON

  - Update src/phases/phase_3.py so the final step becomes:
      - load legitimacy-analysis.json
      - load application-analysis.json
      - call a report agent with those JSON blobs only
      - save the returned HTML to reports/application-report.html

  - Remove src/helper/application_report.py from the Phase 3 rendering path so HTML is no longer built by Python
    string templates.

  - Add output guardrails in phase_3.py before saving:
      - response must be HTML
      - legitimacy section must appear first
      - all required sections must exist
      - red-verdict warning banner must appear when legitimacy is red

  - Keep the schemas and analysis tools unchanged so the structured outputs remain the ground truth.

  ## Public Interfaces / Behavior

  - python3 src/phases/phase_3.py <job-posting.pdf> remains the Phase 3 entrypoint.
  - Final report generation changes from deterministic Python rendering to schema-grounded LLM rendering.
  - The report agent’s input contract is:
      - LegitimacySchema JSON
      - ApplicationAnalysisSchema JSON
      - no raw posting text
      - no resume JSON
      - no market-analysis JSON

  - The report agent’s output contract is:
      - one complete HTML document
      - inline <style>
      - no markdown
      - no surrounding commentary

  ## Test Plan

  - Verify the report agent returns valid HTML with all required sections in the exact order:
      - Legitimacy Assessment
      - Fit Assessment
      - Resume Adaptation
      - Cover Letter Guidance
      - Interview Prep

  - Verify a red legitimacy verdict produces a prominent warning banner near the top of the HTML.
  - Verify no content appears that is not supported by the two schema JSON inputs.
  - Verify the output is visually richer than the current card dump while still preserving the schema facts.
  - Verify phase_3.py fails clearly if the report response is not HTML or is missing required sections.

  ## Assumptions

  - The existing legitimacy and application-analysis agents continue producing the authoritative structured
    JSON.

  - The final HTML may vary slightly in wording between runs; this is acceptable because the schema remains the
    only allowed source of truth.

  - Presentation quality is now prioritized over full deterministic rendering, as long as section structure and
    factual grounding remain tightly constrained.
    </proposed_plan>
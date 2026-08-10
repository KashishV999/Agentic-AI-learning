# Add Debug Logging via LOG_LEVEL=debug

  ## Summary

  Introduce a lightweight debug logger that activates only when LOG_LEVEL=debug, writes exclusively to stderr,
  and provides concise diagnostics for Phase 1, Phase 2, and Phase 3 without changing normal stdout behavior.
  Create a new .env.example with LOG_LEVEL= documented. Replace current noisy print() usage inside helpers/
  tools that would interfere with normal output.

  ## Implementation Changes

  - Add a shared helper such as src/helper/debug_logging.py with:
      - is_debug_enabled()
      - debug_log(message: str)
      - small formatters for safe argument/value rendering
      - all output sent to sys.stderr

  - Use one simple format consistently:
      - [DEBUG] Agent start: Job Extraction Assistant
      - [DEBUG] Tool call: whois_lookup_tool(domain="acmecorp.com")
      - [DEBUG] Extraction summary: type=job extracted_fields=["job_title","company_info","location"]
        missing_or_unknown=3

  - Add .env.example at repo root with:
      - OPENROUTER_API_KEY=
      - OPENAI_TRACING_KEY=
      - TAVILY_API_KEY=
      - LOG_LEVEL=
      - comment that debug enables diagnostic logging to stderr

  - In all three phase entrypoints, log:
      - phase/stage start and completion
      - agent name before each Runner.run(...)
      - input file path and output file path
      - skipped work decisions such as “already processed” and missing prerequisite files
      - report validation failures in Phase 3 before raising

  - In helpers/tools, log:
      - pdf_extraction: file path, request start, success/failure, response status, extracted character count
      - save_disk: target path, save success/failure, byte/character count
      - web_search_tool: query string, result count, API-key-missing failure
      - whois_lookup_tool: normalized domain, lookup success/error, whether key WHOIS fields were available
      - all assess_* tools: tool invocation, output path, schema type saved, top-level extracted field names
        only

  - Do not rely on SDK verbose stdout logging. Either disable enable_verbose_stdout_logging() entirely or gate
    it off unless the SDK can be redirected to stderr; the app-level logger is the source of truth for this
    feature.

  ## What To Log

  - High-signal events only:
      - agent start/end
      - tool call with short safe arguments
      - tool result summaries
      - extraction/report save decisions
      - validation failures and retries when explicitly caught in app code

  - For extraction decisions, log:
      - top-level field names that are populated
      - count of unknown/missing fields
      - schema validation failure summary if a tool invocation fails and is retried

  - For tool arguments, log only safe/truncated values:
      - safe: domain, query, output path, file path, counts, verdict, score
      - unsafe/noisy: full resume text, full job text, full HTML output, full JSON payloads

  - Default truncation:
      - strings truncated to about 120-160 chars
      - sequences/maps summarized as counts or key names, not full content

  ## Public Interfaces / Behavior

  - New environment variable:
      - LOG_LEVEL=debug enables debug logging
      - any other value or unset means no debug logs

      - normal script output remains on stdout

  - Run each phase with LOG_LEVEL unset:
      - confirm no new debug lines appear
      - confirm normal behavior/output is unchanged

  - Run each phase with LOG_LEVEL=debug:
      - confirm debug lines appear on stderr
      - confirm stdout still contains only normal user-facing output

  - Verify representative events:
      - skipped extraction logs
      - agent start logs
      - web_search_tool and whois_lookup_tool call/result logs
      - save success logs
      - Phase 3 HTML validation failure logs

  - Verify redaction/noise limits:
      - no full resume text in logs
      - no full job posting text in logs
      - no full JSON schema dumps in logs
      - no HTML body dumps in logs

  ## Assumptions

  - .env.example should be created because it does not currently exist.
  - The implementation should prefer a custom app logger over OpenAI Agents SDK verbose logging, since the
    current SDK verbose mode writes to stdout and conflicts with the requirement.

  - Validation/retry logging will only cover retries/failures the application actually controls; it will not
    attempt deep SDK instrumentation unless a clean non-invasive hook exists in the installed S
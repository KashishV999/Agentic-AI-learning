# Assignment   1
# AI Code Review Pipeline

An automated, multi-agent code review tool. It sends your code (a staged git diff, or a specific file) to two independent AI reviewers, then has a third "judge" agent synthesize both reviews into a single, polished HTML report.

## How it works

The pipeline runs three AI agents in sequence:

1. **Security Auditor** 
   Scans the code for security vulnerabilities
2. **Senior Architect** : 
   Reviews the code for design problems .

   Both reviewers run **in parallel** and have access to two tools : `read_file` and `ripgrep` which let them pull in extra context from the codebase (e.g. a function's definition) beyond what's visible in the diff alone.

3. **Lead Developer / Judge** (`anthropic/claude-sonnet-4.6`)
   Takes both reviewers' findings  and writes a single self-contained HTML report.

## Requirements

- Python 3.10+
- [ripgrep](https://github.com/BurntSushi/ripgrep) installed and on your `PATH`
  ```bash
  brew install ripgrep      # macOS
  apt-get install ripgrep   # Linux
  ```
- An OpenRouter API key, set in a `.env` file in the project (or any parent directory):
  ```
  OPENROUTER_API_KEY=your_key_here
  ```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

By default, the tool reviews your **currently staged git changes**:

```bash
python3 main.py
```

This is equivalent to reviewing the output of `git diff --staged`. Make sure you've run `git add` on the files you want reviewed before running the tool.

### Arguments

| Flag | Required | Description |
|---|---|---|
| `--file <path>` | No | Review a specific file in full, instead of the staged git diff. |
| `--output <filename>` | No | Filename for the generated HTML report. Defaults to `review-<timestamp>.html` in the current directory. |
| `--debug` | No | Print detailed step-by-step logs (LLM calls, tool calls, tool results, final JSON output) to `stderr`. Useful for seeing exactly what each agent is doing. |

### Examples

Review staged changes, default output filename:
```bash
python3 main.py
```

Review a specific file:
```bash
python3 main.py --file bad_code.py
```

Review staged changes with debug logging visible:
```bash
python3 main.py --debug
```

Review a specific file, custom output name, with debug logs saved to a file:
```bash
python3 main.py --file src/api/users.py --output users_review.html --debug 2> debug.log
```

## Output

The tool writes a single self-contained HTML file (no external CSS/JS) containing the synthesized report — an executive summary, followed by findings grouped by severity (critical → warn → info), each tagged with its file path, line number, category, and a specific description of the issue and suggested fix.


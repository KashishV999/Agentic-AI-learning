import os
import re
import csv
import sys
import time

from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# -----------------------------------------------------------------------------
# Environment Configuration
# -----------------------------------------------------------------------------

load_dotenv(find_dotenv())
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

JUDGE_MODEL = "openai/gpt-4o"

ANSWER_FILES = {
    "llama-3.3-70b": "answers_llama.md",
    "mistral-small-3.2-24b": "answers_mistral.md",
    "gpt-4o-mini": "answers_gpt4omini.md",
}

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)


# -----------------------------------------------------------------------------
# File Utilities
# -----------------------------------------------------------------------------

def get_file_contents(path: str, description: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: {description} not found: {path}")
        sys.exit(1)
    except Exception as err:
        print(f"❌ Error reading {description}: {path}")
        print(f"   {err}")
        sys.exit(1)


def parse_blocks(text: str) -> dict:
    """Split a file into {qid: text} using [R1] style markers."""
    pat = re.compile(r"^\[?([RCWFE]\d)\]", re.M)
    hits = list(pat.finditer(text))
    out = {}
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(text)
        out[m.group(1)] = text[m.end():end].strip()
    return out


# -----------------------------------------------------------------------------
# Judge Integration
# -----------------------------------------------------------------------------

def parse_scores(reply: str) -> dict:
    def grab(name):
        m = re.search(rf"{name}:\s*(\d)", reply)
        return int(m.group(1)) if m else None

    total = re.search(r"Total:\s*(\d+)\s*/\s*20", reply)
    return {
        "accuracy": grab("Accuracy"),
        "helpfulness": grab("Helpfulness"),
        "clarity": grab("Clarity"),
        "safety": grab(r"Safety/Tone"),
        "total": int(total.group(1)) if total else None,
    }


def judge_one(system_prompt: str, question: str, answer: str) -> str:
    for attempt in range(3):
        try:
            r = client.chat.completions.create(
                model=JUDGE_MODEL,
                temperature=0,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": f"Question: {question}\n\nAnswer: {answer}",
                    },
                ],
            )
            return r.choices[0].message.content
        except Exception as e:
            print(f"  retry {attempt + 1}: {e}")
            time.sleep(5)
    raise RuntimeError("Judge call failed 3 times")


# -----------------------------------------------------------------------------
# Output Writers
# -----------------------------------------------------------------------------

def write_csv(rows: list) -> None:
    with open("judge_scores.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("Wrote judge_scores.csv")


def write_md_table(rows: list, questions: dict) -> None:
    """Table with judge totals out of 20."""
    order = [c + str(i) for c in "RCWFE" for i in range(1, 6)]
    models = list(ANSWER_FILES.keys())
    scores = {(r["qid"], r["model"]): r["total"] for r in rows}

    lines = [
        "# Judge Scores (GPT-4o as judge, /20 per answer)",
        "",
        "| ID | Question | LLaMA 3.3 70B | Mistral Small 3.2 | GPT-4o mini |",
        "|---|---|---|---|---|",
    ]
    for qid in order:
        q = questions.get(qid, "").split("\n")[0][:60]
        vals = [str(scores.get((qid, m), "-")) for m in models]
        lines.append(f"| {qid} | {q} | {vals[0]} | {vals[1]} | {vals[2]} |")

    avgs = []
    for m in models:
        ts = [r["total"] for r in rows if r["model"] == m and r["total"] is not None]
        avgs.append(f"{sum(ts) / len(ts):.2f}" if ts else "-")
    lines.append(f"| **Avg** | | **{avgs[0]}** | **{avgs[1]}** | **{avgs[2]}** |")

    with open("judge_scores_table.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("Wrote judge_scores_table.md")


def write_md_table_5(rows: list, questions: dict) -> None:
    """Table with judge totals converted to out of 5 (total / 4),
    directly comparable with the human consensus grades."""
    order = [c + str(i) for c in "RCWFE" for i in range(1, 6)]
    models = list(ANSWER_FILES.keys())
    scores = {(r["qid"], r["model"]): r["total"] for r in rows}

    lines = [
        "# Judge Scores Out of 5 (total / 4)",
        "",
        "| ID | Question | LLaMA 3.3 70B | Mistral Small 3.2 | GPT-4o mini |",
        "|---|---|---|---|---|",
    ]
    for qid in order:
        q = questions.get(qid, "").split("\n")[0][:60]
        vals = []
        for m in models:
            t = scores.get((qid, m))
            vals.append(f"{t / 4:.2f}" if t is not None else "-")
        lines.append(f"| {qid} | {q} | {vals[0]} | {vals[1]} | {vals[2]} |")

    avgs = []
    for m in models:
        ts = [r["total"] for r in rows if r["model"] == m and r["total"] is not None]
        avgs.append(f"{(sum(ts) / len(ts)) / 4:.2f}" if ts else "-")
    lines.append(f"| **Avg** | | **{avgs[0]}** | **{avgs[1]}** | **{avgs[2]}** |")

    with open("judge_scores_table_5.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("Wrote judge_scores_table_5.md")


# -----------------------------------------------------------------------------
# Application Entry Point
# -----------------------------------------------------------------------------

def main():
    if not OPENROUTER_API_KEY:
        print("Error: OPENROUTER_API_KEY not found")
        sys.exit(1)

    print("OPENROUTER_API_KEY found successfully!")

    system_prompt = get_file_contents("SYSTEM_PROMPT.md", "Judge system prompt")
    questions = parse_blocks(get_file_contents("Question.md", "Questions file"))

    rows = []
    for model_name, path in ANSWER_FILES.items():
        answers = parse_blocks(get_file_contents(path, f"{model_name} answers"))
        for qid in questions:
            if qid not in answers:
                print(f"!! {model_name} missing {qid}, skipping")
                continue
            print(f"Judging {model_name} {qid} ...")
            reply = judge_one(system_prompt, questions[qid], answers[qid])
            s = parse_scores(reply)
            if s["total"] is None:
                print(f"  ⚠ could not parse total for {model_name} {qid}, check raw output")
            rows.append(
                {"qid": qid, "model": model_name, **s, "raw": reply.replace("\n", " | ")}
            )
            time.sleep(1)

    write_csv(rows)
    write_md_table(rows, questions)
    write_md_table_5(rows, questions)
    print(f"\nDone. {len(rows)} answers judged.")


if __name__ == "__main__":
    main()
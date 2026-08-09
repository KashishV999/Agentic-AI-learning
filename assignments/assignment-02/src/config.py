# src/config.py
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent      # .../assignment-02/src
PROJECT_ROOT = SRC_DIR.parent                    # .../assignment-02

DATA_FOLDER = PROJECT_ROOT / "data"

RAW_PDF_JOB_FOLDER = DATA_FOLDER / "raw_jobs_pdf"
RAW_RESUME_FOLDER = DATA_FOLDER / "raw_resume_pdf"

JOBS_JSON_FOLDER = DATA_FOLDER / "jobs"
RESUME_JSON_FOLDER = DATA_FOLDER / "resume"
ANALYSIS_FOLDER=  DATA_FOLDER / "analysis"

PROMPTS_FOLDER = SRC_DIR / "prompts"

REPORTS_FOLDER = PROJECT_ROOT / "reports"

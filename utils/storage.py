import json, os, pandas as pd
from pathlib import Path

DATA_DIR = Path("user_data")          # ← turn it into a Path object
DATA_DIR.mkdir(exist_ok=True)
# ── helper --------------------------------------------------------------
def _user_dir(email: str) -> Path:
    user_dir = DATA_DIR / email       # now Path / str works
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir

# ── PROFILE CRUD --------------------------------------------------------
def save_profile(email: str, profile: dict) -> None:
    """Write the profile dict as JSON into user_data/<email>/profile.json."""
    (_user_dir(email) / "profile.json").write_text(
        json.dumps(profile, indent=2)
    )

def load_profile(email: str) -> dict | None:
    p = _user_dir(email)/"profile.json"
    return json.loads(p.read_text()) if p.exists() else None
# ---------- daily log ----------
def append_daily(entry, email):
    print("DEBUG:", type(entry), type(email))
    # 1.  Build user-specific folder path  ───────────────────────────────
    user_dir = Path("user_data") / email  # user_data/<email>/
    user_dir.mkdir(parents=True, exist_ok=True)  # auto-create folder

    # 2.  CSV file that stores the 30-day log  ──────────────────────────
    csv_file = user_dir / "daily_log.csv"

    # 3.  Load existing data or start fresh  ────────────────────────────
    if csv_file.exists():
        df = pd.read_csv(csv_file)
    else:
        df = pd.DataFrame()

    # 4.  Append today’s record and write back  ─────────────────────────
    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(csv_file, index=False)


def read_daily(email: str) -> pd.DataFrame:
    """Return the entire daily log as a DataFrame (empty if none yet)."""
    csv_file = _user_dir(email) / "daily_log.csv"
    return pd.read_csv(csv_file) if csv_file.exists() else pd.DataFrame()


def reset_user(email: str) -> None:
    """Delete profile.json and daily_log.csv for a single user."""
    for f in (_user_dir(email) / "profile.json", _user_dir(email) / "daily_log.csv"):
        if f.exists():
            f.unlink()

def reset_all() -> None:
    """Delete every file under user_data/ (use with care!)."""
    for p in DATA_DIR.rglob("*"):
        if p.is_file():
            p.unlink()
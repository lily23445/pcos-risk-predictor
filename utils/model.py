import pandas as pd
import joblib

# ── 1.  Model loader ────────────────────────────────────────────────
_MODEL = None
def get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = joblib.load("pcos_model.pkl")   # path to your .pkl
    return _MODEL

# ── 2.  Human-to-training name map (only labs need aliases) ─────────
ALIAS = {
    "Age" : "Age (yrs)",
    "TSH" : "TSH (mIU/L)",
    "LH"  : "LH(mIU/mL)",
    "FSH" : "FSH(mIU/mL)",
    "AMH" : "AMH(ng/mL)",
    "PRL" : "PRL(ng/mL)",
}

# ── 3.  Feature list in *training* order ────────────────────────────
FEATURES = [
    "Age (yrs)", "BMI", "TSH (mIU/L)", "LH(mIU/mL)", "FSH(mIU/mL)",
    "AMH(ng/mL)", "PRL(ng/mL)",
    "Weight gain(Y/N)", "hair growth(Y/N)",
    "Skin darkening (Y/N)", "Pimples(Y/N)", "Hair loss(Y/N)",
]

# ── 4.  Helper to rename profile keys once ──────────────────────────
def _rename(d: dict) -> dict:
    return {ALIAS.get(k, k): v for k, v in d.items()}

# ── 5.  Build the 1-row feature frame for prediction ────────────────
def build_features(profile: dict, daily: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with the exact columns/dtypes the model expects."""
    daily = daily.rename(              # unify the five symptom headers
        columns={
            "Hair growth(Y/N)": "hair growth(Y/N)",
            "Skin darkening(Y/N)": "Skin darkening (Y/N)",
        }
    )

    # a) aggregate the five binary symptoms across all logged days
    symptoms = {
        "Weight gain(Y/N)"     : daily["Weight gain(Y/N)"].astype(int).max(),
        "hair growth(Y/N)"     : daily["hair growth(Y/N)"].astype(int).max(),
        "Skin darkening (Y/N)" : daily["Skin darkening (Y/N)"].astype(int).max(),
        "Pimples(Y/N)"         : daily["Pimples(Y/N)"].astype(int).max(),
        "Hair loss(Y/N)"       : daily["Hair loss(Y/N)"].astype(int).max(),
    }

    # b) labs & demographics from profile (after aliasing)
    prof = _rename(profile)
    labs = {k: prof.get(k, 0) for k in FEATURES[:7]}   # fill missing with 0

    # c) combine and enforce column orderr
    row = {**labs, **symptoms}
    X   = pd.DataFrame([row], columns=FEATURES)

    # d) cast numeric labs to float
    float_cols = ["BMI", "TSH (mIU/L)", "LH(mIU/mL)",
                  "FSH(mIU/mL)", "AMH(ng/mL)", "PRL(ng/mL)"]
    X[float_cols] = X[float_cols].apply(pd.to_numeric, errors="coerce")
    return X

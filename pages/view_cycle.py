import streamlit as st, pandas as pd, numpy as np
import utils.storage as store, utils.model as mdl
import utils.nav as nav
from utils.model import get_model, build_features

nav.render_menu()

email = st.user.email

if not st.user.is_logged_in:
    st.switch_page("Login.py")
if store.load_profile(email) is None:
    st.warning("Complete the Profile page first.")
    st.stop()

profile = store.load_profile(email)
daily   = store.read_daily(email)

st.title("📊 Cycle Status")
if profile is None or daily.empty:
    st.warning("Need both a profile and at least one daily entry.")
    st.stop()

# --- Progress bar (capped at 100 %) --------------------------------
progress_ratio = min(len(daily) / 30.0, 1.0)
st.progress(progress_ratio, text=f"{len(daily)}/30 days logged")

# --- Build feature row & predict -----------------------------------
X = build_features(profile, daily)
prob = get_model().predict_proba(X)[0, 1] * 100          # → percent

st.metric("PCOS-flare risk", f"{prob:.1f}%")

# Optional: show raw data
with st.expander("See aggregated features"):
    st.write(X)

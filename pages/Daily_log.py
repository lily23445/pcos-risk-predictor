import streamlit as st, utils.storage as store
from datetime import date
from utils.model import get_model
import utils.nav as nav
nav.render_menu()

email = st.user.email
if not st.user.is_logged_in:
    st.switch_page("Login.py")
if store.load_profile(email) is None:
    st.warning("Complete the Profile page first.")
    st.stop()

st.title("📝 Daily Symptom Log")

wg, hg, sd, pim, hl = st.columns(5)
with wg: wg_val  = st.selectbox("Weight Gain", ["0","1"])
with hg: hg_val  = st.selectbox("Hair Growth", ["0","1"])
with sd: sd_val  = st.selectbox("Skin Darkening", ["0","1"])
with pim: pim_val= st.selectbox("Pimples", ["0","1"])
with hl: hl_val  = st.selectbox("Hair Loss", ["0","1"])



# ─── Save button ──────────────────────────────────────────────
if st.button("Save today’s entry"):

    entry = {
        "Date":              str(date.today()),
        "Weight gain(Y/N)":  wg_val,
        "Hair growth(Y/N)":  hg_val,
        "Skin darkening(Y/N)": sd_val,
        "Pimples(Y/N)":      pim_val,
        "Hair loss(Y/N)":    hl_val,
    }



    # Call once, with BOTH required args: entry then email
    store.append_daily(entry, email)
    st.success("Saved ✔️")
    st.rerun()            # Streamlit ≥ 1.37
 # 2 run prediction
# risk_prob = get_model().predict_proba(X)[0,1] * 100
#
# store.append_daily(email, X.assign(i have given i
#     Risk=risk_prob,
#     Date=date.today().isoformat()
# ))
# st.toast("Saved to your 30-day log ✅")
#
#     # 3 display
# st.metric("Predicted PCOS-flare probability", f"{risk_prob:.1f}%")
#
# st.write("🛠️ Model class:", type(get_model()).__name__)

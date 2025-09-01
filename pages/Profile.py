# pages/1_👤_Profile.py
import streamlit as st
import utils.storage as store
import utils.nav as nav
from datetime import date
nav.render_menu()

# ────────────────────────────────────────────
# 1. Block access if somehow not authenticated
# ────────────────────────────────────────────
if not st.user.is_logged_in:           # Google OAuth must be active
    st.switch_page("Login.py")

email   = st.user.email
profile = store.load_profile(email) or {}

# ────────────────────────────────────────────
# 2. Header with user identity
# ────────────────────────────────────────────
st.set_page_config(page_title="Profile", page_icon="👤", layout="centered")

left, right = st.columns([1,4])
with left:
    st.image(st.user.picture, width=96)

with right:
    st.title("Your Medical Profile")
    st.write(f"**{st.user.name}**  \n{email}")

st.divider()

# quick badge
if profile:
    st.success("✅ Profile on file — edit below if needed")
else:
    st.warning("⚠️ No profile yet — please fill the form and press *Save*")

# ────────────────────────────────────────────
# 3. Two-column editable form
# ────────────────────────────────────────────
with st.form("profile_form", clear_on_submit=False):
    c1, c2 = st.columns(2)

    with c1:
        age   = st.number_input("Age (years)", 10, 60, value=profile.get("Age", 25))
        bmi   = st.number_input("BMI", 10.0, 60.0, value=profile.get("BMI", 22.0))
        waist = st.number_input("Waist (cm)", 40, 150, value=profile.get("Waist", 70))

    with c2:
        tsh = st.number_input("TSH (mIU/L)", 0.0, 20.0, value=profile.get("TSH", 2.0), format="%.2f")
        lh  = st.number_input("LH (mIU/mL)", 0.0, 50.0, value=profile.get("LH", 6.0), format="%.2f")
        fsh = st.number_input("FSH (mIU/mL)", 0.0, 50.0, value=profile.get("FSH", 5.0), format="%.2f")
        amh = st.number_input("AMH (ng/mL)", 0.0, 20.0, value=profile.get("AMH", 3.5), format="%.2f")
        prl = st.number_input("PRL (ng/mL)", 0.0, 50.0, value=profile.get("PRL", 12.0), format="%.2f")

    saved = st.form_submit_button("💾 Save / Update")

# ────────────────────────────────────────────
# 4. Persist on click

if st.button("Save profile"):
    store.save_profile(email, dict(
         Age=age,BMI=bmi, AMH=amh, TSH=tsh, LH=lh, FSH=fsh, PRL=prl,
        LastUpdated=date.today().isoformat()
    ))
    st.success("Profile saved ✔️")
    st.rerun()
# Home.py
import streamlit as st
from datetime import date
import utils.storage as store

email = st.user.email
if not st.user.is_logged_in:
    st.switch_page("Login.py")

import utils.nav as nav
nav.render_menu()

# ---------- page-wide style ----------
st.set_page_config(page_title="PCOS Care Hub",
                   page_icon="🩺",
                   layout="wide",
                   initial_sidebar_state="collapsed")

st.markdown("""
<style>
:root{
  --primary:#1565C0;
  --accent:#43A047;
}
html, body {font-family:'Inter',sans-serif;}
h1, h2, h3 {color:var(--primary);}
.hero-btn{
  background:var(--primary);
  color:#fff;
  padding:0.8rem 2.2rem;
  border:none;border-radius:6px;font-size:1.15rem;
}
.hero-btn:hover{background:#104d99;}
.tiny{text-transform:uppercase;letter-spacing:0.1rem;font-size:0.7rem;color:grey;}
.card{border:1px solid #eee;border-radius:8px;padding:1rem;text-align:center;}
.card:hover{box-shadow:0 4px 12px rgba(0,0,0,0.05);}
</style>
""", unsafe_allow_html=True)

# ---------- hero section ----------
st.markdown("<div style='padding:4rem 2rem;text-align:center;'>", unsafe_allow_html=True)
st.markdown("## 🩺 **PCOS 30-Day Care Hub**")
st.write("Track daily symptoms, understand your cycle risk, and get lifestyle guidance — all in one place.")
st.markdown("<br>", unsafe_allow_html=True)

cta_col = st.columns([3,1,3])[1]
with cta_col:
    st.page_link("pages/Profile.py", label="Get started →", icon="👤")
st.markdown("</div>", unsafe_allow_html=True)

# ---------- quick status tiles ----------
profile_ready = store.load_profile(email) is not None
days_done     = store.read_daily(email).shape[0]

st.markdown("#### Today’s status")
scol1, scol2, scol3 = st.columns(3)
scol1.metric("Profile", "Set" if profile_ready else "Missing",
             delta="✓" if profile_ready else "●")
scol2.metric("Days logged", f"{days_done}/30",
             delta=None if days_done==0 else f"+{days_done}")
scol3.metric("Date", date.today().strftime("%b %d, %Y"))

# ---------- navigation cards ----------
st.divider()
st.markdown("#### Navigate")
card_defs = [
    ("👤 Profile" ,      "Profile",  "One-time medical details"),
    ("📝 Daily Log",      "Daily_log", "Enter today’s symptoms"),
    ("📊 View Cycle",     "view_cycle", "See progress & risk"),
    ("💪 Exercise",       "exercise_recipie", "Workout suggestions"),
    # ("🥗 Diet",           "pages/5_🥗_Diet_Module.py", "Nutrition guidance"),
    # ("⚙️ Settings",       "pages/6_⚙️_Settings.py", "Reset or export data")
]




rows = st.columns(3)
for i, (label, target, subtitle) in enumerate(card_defs):
    with rows[i%3]:
        st.markdown(f"<div class='card'><b>{label}</b><br><span class='tiny'>{subtitle}</span><br><br>"
                    f"<a href='/{target}' target='_self' style='text-decoration:none;'>"
                    f"<button class='hero-btn' style='font-size:0.9rem;padding:0.5rem 1.4rem;'>Open</button>"
                    f"</a></div>", unsafe_allow_html=True)

if st.sidebar.button("Log out"):
    st.logout()
# ---------- footer ----------
st.markdown("<br><hr style='margin:2rem 0;'>"
            "<p style='text-align:center;font-size:0.8rem;'>© 2025 PCOS Care Hub</p>",
            unsafe_allow_html=True)

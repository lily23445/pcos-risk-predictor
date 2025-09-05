import streamlit as st
from datetime import date
import utils.storage as store           # adjust import paths as needed

# ---------- session guard ----------
email = st.session_state.get("email")
if email is None:
    st.switch_page("Login.py")

# ---------- page config ----------
st.set_page_config(page_title="PCOS Care Hub",
                   page_icon="🩺",
                   layout="wide",
                   initial_sidebar_state="collapsed")

# ---------- page-wide style ----------
st.markdown("""
<style>
:root{ --primary:#1565C0; --accent:#43A047; }
html, body {font-family:'Inter',sans-serif;}
h1, h2, h3 {color:var(--primary);}
.hero-btn{
  background:var(--primary); color:#fff; padding:0.8rem 2.2rem;
  border:none; border-radius:6px; font-size:1.15rem;
}
.hero-btn:hover{background:#104d99;}
.tiny{ text-transform:uppercase; letter-spacing:0.1rem; font-size:0.7rem; color:grey; }
.card{ border:1px solid #eee; border-radius:8px; padding:1rem; text-align:center; }
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
daily_df      = store.read_daily(email)
days_done     = len(daily_df) if daily_df is not None else 0

st.markdown("#### Today’s status")
c1, c2, c3 = st.columns(3)
c1.metric("Profile", "Set" if profile_ready else "Missing",
          delta="✓" if profile_ready else "●")
c2.metric("Days logged", f"{days_done}/30",
          delta=None if days_done==0 else f"+{days_done}")
c3.metric("Date", date.today().strftime("%b %d, %Y"))

# ---------- navigation cards ----------
# ----- navigation cards -------------------------------------------------
st.divider()
st.markdown("#### Navigate")

card_defs = [
    ("👤 Profile",   "pages/Profile.py",          "One-time medical details"),
    ("📝 Daily Log", "pages/Daily_log.py",        "Enter today’s symptoms"),
    ("📊 View Cycle","pages/view_cycle.py",       "See progress & risk"),
    ("💪 Exercise",  "pages/exercise_recipie.py", "Workout suggestions"),
    # ("🥗 Diet",    "pages/Diet_Module.py",      "Nutrition guidance"),
    ("⚙️ Settings",  "pages/settings.py",        "Reset or export data"),
]

cols = st.columns(3)
for i, (label, target, subtitle) in enumerate(card_defs):
    with cols[i % 3]:
        # 1️⃣ draw the surrounding “card” box
        st.markdown(
            f"""
            <div class="card">
              <b>{label}</b><br>
              <span class="tiny">{subtitle}</span><br><br>
            """,
            unsafe_allow_html=True,
        )

        # 2️⃣ clean page_link call – NO unsafe_allow_html here
        st.page_link(
            target,
            label="Open",
            icon="➡️",
            use_container_width=True
        )

        # 3️⃣ close the <div>
        st.markdown("</div>", unsafe_allow_html=True)

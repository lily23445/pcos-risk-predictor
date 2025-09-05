import streamlit as st

st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

# ── Unauthenticated view ────────────────────────────────────────
if not st.user.is_logged_in:
    st.markdown(
        """
        <style>
        body            {background:#FFF5F5;}
        .container      {background:linear-gradient(135deg,#E91E63,#A84646);
                         padding:3rem 2rem;border-radius:16px;
                         max-width:380px;margin:6rem auto;text-align:center;
                         box-shadow:0 8px 24px rgba(0,0,0,.12);color:#fff;}
        h1              {font-size:2.5rem;margin:0 0 .3rem;font-weight:700;}
        h2              {font-size:1.1rem;font-weight:400;color:#F8BBD0;margin:0 0 1.8rem;}
        button[kind="primary"]{border-radius:50px;font-size:1.1rem;padding:.7rem 2.5rem;}
        .cta-card       {margin-top:1.5rem;padding:1rem 1.2rem;background:#B03060;
                         border-radius:10px;box-shadow:0 3px 10px rgba(0,0,0,0.2);
                         font-weight:600;color:#fff;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="container">
            <div style="font-size:4rem;margin-bottom:.8rem;">🩺</div>
            <h1>PCOS Tracker</h1>
            <h2>Sign in with Google to continue</h2>

           
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.button("Sign in with Google", type="primary",
              on_click=lambda: st.login("google"))
    st.stop()                       # pause until Google redirects back

# ── OAuth finished -> persist e-mail & go to Home ───────────────
if "email" not in st.session_state:
    st.session_state["email"] = st.user.email

st.switch_page("pages/homepage.py")   # ← automatic redirect

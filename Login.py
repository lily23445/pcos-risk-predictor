import streamlit as st

# ---------- page config ----------
st.set_page_config(page_title="Login", page_icon="🔐", layout="centered")

# ---------- custom CSS for pizzazz ----------
st.markdown("""
<style>
body            {background:#FFF5F5;}
.container      {background:linear-gradient(135deg,#E91E63,#A84646);
                 padding:3rem 2rem;border-radius:16px;
                 max-width:380px;margin:6rem auto;text-align:center;
                 box-shadow:0 8px 24px rgba(0,0,0,.12);color:#fff;}
h1              {font-size:2.5rem;margin:0 0 .3rem;font-weight:700;}
h2              {font-size:1.1rem;font-weight:400;color:#F8BBD0;margin:0 0 1.8rem;}
button[kind="primary"]{border-radius:50px;font-size:1.1rem;padding:.7rem 2.5rem;}
</style>
""", unsafe_allow_html=True)

# ---------- unauthenticated view ----------
if not st.user.is_logged_in:
    st.markdown("""
    <div class="container">
        <div style="font-size:4rem;margin-bottom:.8rem;">🩺</div>
        <h1>PCOS Tracker</h1>
        <h2>Sign in with Google to continue</h2>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Login with Google"):
        st.login("google")              # native OAuth call
    st.stop()                           # wait for redirect
# authenticated view
st.balloons()
st.success(f"Welcome back, {st.user}!")

st.switch_page("pages/homepage.py")

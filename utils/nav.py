import streamlit as st

def render_menu():
    """Draw sidebar links; skip Login after the user authenticates."""
    with st.sidebar:
        if st.user.is_logged_in:
            st.page_link("pages/homepage.py",   label="🏠 Dashboard")
            st.page_link("pages/Profile.py", label="👤 Profile")
            st.page_link("pages/Daily_log.py", label="📝 Daily Log")
            st.page_link("pages/view_cycle.py", label="📊 View Cycle")
            st.page_link("pages/exercise_recipie.py", label="🍽️  Exercise Recipie")
            st.page_link("pages/settings.py", label="⚙️ Setting")
            st.sidebar.markdown("---")
            if st.button("🚪 Log out", use_container_width=True):
                st.logout()
                st.switch_page("Login.py")
        else:
            st.page_link("Login.py", label="🔐 Sign in")


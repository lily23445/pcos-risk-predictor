import streamlit as st
import utils.nav as nav
nav.render_menu()

if not st.user.is_logged_in:
    st.switch_page("../Login.py")
st.title("💪 Exercise Recommendations")
st.info("Algorithm coming soon. For now, try 30 min moderate cardio + strength training 3×/week.")

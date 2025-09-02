import streamlit as st, utils.storage as store
import utils.nav as nav
nav.render_menu()
email = st.user.email
if not st.user.is_logged_in:
    st.switch_page("Login.py")
st.title("⚙️ Settings")

if st.button("Delete all stored data"):
    store.reset_user(email)
    st.success("Everything wiped. Refresh the page.")

     # 2️⃣ land on login screen

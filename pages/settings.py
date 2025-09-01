import streamlit as st, utils.storage as store

email = st.user.email
if not st.user.is_logged_in:
    st.switch_page("Login.py")
st.title("⚙️ Settings")

if st.button("Delete all stored data"):
    store.reset_user(email)
    st.success("Everything wiped. Refresh the page.")

if st.user.is_logged_in:                       # show only to signed-in users
    with st.sidebar:                           # or use 'main' for body area
        if st.button("🚪 Log out", use_container_width=True):
            st.logout()                        # 1️⃣ clear identity cookie
            st.switch_page("Login.py")         # 2️⃣ land on login screen

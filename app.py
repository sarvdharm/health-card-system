import streamlit as st
import database
import auth_system
import user_dashboard

database.init_db()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.page = "home"

# Green Top Banner (Image 1000102888)
st.markdown("<h1 style='text-align:center; background:#0c352f; color:white; padding:15px;'>Sarv Dharm Smanya Kalyan Samiti</h1>", unsafe_allow_html=True)

# Navigation
cols = st.columns(5)
if cols[0].button("🏠 Home"): st.session_state.page = "home"
if cols[3].button("👥 Login"): st.session_state.page = "login"
if cols[4].button("📊 Dashboard"): st.session_state.page = "dashboard"

if st.session_state.page == "login":
    auth_system.login()
elif st.session_state.page == "dashboard":
    if st.session_state.logged_in:
        user_dashboard.show_dashboard()
    else:
        st.warning("Please login first.")
elif st.session_state.page == "home":
    st.image("https://img.freepik.com/free-vector/medical-care-concept-landing-page_52683-20202.jpg")

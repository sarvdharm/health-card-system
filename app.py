import streamlit as st
import database
import auth_system
import main_controller # Naya controller import kiya

database.init_db()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.page = "home"

# Green Top Banner (Image 1000102888 jaisa)
st.markdown("<h1 style='text-align:center; background:#0c352f; color:white; padding:15px; border-radius:10px;'>Sarv Dharm Smanya Kalyan Samiti</h1>", unsafe_allow_html=True)

# Agar login nahi hai, toh Home ya Login page dikhao
if not st.session_state.logged_in:
    cols = st.columns(5)
    if cols[0].button("🏠 Home"): st.session_state.page = "home"
    if cols[4].button("👥 Login"): st.session_state.page = "login"

    if st.session_state.page == "login":
        auth_system.login()
    else:
        st.image("https://img.freepik.com/free-vector/medical-care-concept-landing-page_52683-20202.jpg")
        st.write("### NGO Mission: Swasthya aur Seva")

# AGAR LOGIN HAI, TOH CONTROLLER KO BULAO (Jo Role check karke sahi pannel dikhayega)
else:
    main_controller.route_user()

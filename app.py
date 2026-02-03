import streamlit as st
import database, ui_design, auth_system, admin_panel

# Start Database
database.init_db()
ui_design.load_styles()
ui_design.show_banner()

# Main Menu
menu = st.columns(4)
if menu[0].button("🏠 Home"): st.session_state.page = "home"
if menu[1].button("👥 Login/Register"): st.session_state.page = "login"
if menu[2].button("👑 Admin"): st.session_state.page = "admin"
if menu[3].button("💳 Health Card"): st.session_state.page = "card"

# Page Logic
page = st.session_state.get("page", "home")

if page == "login":
    auth_system.registration()
elif page == "admin":
    admin_panel.manage_approvals()
elif page == "home":
    st.image("https://img.freepik.com/free-vector/medical-care-concept-landing-page_52683-20202.jpg")

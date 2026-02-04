import streamlit as st
import admin_panel, user_dashboard, create_card, database

def route_user():
    st.sidebar.title(f"Welcome, {st.session_state.user_name}")
    role = st.session_state.user_role
    
    menu = ["Dashboard"]
    if role == "admin": menu += ["Manage Staff"]
    if role == "panchayat": menu += ["Create Card"]
    
    choice = st.sidebar.radio("Navigation", menu)
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if choice == "Dashboard": user_dashboard.show_dashboard()
    elif choice == "Manage Staff": admin_panel.show_admin_controls()
    elif choice == "Create Card": create_card.show_form()

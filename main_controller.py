import streamlit as st
import admin_panel
import user_dashboard
import create_card

def route_user():
    role = st.session_state.user_role
    
    st.sidebar.markdown(f"### Welcome, {st.session_state.user_name}")
    st.sidebar.write(f"Role: {role.upper()}")
    
    if role == "admin":
        menu = ["Dashboard", "Manage Staff", "View Cards"]
    elif role == "block":
        menu = ["Dashboard", "Verify Cards"]
    else:
        menu = ["Dashboard", "Create New Card"]
        
    choice = st.sidebar.radio("Main Menu", menu)
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # Routing Logic
    if choice == "Dashboard":
        user_dashboard.show_dashboard()
    elif choice == "Manage Staff":
        admin_panel.show_admin_controls()
    elif choice == "Create New Card":
        create_card.show_form()
    elif choice == "Verify Cards" or choice == "View Cards":
        user_dashboard.show_dashboard()

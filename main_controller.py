import streamlit as st
import admin_panel
import user_dashboard
import create_card # Nayi file import kari
import database

def route_user():
    role = st.session_state.user_role
    
    # Sidebar Logo
    st.sidebar.image(database.LOGO_URL, width=100)
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if role == "admin":
        st.sidebar.title("👑 Admin Menu")
        choice = st.sidebar.radio("Navigation", ["Dashboard", "Manage Staff", "View All Cards"])
        
        if choice == "Dashboard":
            user_dashboard.show_dashboard()
        elif choice == "Manage Staff":
            admin_panel.show_admin_controls()
        elif choice == "View All Cards":
            user_dashboard.show_dashboard()

    else:
        st.sidebar.title("👥 Coordinator Menu")
        # Panchayat ko 'Create Card' dikhega, Block ko sirf 'Dashboard'
        menu_options = ["My Dashboard", "Profile"]
        if role == "panchayat":
            menu_options.insert(1, "➕ Create New Card")
            
        choice = st.sidebar.radio("Navigation", menu_options)
        
        if choice == "My Dashboard":
            user_dashboard.show_dashboard()
        elif choice == "➕ Create New Card":
            create_card.show_form()
        elif choice == "Profile":
            st.write(f"Logged in as: {st.session_state.user_name}")

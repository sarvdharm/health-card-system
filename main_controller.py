import streamlit as st
import admin_panel
import user_dashboard

def route_user():
    role = st.session_state.user_role
    
    # Sidebar mein Logout button common rahega
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    if role == "admin":
        st.sidebar.title("👑 Admin Menu")
        choice = st.sidebar.radio("Go to", ["Admin Dashboard", "User View", "Manage Staff"])
        
        if choice == "Admin Dashboard":
            st.title("Admin Master Console")
            # Admin ke liye specific overview yahan aayega
            user_dashboard.show_dashboard() 
        elif choice == "Manage Staff":
            admin_panel.show_admin_controls()
        elif choice == "User View":
            user_dashboard.show_dashboard()

    else:
        # STAFF / COORDINATOR PANNEL
        st.sidebar.title("👥 Staff Menu")
        choice = st.sidebar.radio("Go to", ["My Dashboard", "Create New Card", "Profile"])
        
        if choice == "My Dashboard":
            user_dashboard.show_dashboard()
        elif choice == "Create New Card":
            st.info("Registration Form Coming Soon...")
        elif choice == "Profile":
            st.write(f"Name: {st.session_state.user_name}")
            st.write(f"Role: {st.session_state.user_role.upper()}")

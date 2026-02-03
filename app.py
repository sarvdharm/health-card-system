import streamlit as st
import database
import auth_system
import user_dashboard
import admin_panel # Nayi file import karein

database.init_db()

# ... (baaki purana navigation code waisa hi rahega) ...

elif st.session_state.page == "dashboard":
    if st.session_state.logged_in:
        # User details display
        st.sidebar.success(f"Logged in: {st.session_state.user_name}")
        
        # AGAR ADMIN HAI TOH ADMIN PANEL BHI DIKHAYE
        if st.session_state.user_role == "admin":
            admin_panel.show_admin_controls()
            st.divider()
        
        # Saare users (including Admin) apna dashboard dekh sakte hain
        user_dashboard.show_dashboard()
    else:
        st.warning("Please login first.")

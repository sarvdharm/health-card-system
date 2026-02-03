import streamlit as st
import user_dashboard # Nayi file ko import karein

# ... (Purana Login Code yahan rahega) ...

if st.session_state.logged_in:
    # Navigation Sidebar
    st.sidebar.title("NGO Menu")
    if st.sidebar.button("📊 Dashboard"): st.session_state.page = "dashboard"
    if st.sidebar.button("🔑 Change Password"): st.session_state.page = "change_password"
    if st.sidebar.button("🚪 Logout"): 
        st.session_state.logged_in = False
        st.rerun()

    # Page Routing
    if st.session_state.page == "dashboard":
        user_dashboard.show_dashboard()
    elif st.session_state.page == "change_password":
        st.write("Password Change Form Here")

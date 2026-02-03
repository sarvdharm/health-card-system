import streamlit as st
import pandas as pd
import os

# Page Config
st.set_page_config(page_title="SDSKS Portal", layout="wide")

# Database Files (CSV acting as SQL tables)
USER_DB = "users_registry.csv"
CARD_DB = "health_cards.csv"

# Initialize Files if they don't exist
for db, cols in [(USER_DB, ['UserID', 'Name', 'Pass', 'Role', 'ParentID']), 
                 (CARD_DB, ['id', 'card_no', 'head_name', 'panchayat', 'created_by', 'status'])]:
    if not os.path.exists(db):
        pd.DataFrame(columns=cols).to_csv(db, index=False)

# Session State Initialization (Like PHP session_start)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.page = "home"

# --- NAVIGATION BAR ---
cols = st.columns(6)
if cols[0].button("🏠 Home"): st.session_state.page = "home"
if cols[4].button("👥 Login Portal"): st.session_state.page = "login"
if cols[5].button("💳 Health Card"): st.session_state.page = "dashboard"

# --- PAGE ROUTING ---
if st.session_state.page == "login":
    if not st.session_state.logged_in:
        st.subheader("🔐 Multi-Level Login")
        uid = st.text_input("UserID")
        upw = st.text_input("Password", type="password")
        if st.button("Login"):
            if uid == "admin" and upw == "ngo786":
                st.session_state.update({"logged_in": True, "user_role": "admin", "user_name": "Chief Admin", "user_id": "0"})
                st.rerun()
            else:
                df = pd.read_csv(USER_DB)
                user = df[(df['UserID'].astype(str) == uid) & (df['Pass'].astype(str) == upw)]
                if not user.empty:
                    st.session_state.update({"logged_in": True, "user_id": uid, "user_role": user.iloc[0]['Role'].lower(), "user_name": user.iloc[0]['Name']})
                    st.rerun()
                else: st.error("Invalid Credentials")
    else:
        st.success(f"Welcome {st.session_state.user_name}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

elif st.session_state.page == "dashboard":
    if st.session_state.logged_in:
        import user_dashboard
        user_dashboard.show_dashboard()
    else:
        st.warning("Please login first.")

elif st.session_state.page == "home":
    st.image("https://img.freepik.com/free-vector/medical-care-concept-landing-page_52683-20202.jpg")

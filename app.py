import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- CONFIG & DATABASE ---
st.set_page_config(page_title="SDSKS Management System", layout="wide")

USER_DB = "users_registry.csv"
CARD_DB = "health_cards.csv"

def init_db():
    if not os.path.exists(USER_DB):
        pd.DataFrame(columns=['UserID', 'Name', 'Pass', 'Role', 'ParentID', 'Area']).to_csv(USER_DB, index=False)
    if not os.path.exists(CARD_DB):
        pd.DataFrame(columns=['Date', 'Head', 'Aadhar', 'Panchayat', 'CreatedBy']).to_csv(CARD_DB, index=False)

init_db()

# --- UI DESIGN (Image 33 & 1000102888 Style) ---
st.markdown("""
    <style>
    .main-header { background-color: #0c352f; color: white; padding: 20px; text-align: center; border-radius: 10px; }
    .stButton>button { background-color: #1a7b8c; color: white; border-radius: 8px; width: 100%; font-weight: bold; height: 45px; }
    .role-badge { background-color: #e1f5fe; color: #01579b; padding: 5px 10px; border-radius: 15px; font-weight: bold; }
    </style>
    <div class="main-header">
        <h1>Sarv Dharm Smanya Kalyan Samiti</h1>
        <p>सेवा, स्वास्थ्य और समानता - हर व्यक्ति का अधिकार</p>
    </div>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
cols = st.columns(6)
if cols[0].button("🏠 Home"): st.session_state.page = "home"
if cols[1].button("👨‍⚕️ Doctors"): st.session_state.page = "doctors"
if cols[2].button("📄 Documents"): st.session_state.page = "docs"
if cols[3].button("🔬 Labs"): st.session_state.page = "labs"
if cols[4].button("👥 Login Portal"): st.session_state.page = "login"
if cols[5].button("💳 Health Card"): st.session_state.page = "card"

if "page" not in st.session_state: st.session_state.page = "home"
if "logged_in" not in st.session_state: st.session_state.logged_in = False

# --- LOGIC SECTIONS ---

# 1. LOGIN PORTAL (District, Block, Panchayat Sab ke liye)
if st.session_state.page == "login":
    if not st.session_state.logged_in:
        st.subheader("🔐 Multi-Level Coordinator Login")
        u_id = st.text_input("UserID (Mobile Number)")
        u_pw = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if u_id == "admin" and u_pw == "ngo786":
                st.session_state.update({"logged_in": True, "user_role": "Admin", "user_name": "Chief Admin"})
                st.rerun()
            else:
                df = pd.read_csv(USER_DB)
                user = df[(df['UserID'].astype(str) == u_id) & (df['Pass'].astype(str) == u_pw)]
                if not user.empty:
                    st.session_state.update({
                        "logged_in": True, "user_id": u_id, 
                        "user_role": user.iloc[0]['Role'], "user_name": user.iloc[0]['Name']
                    })
                    st.rerun()
                else: st.error("Galt Credentials! Admin se apni ID lein.")
    else:
        # LOGGED IN DASHBOARD
        st.sidebar.markdown(f"### Welcome, {st.session_state.user_name}")
        st.sidebar.markdown(f"Role: <span class='role-badge'>{st.session_state.user_role}</span>", unsafe_allow_html=True)
        
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

        # ADMIN PANEL: To Create All Coordinators
        if st.session_state.user_role == "Admin":
            st.header("👑 Admin Master Control")
            with st.expander("➕ Create New Coordinator (District/Block/Panchayat)"):
                with st.form("create_user"):
                    c_name = st.text_input("Full Name")
                    c_phone = st.text_input("Mobile (UserID)")
                    c_pass = st.text_input("Password")
                    c_role = st.selectbox("Assign Role", ["District", "Block", "Panchayat"])
                    c_parent = st.text_input("Parent ID (e.g., Block Coord's Mobile for Panchayat Coord)")
                    c_area = st.text_input("Assigned Area (District/Block Name)")
                    if st.form_submit_button("Generate ID"):
                        df = pd.read_csv(USER_DB)
                        new_data = {"UserID": c_phone, "Name": c_name, "Pass": c_pass, "Role": c_role, "ParentID": c_parent, "Area": c_area}
                        pd.concat([df, pd.DataFrame([new_data])]).to_csv(USER_DB, index=False)
                        st.success(f"ID Created for {c_name} as {c_role}!")

        # HIERARCHY VIEW: Block Coordinator sees their Panchayat Team
        if st.session_state.user_role in ["District", "Block"]:
            st.header(f"📊 {st.session_state.user_role} Management Dashboard")
            df_all = pd.read_csv(USER_DB)
            my_team = df_all[df_all['ParentID'].astype(str) == str(st.session_state.user_id)]
            st.write("### Your Team Members")
            st.dataframe(my_team[['Name', 'UserID', 'Role', 'Area']])

# 2. HEALTH CARD (Only for Panchayat & Admin)
elif st.session_state.page == "card":
    if st.session_state.get("logged_in") and st.session_state.user_role in ["Panchayat", "Admin"]:
        st.header("💳 Health Card Generation")
        # Yahan card banane ka form aayega...
    else:
        st.warning("Kripya Panchayat Coordinator ID se login karein card banane ke liye.")

# 3. HOME (Website Look)
elif st.session_state.page == "home":
    st.image("https://img.freepik.com/free-vector/medical-care-concept-landing-page_52683-20202.jpg")
    st.write("### Swasthya Aur Seva, Har Ghar Tak")

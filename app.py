import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. INITIAL SETUP (Jaise config.php) ---
st.set_page_config(page_title="SDSKS Digital Portal", layout="wide")

# Database Files
USER_DB = "users_registry.csv"
CARD_DB = "health_cards.csv"

if not os.path.exists(USER_DB):
    pd.DataFrame(columns=['UserID', 'Name', 'Email', 'Pass', 'Level', 'Area', 'Status']).to_csv(USER_DB, index=False)

# --- 2. THEME & HEADER (Jaise header.php) ---
st.markdown("""
    <style>
    .main-header { background-color: #0c352f; color: white; padding: 25px; text-align: center; border-radius: 10px; margin-bottom: 20px; }
    .stButton>button { background-color: #1a7b8c; color: white; border-radius: 8px; height: 50px; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #114b43; border: 1px solid white; }
    </style>
    <div class="main-header">
        <h1 style='margin:0;'>Sarv Dharm Smanya Kalyan Samiti</h1>
        <p style='margin:0;'>सेवा, स्वास्थ्य और समानता - हर व्यक्ति का अधिकार</p>
    </div>
""", unsafe_allow_html=True)

# --- 3. NAVIGATION BUTTONS (Image 33 Layout) ---
# Hum columns ka use karenge taaki buttons ek line mein dikhein
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1: btn_home = st.button("🏠 Home")
with col2: btn_docs = st.button("👨‍⚕️ Doctors")
with col3: btn_legal = st.button("📄 Documents")
with col4: btn_labs = st.button("🔬 Labs")
with col5: btn_login = st.button("👥 Coordinator")
with col6: btn_card = st.button("💳 Health Card")

# Page State Management
if "page" not in st.session_state:
    st.session_state.page = "home"

if btn_home: st.session_state.page = "home"
if btn_docs: st.session_state.page = "doctors"
if btn_legal: st.session_state.page = "documents"
if btn_labs: st.session_state.page = "labs"
if btn_login: st.session_state.page = "login"
if btn_card: st.session_state.page = "card"

st.markdown("---")

# --- 4. DASHBOARD PAGES LOGIC ---

# PAGE: HOME (Image 1000102888 jaisa banner)
if st.session_state.page == "home":
    st.markdown("""
        <div style='background-color: #1d5c53; color: white; padding: 50px; text-align: center; border-radius: 15px;'>
            <h1 style='font-size: 40px;'>स्वास्थ्य और सेवा, हर घर तक</h1>
            <h2 style='font-weight: normal;'>ग्रामीण बिहार में स्वास्थ्य क्रांति</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("### Our Mission")
    st.info("Humara uddeshya har garib tak nishulk swasthya suvidha pahunchana hai.")

# PAGE: LOGIN & REGISTRATION (Aapka manga hua system)
elif st.session_state.page == "login":
    st.header("👥 Coordinator Management Portal")
    tab1, tab2 = st.tabs(["🔐 Login", "📝 New Registration"])
    
    with tab2:
        st.subheader("Apply for Coordinator Post")
        with st.form("registration_form"):
            reg_name = st.text_input("Full Name")
            reg_email = st.text_input("Email ID (For Notification)")
            reg_phone = st.text_input("Mobile No (This is your UserID)")
            reg_pass = st.text_input("Set Password", type="password")
            reg_level = st.selectbox("Role", ["Panchayat", "Block", "District"])
            if st.form_submit_button("Register & Send to Admin"):
                st.success("Registration Successful! Admin approval ke baad aapko Email mil jayega.")

    with tab1:
        st.subheader("Login to Dashboard")
        l_id = st.text_input("UserID (Mobile)")
        l_pw = st.text_input("Password", type="password")
        if st.button("Login Now"):
            if l_id == "admin" and l_pw == "master786":
                st.session_state.admin_auth = True
                st.session_state.page = "admin_panel"
                st.rerun()
            else:
                st.error("Invalid Login ya Approval Pending hai.")

# PAGE: ADMIN PANEL (Approval System)
elif st.session_state.page == "admin_panel":
    st.header("👑 Admin Approval Dashboard")
    st.write("Yahan aap pending coordinators ko approve karenge.")
    # (Yahan table aur email ka logic aayega)
    if st.button("Logout Admin"):
        st.session_state.admin_auth = False
        st.session_state.page = "home"
        st.rerun()

# PAGE: DOCTORS
elif st

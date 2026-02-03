import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. CONFIG & DATABASE ---
st.set_page_config(page_title="SDSKS Management System", layout="wide")

USER_DB = "users_registry.csv"
CARD_DB = "health_cards.csv"

# Database initialize karna (XAMPP config jaisa)
def init_db():
    if not os.path.exists(USER_DB):
        pd.DataFrame(columns=['UserID', 'Name', 'Pass', 'Role', 'ParentID', 'Status']).to_csv(USER_DB, index=False)
    if not os.path.exists(CARD_DB):
        pd.DataFrame(columns=['Date', 'Head', 'Aadhar', 'Panchayat', 'CreatedBy']).to_csv(CARD_DB, index=False)

init_db()

# --- 2. UI DESIGN (Image 33 jaisa professional look) ---
st.markdown("""
    <style>
    .main-header { background-color: #0c352f; color: white; padding: 20px; text-align: center; border-radius: 10px; }
    .stButton>button { background-color: #1a7b8c; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    .card-box { border: 1px solid #ddd; padding: 15px; border-radius: 10px; background-color: #f9f9f9; }
    </style>
    <div class="main-header">
        <h1>Sarv Dharm Smanya Kalyan Samiti</h1>
        <p>स्वास्थ्य और सेवा, हर घर तक - ग्रामीण बिहार में स्वास्थ्य क्रांति</p>
    </div>
""", unsafe_allow_html=True)

# --- 3. NAVIGATION ---
cols = st.columns(6)
btn_home = cols[0].button("🏠 Home")
btn_docs = cols[1].button("👨‍⚕️ Doctors")
btn_legal = cols[2].button("📄 Documents")
btn_labs = cols[3].button("🔬 Labs")
btn_login = cols[4].button("👥 Staff Login")
btn_card = cols[5].button("💳 Health Card")

if "page" not in st.session_state: st.session_state.page = "home"
if "logged_in" not in st.session_state: st.session_state.logged_in = False

if btn_home: st.session_state.page = "home"
if btn_login: st.session_state.page = "login"
if btn_card: st.session_state.page = "card"

st.write("---")

# --- 4. LOGIC SECTIONS ---

# PAGE: HOME
if st.session_state.page == "home":
    st.image("https://img.freepik.com/free-vector/medical-care-concept-landing-page_52683-20202.jpg", use_container_width=True)
    st.write("### Humari Team (Image 1000102887 jaisa)")
    c1, c2, c3 = st.columns(3)
    c1.info("*President*: Shailesh Kumar")
    c2.info("*Secretary*: Surendra Jha Suman")
    c3.info("*Treasurer*: Satish Kumar")

# PAGE: LOGIN & DASHBOARD
elif st.session_state.page == "login":
    if not st.session_state.logged_in:
        st.subheader("🔐 Staff Login")
        u_id = st.text_input("UserID (Mobile)")
        u_pw = st.text_input("Password", type="password")
        
        if st.button("Login"):
            # Admin Login
            if u_id == "admin" and u_pw == "ngo786":
                st.session_state.logged_in = True
                st.session_state.user_role = "Admin"
                st.rerun()
            # Coordinator Login
            else:
                df = pd.read_csv(USER_DB)
                user = df[(df['UserID'].astype(str) == u_id) & (df['Pass'].astype(str) == u_pw)]
                if not user.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_id = u_id
                    st.session_state.user_role = user.iloc[0]['Role']
                    st.session_state.user_name

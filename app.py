import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ==========================================
# 1. DATABASE LOGIC (Jaise config.php)
# ==========================================
USER_DB = "users_registry.csv"

def init_db():
    if not os.path.exists(USER_DB):
        df = pd.DataFrame(columns=['UserID', 'Name', 'Email', 'Pass', 'Level', 'Status'])
        df.to_csv(USER_DB, index=False)

# ==========================================
# 2. UI DESIGN (Jaise style.css/header.php)
# ==========================================
def load_ui():
    st.markdown("""
        <style>
        .main-header { background-color: #0c352f; color: white; padding: 20px; text-align: center; border-radius: 10px; }
        .nav-btn { background-color: #1a7b8c; color: white; border-radius: 5px; padding: 10px; }
        </style>
        <div class="main-header"><h1>Sarv Dharm Smanya Kalyan Samiti</h1></div>
    """, unsafe_allow_html=True)

# ==========================================
# 3. MAIN APP (Jaise index.php)
# ==========================================
init_db()
load_ui()

# Navigation Tabs (Image 33 Layout)
menu = st.tabs(["🏠 Home", "👥 Coordinator Registration", "🔐 Staff Login", "👑 Admin"])

with menu[0]:
    st.write("### Swasthya Aur Seva, Har Ghar Tak")
    st.image("https://img.freepik.com/free-vector/medical-care-concept-landing-page_52683-20202.jpg")

with menu[1]:
    st.subheader("New Coordinator Registration")
    with st.form("reg"):
        n = st.text_input("Full Name")
        e = st.text_input("Email")
        p = st.text_input("Mobile (UserID)")
        pw = st.text_input("Password", type="password")
        lvl = st.selectbox("Role", ["Panchayat", "Block", "District"])
        if st.form_submit_button("Register Now"):
            # Yahan data save karne ka logic
            st.success("Registration Sent! Admin approval ka intezar karein.")

with menu[2]:
    st.subheader("Staff Login")
    user = st.text_input("Mobile No")
    pas = st.text_input("Password ", type="password")
    if st.button("Login"):
        st.info("Verification in progress...")

with menu[3]:
    st.subheader("Admin Master Control")
    master = st.text_input("Master Password", type="password")
    if master == "NGO@786":
        st.success("Access Granted. Showing Pending Approvals...")

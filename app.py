import streamlit as st
import pandas as pd
import os

# 1. Page Config & CSS (Website Look)
st.set_page_config(page_title="SDSKS Digital Portal", layout="wide")

st.markdown("""
    <style>
    .main-header { background-color: #0c352f; color: white; padding: 20px; text-align: center; border-radius: 10px; }
    .nav-btn { background-color: #1a7b8c; color: white; border-radius: 5px; text-align: center; padding: 10px; cursor: pointer; }
    .footer { background-color: #0c352f; color: white; padding: 20px; text-align: center; margin-top: 50px; }
    </style>
    <div class="main-header">
        <h1>Sarv Dharm Smanya Kalyan Samiti</h1>
        <p>सेवा, स्वास्थ्य और समानता - हर व्यक्ति का अधिकार</p>
    </div>
""", unsafe_allow_html=True)

# 2. Database Initialization
USER_DB = "users.csv"
if not os.path.exists(USER_DB):
    pd.DataFrame(columns=['Name', 'Email', 'Mobile', 'Role', 'Status']).to_csv(USER_DB, index=False)

# 3. Navigation Menu (Image 33 jaisa)
st.write("---")
cols = st.columns(6)
b_home = cols[0].button("🏠 Home")
b_docs = cols[1].button("👨‍⚕️ Doctors")
b_legal = cols[2].button("📄 Documents")
b_labs = cols[3].button("🔬 Labs")
b_login = cols[4].button("👥 Staff Login")
b_card = cols[5].button("💳 Health Card")

# Page State
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if b_home: st.session_state.page = 'home'
if b_docs: st.session_state.page = 'doctors'
if b_legal: st.session_state.page = 'legal'
if b_labs: st.session_state.page = 'labs'
if b_login: st.session_state.page = 'login'
if b_card: st.session_state.page = 'card'

# 4. Dashboard Content Sections
if st.session_state.page == 'home':
    st.markdown("""
        <div style='background-color: #1d5c53; color: white; padding: 40px; text-align: center; border-radius: 15px;'>
            <h1 style='font-size: 35px;'>स्वास्थ्य और सेवा, हर घर तक - ग्रामीण बिहार में स्वास्थ्य क्रांति</h1>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: st.info("🚑 *नि:शुल्क मेडिकल कैंप*")
    with c2: st.success("❤️ *स्वास्थ्य जागरूकता*")
    with c3: st.warning("🤝 *रिफरल सहायता*")

elif st.session_state.page == 'login':
    st.subheader("👥 Coordinator & Staff Portal")
    t1, t2 = st.tabs(["Login", "Registration"])
    
    with t2:
        with st.form("reg_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email ID")
            mob = st.text_input("Mobile No")
            role = st.selectbox("Role", ["Panchayat", "Block", "District"])
            if st.form_submit_button("Submit Application"):
                st.success("Application submitted! Admin approval pending.")
    
    with t1:
        u = st.text_input("UserID")
        p = st.text_input("Password", type="password")
        if st.button("Enter Dashboard"):
            if u == "admin" and p == "master786":
                st.session_state.is_admin = True
                st.success("Welcome Admin!")
            else:
                st.error("Invalid Credentials or Not Approved.")

elif st.session_state.page == 'card':
    st.header("💳 Family Health Card")
    st.warning("Kripya pehle Staff Login karein taaki aap card bana saken.")

# 5. Footer (Image 1000102887 jaisa)
st.markdown("""
    <div class="footer">
        <p>Registration No.: S000338/2021/2022 | Contact: secretary@sdsks.org</p>
    </div>
""", unsafe_allow_html=True)

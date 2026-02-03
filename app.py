import streamlit as st
import pandas as pd
from PIL import Image
import qrcode
import io
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="SDSKS Digital Portal", layout="wide")

# --- CUSTOM CSS (Aapki Website Jaisa Dikhne ke liye) ---
st.markdown("""
    <style>
    /* Green Header Background */
    .stApp { background-color: #f8f9fa; }
    header { background-color: #114b43 !important; }
    
    /* Navigation Bar Style */
    .nav-container {
        background-color: #114b43;
        padding: 10px;
        border-radius: 0px 0px 15px 15px;
        display: flex;
        justify-content: center;
        gap: 15px;
    }
    
    /* Card/Box Styling */
    .feature-box {
        background-color: #1d5c53;
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* Main Banner Area */
    .banner-text {
        background-color: #1d5c53;
        color: white;
        padding: 40px;
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE SETUP ---
DB_FILE = "sdsks_master.csv"

# --- TOP HEADER (Image 30 Jaisa) ---
st.markdown("""
    <div style='background-color: #0c352f; padding: 15px; text-align: left; color: white; display: flex; align-items: center;'>
        <img src='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR6A5N_HId_tW_DIsO_7o-xN4Xk8x6S0y5_iA&s' width='50' style='margin-right: 20px;'>
        <div>
            <h2 style='margin:0;'>Sarv Dharm Smanya Kalyan Samiti</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- NAVIGATION BUTTONS (Image 30 Jaisa Layout) ---
col_nav = st.columns(7)
home_btn = col_nav[0].button("🏠 Home")
doc_btn = col_nav[1].button("👨‍⚕️ Doctors")
file_btn = col_nav[2].button("📄 Documents")
lab_btn = col_nav[3].button("🔬 Labs")
emp_btn = col_nav[4].button("👥 Employer")
card_btn = col_nav[5].button("💳 Health Card")

st.markdown("---")

# --- MAIN CONTENT AREA ---

# 1. HOME SECTION (Image 30 Ki Tarah Large Text Banner)
if home_btn or (not any([doc_btn, file_btn, lab_btn, emp_btn, card_btn])):
    st.markdown("""
        <div class='banner-text'>
            स्वास्थ्य और सेवा, हर घर तक - ग्रामीण बिहार में <br> स्वास्थ्य क्रांति
        </div>
        <p style='text-align:center; color: #555; padding: 10px;'>
            सेवा, स्वास्थ्य और समानता - हर व्यक्ति का अधिकार | Service, Health and Equality
        </p>
        """, unsafe_allow_html=True)
    
    # 3 Boxes like Image 30 bottom
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='feature-box'>🚑<br><h3>नि:शुल्क मेडिकल कैंप</h3><p>मासिक स्वास्थ्य जांच शिविर</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='feature-box'>❤️<br><h3>स्वास्थ्य जागरूकता</h3><p>पोषण और शिशु स्वास्थ्य</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='feature-box'>🤝<br><h3>रिफरल सहायता</h3><p>गंभीर मामलों के लिए अस्पताल समन्वय</p></div>", unsafe_allow_html=True)

# 2. HEALTH CARD SECTION (Asli Kaam Karne wala Button)
elif card_btn:
    st.title("💳 Family Health Card Generator")
    with st.container(border=True):
        st.write("### Beneficiary Details")
        c1, c2 = st.columns(2)
        h_name = c1.text_input("Head Name")
        f_name = c1.text_input("Father/Husband Name")
        adh = c2.text_input("Aadhar (Last 4)")
        coord = c2.text_input("Coordinator Name")
        
        if st.button("Generate & Save"):
            # Yahan data save karne ka logic
            st.success(f"{h_name} ka data save ho gaya hai!")
            # Card image display logic...

# 3. DOCTORS / STAFF SECTION
elif doc_btn or emp_btn:
    st.header("Our Professional Team")
    st.info("Management aur Doctors ki list yahan dekhein.")
    # Team members list...

# --- FOOTER (Image 32 Jaisa) ---
st.markdown("---")
f1, f2 = st.columns(2)
with f1:
    st.write("*Sarv Dharm Smanya Kalyan Samiti*")
    st.write("Registration No.: S000338/2021/2022")
with f2:
    st.write("*Contact:* secretary@sdsks.org")

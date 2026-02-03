import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw
import qrcode
import io
from datetime import datetime

# Page Settings
st.set_page_config(page_title="SDSKS Digital Portal", layout="wide")

# Database File
DB_FILE = "sdsks_master_data.csv"

# Function to save data
def save_entry(data):
    df = pd.DataFrame([data])
    df.to_csv(DB_FILE, mode='a', header=not pd.io.common.file_exists(DB_FILE), index=False)

# --- CSS FOR UI (Image 33 ke jaisa) ---
st.markdown("""
    <style>
    .nav-button { background-color: #f0f2f6; border-radius: 10px; padding: 10px; text-align: center; border: 1px solid #ddd; }
    .main-title { background-color: #0c352f; color: white; padding: 20px; text-align: center; border-radius: 5px; }
    .banner-box { background-color: #1a7b8c; color: white; padding: 30px; text-align: center; font-size: 24px; font-weight: bold; border-radius: 10px; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER & NAVIGATION ---
st.markdown('<div class="main-title"><h1>Sarv Dharm Smanya Kalyan Samiti</h1></div>', unsafe_allow_html=True)

# Buttons Row (Image 33 Layout)
col_nav = st.columns([1, 1.5, 1.2, 1.2, 1.5, 1.5])
btn_home = col_nav[0].button("🏠 Home")
btn_docs_h = col_nav[1].button("👨‍⚕️ Private Doctors")
btn_docum = col_nav[2].button("📄 Documents")
btn_labs = col_nav[3].button("🔬 Partner Labs")
btn_login = col_nav[4].button("👥 Staff Login")
btn_card = col_nav[5].button("💳 Download Card")

st.markdown("---")

# --- NAVIGATION LOGIC (Buttons Work) ---

# 1. HOME PAGE (Aapki Image 30 jaisa banner)
if btn_home or (not any([btn_docs_h, btn_docum, btn_labs, btn_login, btn_card])):
    st.markdown('<div class="banner-box">स्वास्थ्य और सेवा, हर घर तक - ग्रामीण बिहार में स्वास्थ्य क्रांति</div>', unsafe_allow_html=True)
    st.write("### Our Plan & Mission")
    st.info("Humara uddeshya gramin kshetro mein swasthya jagrukta aur nishulk medical camp pahunchana hai.")
    # Team display like Image 32
    c1, c2, c3 = st.columns(3)
    c1.metric("President", "Shailesh Kumar")
    c2.metric("Secretary", "Surendra Jha Suman")
    c3.metric("Treasurer", "Satish Kumar")

# 2. PRIVATE DOCTORS/HOSPITALS
elif btn_docs_h:
    st.header("👨‍⚕️ Registered Doctors & Hospitals")
    st.write("NGO se jude huye private doctors ki list yahan dekhein:")
    # Yahan aap doctors ki table daal sakte hain
    data = {"Doctor Name": ["Dr. A.K. Singh", "Dr. S.P. Verma"], "Specialization": ["Eye Specialist", "Child Specialist"], "City": ["Bettiah", "Motihari"]}
    st.table(data)

# 3. DOCUMENTS SECTION
elif btn_docum:
    st.header("📄 Important Documents")
    st.write("NGO Registration, 12A, 80G aur anya certificates yahan se download karein.")
    st.button("Download Registration Copy")

# 4. PARTNER LABS
elif btn_labs:
    st.header("🔬 Partner Diagnostic Labs")
    st.write("In labs par SDSKS card dikhane par 20% discount milega.")
    st.success("1. City Scan Center | 2. Janta Lab | 3. Bihar Pathology")

# 5. STAFF/COORDINATOR LOGIN (Management System)
elif btn_login:
    st.header("🔐 Staff Management Login")
    user_type = st.radio("Access Level", ["Panchayat", "Block", "District", "Admin"])
    pwd = st.text_input("Security Password", type="password")
    
    if pwd == "ngo123": # Master password (badal sakte hain)
        st.success(f"Access Granted to {user_type} Dashboard")
        try:
            df = pd.read_csv(DB_FILE)
            st.write("### Data Records")
            st.dataframe(df)
        except:
            st.warning("Database abhi khali hai.")

# 6. DOWNLOAD HEALTH CARD (Asli Kaam)
elif btn_card:
    st.header("💳 Generate Family Health Card")
    with st.form("card_form"):
        col1, col2 = st.columns(2)
        h_name = col1.text_input("Head of Family")
        f_name = col1.text_input("Father/Husband Name")
        adh_no = col2.text_input("Aadhar (Last 4)")
        p_name = col2.text_input("Panchayat")
        submit = st.form_submit_button("Save & Generate Card")
        
        if submit:
            if h_name and adh_no:
                # Save Data
                entry = {"Date": datetime.now(), "Head": h_name, "Father": f_name, "Aadhar": adh_no, "Panchayat": p_name}
                save_entry(entry)
                st.success(f"Data for {h_name} has been saved successfully!")
                
                # Simple Card Preview
                st.info("Aapka Digital Card taiyar hai. (Upar black & orange strip ke saath)")
                # (Yahan Image 27 wala design logic add kar sakte hain)
            else:
                st.error("Kripya poori jaankari bharein.")

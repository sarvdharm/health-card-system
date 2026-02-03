import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image, ImageDraw
import qrcode
import io

# --- PAGE CONFIG & THEME ---
st.set_page_config(page_title="SDSKS Digital Portal", layout="wide")

# Custom CSS for NGO Theme (Greenish UI)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { background-color: #114b43; color: white; border-radius: 5px; width: 100%; }
    .header-box { background-color: #114b43; padding: 20px; border-radius: 10px; color: white; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE LOGIC ---
DB_FILE = "sdsks_master_data.csv"
def save_data(data):
    df = pd.DataFrame([data])
    df.to_csv(DB_FILE, mode='a', header=not pd.io.common.file_exists(DB_FILE), index=False)

# --- SIDEBAR NAVIGATION (Role Based) ---
st.sidebar.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR6A5N_HId_tW_DIsO_7o-xN4Xk8x6S0y5_iA&s", width=100)
role = st.sidebar.selectbox("Login Role", ["Coordinator", "Block Head", "District Head", "Office/Admin"])

# --- TOP NAVIGATION BUTTONS (Working Menu) ---
st.markdown('<div class="header-box"><h1>सर्व धर्म समान कल्याण समिति</h1><p>Health and Equality - Everyone\'s Right</p></div>', unsafe_allow_html=True)
nav_col = st.columns(6)
b_home = nav_col[0].button("🏠 Home")
b_docs = nav_col[1].button("👨‍⚕️ Doctors")
b_file = nav_col[2].button("📄 Docs")
b_lab = nav_col[3].button("🔬 Labs")
b_card = nav_col[4].button("💳 Health Card")
b_staff = nav_col[5].button("👥 Staff")

# --- APP LOGIC BASED ON BUTTONS & ROLES ---

# 1. DOCTORS SECTION
if b_docs:
    st.subheader("Available Doctors & Medical Staff")
    st.info("Yahan aap apne NGO se jude doctors ki list aur unki availability dekh sakte hain.")
    st.table(pd.DataFrame({"Doctor Name": ["Dr. Sharma", "Dr. Verma"], "Specialty": ["General", "Child Spl"], "Status": ["Online", "Offline"]}))

# 2. LABS SECTION
elif b_lab:
    st.subheader("Partner Labs & Checkup Centers")
    st.write("Free checkup camps ki jankari yahan milegi.")

# 3. HEALTH CARD GENERATION (Main Work)
elif b_card or role == "Coordinator":
    st.subheader("💳 Digital Health Card System")
    with st.expander("Naya Card Banayein (Form)", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Beneficiary Name")
            fname = st.text_input("Father/Husband Name")
            aadhar = st.text_input("Aadhar (Last 4)")
        with col2:
            panchayat = st.text_input("Panchayat")
            block = st.text_input("Block")
            dist = st.text_input("District")
        
        if st.button("Save & Generate PDF Card"):
            if name and aadhar:
                # Save to Database
                entry = {"Date": datetime.now(), "Name": name, "Aadhar": aadhar, "Block": block, "Dist": dist, "Coordinator": role}
                save_data(entry)
                st.success(f"Record saved for {name}!")
                # Card Preview logic here...
            else:
                st.warning("Please fill details.")

# 4. ADMIN / STAFF VIEW (Managing the system)
elif role == "Office/Admin" or b_staff:
    st.subheader("📊 NGO Management Dashboard")
    pwd = st.text_input("Enter Admin Password", type="password")
    if pwd == "admin123":
        try:
            df = pd.read_csv(DB_FILE)
            st.metric("Total Cards Issued", len(df))
            
            tab1, tab2 = st.tabs(["Master Data", "Block-wise Report"])
            with tab1:
                st.dataframe(df)
            with tab2:
                st.bar_chart(df['Block'].value_counts())
        except:
            st.write("Abhi koi data nahi hai.")

# 5. HOME (Default Page)
else:
    st.image("https://img.freepik.com/free-vector/medical-video-call-consultation-with-doctor_23-2148520864.jpg", use_column_width=True)
    st.write("### Swasthya aur Seva, Har Ghar Tak")
    st.write("Is portal ke madhyam se aap digital health cards manage kar sakte hain.")

import streamlit as st
from PIL import Image, ImageDraw
import qrcode
import pandas as pd
from datetime import datetime
import io

# Page Config
st.set_page_config(page_title="SDSKS Health System", layout="wide")

DB_FILE = "sdsks_database.csv"

def save_to_db(data):
    df = pd.DataFrame([data])
    df.to_csv(DB_FILE, mode='a', header=not pd.io.common.file_exists(DB_FILE), index=False)

# --- SIDEBAR NAVIGATION ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2382/2382443.png", width=100)
st.sidebar.title("SDSKS Portal")
role = st.sidebar.radio("Login As:", ["Coordinator (User)", "NGO Head (Admin)"])

# --- COORDINATOR DASHBOARD ---
if role == "Coordinator (User)":
    st.title("📋 Coordinator Dashboard")
    st.subheader("Family Health Card Entry")
    
    with st.form("entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            h_name = st.text_input("Head of Family Name")
            f_name = st.text_input("Father/Husband Name")
            adh_no = st.text_input("Aadhar No (Last 4 Digits)")
        with col2:
            coord_name = st.text_input("Your Name (Coordinator)")
            members = st.text_area("Other Family Members (Comma separated)")
        
        submit = st.form_submit_button("Generate & Save Card")

    if submit:
        if h_name and adh_no and coord_name:
            # Card Generation Logic
            img = Image.new('RGB', (1000, 600), (255, 255, 255))
            draw = ImageDraw.Draw(img)
            draw.rectangle([0, 0, 1000, 120], fill="black")
            draw.text((80, 40), "SARV DHARM SMANYA KALYAN SAMITI", fill="white")
            
            # Text and QR
            draw.text((60, 200), f"Name: {h_name} | Father: {f_name}", fill="black")
            draw.text((60, 250), f"Aadhar: XXXX-XXXX-{adh_no}", fill="black")
            qr = qrcode.make(f"SDSKS-{adh_no}").resize((180, 180))
            img.paste(qr, (750, 180))
            
            # Show Preview
            st.image(img, caption="Preview")
            
            # Save Data
            entry = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Coordinator": coord_name,
                "Family_Head": h_name,
                "Aadhar_Last4": adh_no
            }
            save_to_db(entry)
            st.success("Card data saved to Admin records!")
        else:
            st.error("Please fill all required fields!")

# --- ADMIN DASHBOARD ---
elif role == "NGO Head (Admin)":
    st.title("🔐 Admin Management Panel")
    
    # Password Protection
    password = st.text_input("Enter Admin Password", type="password")
    if password == "NGO@123":  # Aap is password ko badal sakte hain
        st.success("Welcome, NGO Head!")
        
        try:
            df = pd.read_csv(DB_FILE)
            
            # Metrics
            c1, c2 = st.columns(2)
            c1.metric("Total Cards Issued", len(df))
            c2.metric("Total Coordinators Active", df['Coordinator'].nunique())
            
            # Data Table
            st.subheader("All Issued Records")
            st.dataframe(df, use_container_width=True)
            
            # Download Data
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download Full Excel Report", csv, "sdsks_full_report.csv", "text/csv")
            
        except FileNotFoundError:
            st.info("No records found yet. Ask coordinators to start entries.")
    elif password:
        st.error("Incorrect Password!")

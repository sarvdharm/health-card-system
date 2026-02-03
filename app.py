import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import qrcode
import pandas as pd
from datetime import datetime
import io

# Page Configuration
st.set_page_config(page_title="SDSKS Health Management System", layout="wide")

# Database File Name
DB_FILE = "sdsks_records.csv"

# Function to save record to CSV
def save_to_db(data):
    df = pd.DataFrame([data])
    df.to_csv(DB_FILE, mode='a', header=not pd.io.common.file_exists(DB_FILE), index=False)

# Sidebar Menu
st.sidebar.title("SDSKS Admin")
choice = st.sidebar.radio("Navigation", ["Generate Health Card", "Records Dashboard (Admin)"])

if choice == "Generate Health Card":
    st.title("🛡️ Family Health Card Generator")
    st.info("Niche di gayi details bharein aur 'Save & Generate' par click karein.")
    
    col1, col2 = st.columns(2)
    with col1:
        h_name = st.text_input("Head of Family Name")
        f_name = st.text_input("Father/Husband Name")
        adh_no = st.text_input("Aadhar No (Last 4 Digits)")
        coord_id = st.text_input("Coordinator ID/Name")
    
    with col2:
        m2 = st.text_input("Family Member 2")
        m3 = st.text_input("Family Member 3")
        m4 = st.text_input("Family Member 4")
        issue_date = datetime.now().strftime("%d-%m-%Y")

    if st.button("Save Data & Generate Card"):
        if h_name and adh_no:
            # --- CARD DESIGN LOGIC ---
            img = Image.new('RGB', (1000, 600), (255, 255, 255))
            draw = ImageDraw.Draw(img)
            
            # Header
            draw.rectangle([0, 0, 1000, 120], fill="#000000") # Black Header
            draw.rectangle([0, 120, 1000, 150], fill="#FF9933") # Orange Strip
            
            # Text
            draw.text((80, 40), "SARV DHARM SMANYA KALYAN SAMITI", fill="white")
            draw.text((350, 160), "FAMILY HEALTH PROTECTION CARD", fill="black")
            
            # Details
            draw.text((60, 230), f"Head: {h_name}", fill="black")
            draw.text((60, 270), f"Father: {f_name}", fill="black")
            draw.text((60, 310), f"Aadhar: XXXX-XXXX-{adh_no}", fill="black")
            draw.line([60, 360, 940, 360], fill="gray", width=2)
            draw.text((60, 380), f"Members: {m2}, {m3}, {m4}", fill="black")
            
            # QR Code
            qr_data = f"SDSKS-{adh_no} | {h_name} | Verified"
            qr = qrcode.make(qr_data).resize((200, 200))
            img.paste(qr, (750, 200))
            
            # Footer
            draw.text((60, 530), f"Date: {issue_date} | Coordinator: {coord_id}", fill="darkblue")
            
            # Display and Save
            st.image(img, caption="Card Preview")
            
            # Database Update
            new_data = {
                "Date": issue_date, 
                "Head_Name": h_name, 
                "Aadhar_Last4": adh_no, 
                "Coordinator": coord_id,
                "Members": f"{m2}, {m3}, {m4}"
            }
            save_to_db(new_data)
            
            # Download Button
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.download_button("Download Card Now", buf.getvalue(), f"{h_name}_card.png")
            st.success("Record Saved Successfully!")
        else:
            st.error("Please enter Name and Aadhar.")

elif choice == "Records Dashboard (Admin)":
    st.title("📊 SDSKS Management Dashboard")
    try:
        df = pd.read_csv(DB_FILE)
        st.metric("Total Cards Issued", len(df))
        st.write("Sabhi coordinators ka data niche dekhein:")
        st.dataframe(df, use_container_width=True)
        
        # Excel Download for Admin
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Full Report (CSV)", csv, "sdsks_report.csv", "text/csv")
    except:
        st.info("Abhi tak koi data save nahi hua hai.")

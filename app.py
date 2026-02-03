import streamlit as st
from PIL import Image, ImageDraw
import qrcode
import io

# Software Header
st.set_page_config(page_title="SDSKS Health Card")
st.title("🛡️ Family Health Card Generator")

# Information bharne ke liye Sidebar
with st.sidebar:
    st.header("Coordinators Entry Form")
    h_name = st.text_input("Head of Family Name", "Golu (H)")
    f_name = st.text_input("Father Name", "Misri")
    adh_no = st.text_input("Aadhar Number", "8888")
    st.divider()
    m2 = st.text_input("Member 2", "Nikki Kumari")
    m3 = st.text_input("Member 3", "Aradhya Kumari")
    m4 = st.text_input("Member 4", "Chhotu Kumar")

def create_card():
    # Card Design
    img = Image.new('RGB', (1000, 600), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 1000, 100], fill="black")
    draw.rectangle([0, 100, 1000, 140], fill="#f39c12")
    draw.text((80, 30), "SARV DHARM SMANYA KALYAN SAMITI", fill="white")
    
    # Text Data
    draw.text((50, 200), f"Name: {h_name} | Father: {f_name} | Aadhar: {adh_no}", fill="black")
    draw.text((50, 300), f"Members: {m2}, {m3}, {m4}", fill="black")
    
    # QR Code
    qr = qrcode.make(f"ID: SDSKS-{adh_no}").resize((160, 160))
    img.paste(qr, (780, 200))
    return img

if st.button("Generate Automatic Card"):
    card = create_card()
    st.image(card, caption="Aapka Card Taiyaar Hai")
    buf = io.BytesIO()
    card.save(buf, format="PNG")
    st.download_button("Download Card", buf.getvalue(), "health_card.png")

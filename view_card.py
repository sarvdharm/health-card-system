import streamlit as st
import database
import qrcode
from io import BytesIO
from PIL import Image

def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#134e4a", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def show_card_details(card_no):
    df_cards = database.get_cards()
    card_data = df_cards[df_cards['card_no'] == card_no]
    
    if not card_data.empty:
        row = card_data.iloc[0]
        
        # QR Code Data (Sirf basic info)
        qr_info = f"Card: {row['card_no']}\nName: {row['head_name']}\nStatus: {row['status']}"
        qr_img = generate_qr(qr_info)
        
        # Card Design
        st.markdown(f"""
        <div style="border: 3px solid #134e4a; border-radius: 20px; padding: 25px; width: 400px; background: linear-gradient(145deg, #ffffff, #f0fdf4); font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; box-shadow: 10px 10px 20px rgba(0,0,0,0.1);">
            <div style="text-align: center; border-bottom: 3px solid #fbbf24; padding-bottom: 15px; margin-bottom: 15px;">
                <img src="{database.LOGO_URL}" width="70"><br>
                <strong style="color: #064e3b; font-size: 20px;">SARV DHARM SMANYA KALYAN SAMITI</strong><br>
                <div style="background: #fbbf24; color: #064e3b; display: inline-block; padding: 2px 15px; border-radius: 20px; font-size: 12px; margin-top: 5px; font-weight: bold;">DIGITAL HEALTH CARD</div>
            </div>
            
            <table style="width: 100%; border-collapse: collapse; color: #1f2937;">
                <tr><td style="padding: 5px; font-weight: bold;">Card No:</td><td style="color: #dc2626; font-weight: bold;">{row['card_no']}</td></tr>
                <tr><td style="padding: 5px; font-weight: bold;">Head Name:</td><td>{row['head_name']}</td></tr>
                <tr><td style="padding: 5px; font-weight: bold;">Mobile:</td><td>{row['mobile']}</td></tr>
                <tr><td style="padding: 5px; font-weight: bold;">Panchayat:</td><td>{row['panchayat']}</td></tr>
                <tr><td style="padding: 5px; font-weight: bold;">Block/Dist:</td><td>{row['block']}, {row['district']}</td></tr>
                <tr><td style="padding: 5px; font-weight: bold;">Status:</td><td><span style="color: #059669;">● {row['status']}</span></td></tr>
            </table>
            
            <div style="text-align: right; margin-top: -60px;">
                <img src="data:image/png;base64,{st.image(qr_img, width=80)}" style="display:none;"> </div>
            <div style="text-align: center; margin-top: 20px;">
                 <img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data={row['card_no']}" width="80">
            </div>
            
            <div style="text-align: center; margin-top: 20px; font-size: 11px; color: #6b7280; font-style: italic;">
                "स्वास्थ्य और सेवा, हर घर तक - ग्रामीण बिहार में स्वास्थ्य क्रांति"
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Back to Dashboard"):
                st.session_state.view_card_no = None
                st.rerun()
        with col2:
            st.info("💡 Screenshot le kar print karein.")

    else:
        st.error("Data error!")

import streamlit as st
import database

def show_card_details(card_no):
    df_cards = database.get_cards()
    card_data = df_cards[df_cards['card_no'] == card_no]
    
    if not card_data.empty:
        row = card_data.iloc[0]
        
        # ID Card Design (HTML/CSS se)
        st.markdown(f"""
        <div style="border: 2px solid #134e4a; border-radius: 15px; padding: 20px; width: 350px; background-color: white; font-family: Arial;">
            <div style="text-align: center; border-bottom: 2px solid #fbbf24; padding-bottom: 10px; margin-bottom: 10px;">
                <img src="{database.LOGO_URL}" width="60"><br>
                <strong style="color: #134e4a; font-size: 18px;">SARV DHARM SMANYA KALYAN SAMITI</strong><br>
                <small>Digital Health Card</small>
            </div>
            
            <div style="color: #333;">
                <p><strong>Card No:</strong> <span style="color: red;">{row['card_no']}</span></p>
                <p><strong>Name:</strong> {row['head_name']}</p>
                <p><strong>Mobile:</strong> {row['mobile']}</p>
                <p><strong>Panchayat:</strong> {row['panchayat']}</p>
                <p><strong>Block:</strong> {row['block']}</p>
                <p><strong>Status:</strong> <span style="background: #e8f5e9; color: #2e7d32; padding: 2px 5px; border-radius: 4px;">{row['status']}</span></p>
            </div>
            
            <div style="text-align: center; margin-top: 15px; font-size: 10px; color: gray; border-top: 1px dashed #ccc; pt-10px;">
                सेवा, स्वास्थ्य और समानता - हर व्यक्ति का अधिकार
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⬅️ Back to List"):
            st.session_state.view_card_no = None
            st.rerun()
    else:
        st.error("Card data nahi mila!")

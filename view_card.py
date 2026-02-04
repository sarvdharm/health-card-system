import streamlit as st
import database

def show_card_details(card_no):
    df = database.get_cards()
    row = df[df['card_no'] == card_no].iloc[0]
    
    st.markdown(f"""
    <div style="border:5px solid #134e4a; padding:20px; border-radius:15px; background:white; width:350px;">
        <h3 style="color:#134e4a; text-align:center;">NGO HEALTH CARD</h3>
        <p><b>Card No:</b> {row['card_no']}</p>
        <p><b>Name:</b> {row['head_name']}</p>
        <p><b>Status:</b> {row['status']}</p>
        <hr>
        <p style="font-size:10px; text-align:center;">Valid for 4 Family Members</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Back"):
        st.session_state.view_card_no = None
        st.rerun()

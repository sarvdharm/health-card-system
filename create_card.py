import streamlit as st
import pandas as pd
import database
import datetime

def show_form():
    st.markdown(f"<div style='text-align:center'><img src='{database.LOGO_URL}' width='100'></div>", unsafe_allow_html=True)
    st.header("📝 New Health Card Registration")
    
    with st.form("health_card_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            head_name = st.text_input("Head of Family Name*")
            mobile = st.text_input("Mobile Number*")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
        with col2:
            panchayat = st.text_input("Panchayat Name*")
            block = st.text_input("Block Name*")
            district = st.text_input("District*")
            
        address = st.text_area("Full Address")
        
        submit = st.form_submit_button("Save & Generate Card No")
        
        if submit:
            if head_name and mobile and panchayat:
                df = database.get_cards()
                # Simple Card No generation (Like: SDSKS-2024-001)
                new_id = len(df) + 1
                card_no = f"SDSKS-{datetime.datetime.now().year}-{1000 + new_id}"
                
                new_data = {
                    "id": new_id,
                    "card_no": card_no,
                    "head_name": head_name,
                    "panchayat": panchayat,
                    "block": block,
                    "district": district,
                    "mobile": mobile,
                    "status": "Pending",
                    "created_by": st.session_state.user_id
                }
                
                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                df.to_csv("health_cards.csv", index=False)
                st.success(f"Registration Successful! Card No: {card_no}")
            else:
                st.error("Kripya saari zaroori (*) jaankari bharein.")

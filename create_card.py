import streamlit as st
import database
import datetime
import pandas as pd

def show_form():
    st.markdown("<h2 style='color: #134e4a;'>📝 नया हेल्थ कार्ड रजिस्ट्रेशन</h2>", unsafe_allow_html=True)
    
    with st.form("enhanced_card_form"):
        col1, col2 = st.columns(2)
        with col1:
            head_name = st.text_input("मुखिया का नाम (Head Name)*")
            father_husband = st.text_input("पिता/पति का नाम (Father/Husband Name)*")
        with col2:
            mobile = st.text_input("मोबाइल नंबर*")
            panchayat = st.text_input("पंचायत*")

        st.write("---")
        st.write("### 👨‍👩‍👧‍👦 अन्य परिवार के सदस्य (Other Members)")
        m2 = st.text_input("सदस्य 2 का नाम")
        m3 = st.text_input("सदस्य 3 का नाम")
        m4 = st.text_input("सदस्य 4 का नाम")

        submit = st.form_submit_button("डेटा सुरक्षित करें (Save Card)")

        if submit:
            if not head_name or not father_husband or not mobile:
                st.error("कृपया सभी जरूरी (*) जानकारी भरें।")
            else:
                df = database.get_cards()
                card_no = f"SDSKS-{datetime.datetime.now().year}-{1000 + len(df)}"
                
                new_data = {
                    "id": len(df) + 1,
                    "card_no": card_no,
                    "head_name": head_name,
                    "father_husband": father_husband,
                    "mobile": mobile,
                    "panchayat": panchayat,
                    "m2_name": m2 if m2 else "-",
                    "m3_name": m3 if m3 else "-",
                    "m4_name": m4 if m4 else "-",
                    "status": "Pending",
                    "created_by": st.session_state.user_id
                }
                
                updated_df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                updated_df.to_csv("health_cards.csv", index=False)
                st.success(f"बधाई हो! कार्ड सफलतापूर्वक बन गया है। नंबर: {card_no}")

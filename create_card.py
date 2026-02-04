import streamlit as st
import database
import datetime
import pandas as pd

def show_form():
    st.markdown("<h2 style='color: #134e4a;'>📝 नया हेल्थ कार्ड रजिस्ट्रेशन (₹200)</h2>", unsafe_allow_html=True)
    
    with st.form("professional_card_form"):
        # Member 1 (Head)
        col1, col2, col3 = st.columns(3)
        with col1: h_name = st.text_input("मुखिया का नाम*")
        with col2: h_father = st.text_input("पिता/पति का नाम*")
        with col3: h_aadhar = st.text_input("आधार नंबर (Last 4 digits)")

        st.write("---")
        # Members 2, 3, 4
        m2_cols = st.columns(3)
        m2_n = m2_cols[0].text_input("सदस्य 2 का नाम")
        m2_f = m2_cols[1].text_input("पिता/पति (M2)")
        m2_a = m2_cols[2].text_input("आधार (M2)")

        m3_cols = st.columns(3)
        m3_n = m3_cols[0].text_input("सदस्य 3 का नाम")
        m3_f = m3_cols[1].text_input("पिता/पति (M3)")
        m3_a = m3_cols[2].text_input("आधार (M3)")

        m4_cols = st.columns(3)
        m4_n = m4_cols[0].text_input("सदस्य 4 का नाम")
        m4_f = m4_cols[1].text_input("पिता/पति (M4)")
        m4_a = m4_cols[2].text_input("आधार (M4)")

        st.write("---")
        c_mob = st.text_input("मोबाइल नंबर*")
        c_panch = st.text_input("पंचायत*")

        if st.form_submit_button("Save Health Card"):
            if h_name and h_father and c_mob:
                df = database.get_cards()
                c_no = f"SDSKS-{datetime.datetime.now().year}-{2000 + len(df)}"
                
                new_row = {
                    "id": len(df)+1, "card_no": c_no, "head_name": h_name, 
                    "father_husband": h_father, "mobile": c_mob, "panchayat": c_panch,
                    "m2_name": m2_n, "m2_father": m2_f, "m2_aadhar": m2_a,
                    "m3_name": m3_n, "m3_father": m3_f, "m3_aadhar": m3_a,
                    "m4_name": m4_n, "m4_father": m4_f, "m4_aadhar": m4_a,
                    "status": "Pending", "created_by": st.session_state.user_id,
                    "issue_date": datetime.datetime.now().strftime("%d-%m-%Y")
                }
                pd.concat([df, pd.DataFrame([new_row])]).to_csv("health_cards.csv", index=False)
                st.success(f"Card Saved! ID: {c_no}")
            else:
                st.error("Zaroori jankari bharein!")

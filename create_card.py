import streamlit as st
import database, datetime, pandas as pd

def show_form():
    st.subheader("📝 Register New Health Card (₹200/4 Members)")
    with st.form("card_form"):
        name = st.text_input("Head Name")
        mob = st.text_input("Mobile")
        panch = st.text_input("Panchayat")
        submit = st.form_submit_button("Save Data")
        
        if submit and name and mob:
            df = database.get_cards()
            card_no = f"SDSKS-{datetime.datetime.now().year}-{1000 + len(df)}"
            new_row = {"id": len(df)+1, "card_no": card_no, "head_name": name, "panchayat": panch, "mobile": mob, "status": "Pending", "created_by": st.session_state.user_id}
            pd.concat([df, pd.DataFrame([new_row])]).to_csv("health_cards.csv", index=False)
            st.success(f"Saved! Card No: {card_no}")

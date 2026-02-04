import streamlit as st
import pandas as pd
import database, view_card

def show_dashboard():
    df_cards = database.get_cards()
    my_id = str(st.session_state.user_id)
    
    if st.session_state.user_role == "panchayat":
        display_df = df_cards[df_cards['created_by'].astype(str) == my_id]
    else:
        display_df = df_cards

    st.markdown("### 📊 Beneficiary Overview")
    m1, m2 = st.columns(2)
    m1.metric("Total Cards", len(display_df))
    m2.metric("Verified", len(display_df[display_df['status'] == 'Verified']))

    if 'view_card_no' not in st.session_state: st.session_state.view_card_no = None

    if st.session_state.view_card_no:
        view_card.show_card_details(st.session_state.view_card_no)
    else:
        st.dataframe(display_df[['card_no', 'head_name', 'status']], use_container_width=True)
        sel = st.selectbox("Select Card", display_df['card_no'].tolist())
        if st.button("👁️ View Card"):
            st.session_state.view_card_no = sel
            st.rerun()

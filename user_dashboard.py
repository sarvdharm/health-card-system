import streamlit as st
import database
import view_card

def show_dashboard():
    # Header logic
    st.markdown(f"""
        <div style="background-color: #f8fafc; padding: 15px; border-radius: 10px; border-bottom: 3px solid #134e4a; margin-bottom: 20px;">
            <h3 style="margin:0; color: #134e4a;">📋 लाभार्थी डैशबोर्ड (Beneficiary Dashboard)</h3>
            <p style="margin:0; color: gray;">Welcome, {st.session_state.user_name} | Role: {st.session_state.user_role.upper()}</p>
        </div>
    """, unsafe_allow_html=True)

    df_cards = database.get_cards()
    
    # Filter by user
    if st.session_state.user_role == 'panchayat':
        display_df = df_cards[df_cards['created_by'].astype(str) == str(st.session_state.user_id)]
    else:
        display_df = df_cards

    # NGO Statistics (As per Image 1000102887)
    s1, s2, s3 = st.columns(3)
    s1.metric("कुल लाभार्थी (Total)", len(display_df))
    s2.metric("पेंडिंग (Pending)", len(display_df[display_df['status'] == 'Pending']))
    s3.metric("सत्यापित (Verified)", len(display_df[display_df['status'] == 'Verified']))

    st.write("---")

    # Table Layout
    if not display_df.empty:
        st.write("#### हाल के रजिस्ट्रेशन (Recent Registrations)")
        st.dataframe(display_df[['card_no', 'head_name', 'panchayat', 'status']], use_container_width=True)
        
        sel = st.selectbox("कार्ड चुनें (Select Card)", display_df['card_no'].tolist())
        if st.button("👁️ View & Print Health Card"):
            st.session_state.view_card_no = sel
            st.rerun()
    else:
        st.warning("अभी तक कोई डेटा दर्ज नहीं किया गया है।")

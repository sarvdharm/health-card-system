import streamlit as st
import database

def show_dashboard():
    my_id = str(st.session_state.user_id)
    role = st.session_state.user_role
    username = st.session_state.user_name

    st.markdown(f"""
        <div style="background-color: #134e4a; color: white; padding: 15px; border-radius: 8px;">
            <strong>SARV DHARM NGO</strong> | Welcome, {username} ({role.upper()})
        </div>
    """, unsafe_allow_html=True)

    df_cards = database.get_cards()
    df_users = database.get_users()

    # Search Logic
    search_txt = st.text_input("🔍 Search by Name or Card No...")

    # Hierarchy Logic (Like your PHP SQL)
    if role in ['admin', 'staff']:
        display_df = df_cards
    elif role == 'block':
        sub_ids = df_users[df_users['ParentID'].astype(str) == my_id]['UserID'].tolist()
        display_df = df_cards[df_cards['created_by'].astype(str).isin([my_id] + [str(i) for i in sub_ids])]
    else:
        display_df = df_cards[df_cards['created_by'].astype(str) == my_id]

    if search_txt:
        display_df = display_df[display_df['head_name'].str.contains(search_txt, case=False, na=False)]

    st.table(display_df[['card_no', 'head_name', 'panchayat', 'status']])

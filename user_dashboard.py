import streamlit as st
import pandas as pd
import database
import view_card

def show_dashboard():
    my_id = str(st.session_state.user_id)
    role = st.session_state.user_role
    username = st.session_state.user_name

    # --- CUSTOM CSS FOR PROFESSIONAL LOOK ---
    st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #0c352f 0%, #134e4a 100%);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 2rem;
        }
        .stats-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 5px solid #fbbf24;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            text-align: center;
        }
        .stButton>button {
            background-color: #134e4a;
            color: white;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- TOP GREEN HEADER (Image 1000102888 jaisa) ---
    st.markdown(f"""
        <div class="main-header">
            <h1>Sarv Dharm Smanya Kalyan Samiti</h1>
            <p>Welcome back, <b>{username}</b> | Role: {role.upper()}</p>
        </div>
    """, unsafe_allow_html=True)

    # --- DATA LOADING ---
    df_cards = database.get_cards()
    df_users = database.get_users()

    # --- HIERARCHY LOGIC ---
    if role in ['admin', 'staff']:
        display_df = df_cards
    elif role == 'block':
        sub_ids = df_users[df_users['ParentID'].astype(str) == my_id]['UserID'].tolist()
        display_df = df_cards[df_cards['created_by'].astype(str).isin([my_id] + [str(i) for i in sub_ids])]
    else:
        display_df = df_cards[df_cards['created_by'].astype(str) == my_id]

    # --- STATS CARDS (Beneficiaries Overview) ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="stats-card"><h3>Total Cards</h3><h2>{len(display_df)}</h2></div>', unsafe_allow_html=True)
    with col2:
        pending = len(display_df[display_df['status'] == 'Pending'])
        st.markdown(f'<div class="stats-card" style="border-left-color: #ef4444;"><h3>Pending</h3><h2>{pending}</h2></div>', unsafe_allow_html=True)
    with col3:
        verified = len(display_df[display_df['status'] == 'Verified'])
        st.markdown(f'<div class="stats-card" style="border-left-color: #22c55e;"><h3>Verified</h3><h2>{verified}</h2></div>', unsafe_allow_html=True)

    st.write("##")

    # --- SEARCH & TABLE ---
    if 'view_card_no' not in st.session_state:
        st.session_state.view_card_no = None

    if st.session_state.view_card_no:
        view_card.show_card_details(st.session_state.view_card_no)
    else:
        st.write("### 📋 Recent Beneficiaries")
        
        # Search Box
        search = st.text_input("🔍 Search by Name or Card Number", placeholder="Type here to search...")
        if search:
            display_df = display_df[display_df['head_name'].str.contains(search, case=False, na=False) | 
                                    display_df['card_no'].str.contains(search, case=False, na=False)]

        # Professional Table
        if not display_df.empty:
            st.dataframe(display_df[['card_no', 'head_name', 'panchayat', 'status']], use_container_width=True)
            
            # Action Buttons
            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                sel = st.selectbox("Select Card for Action", display_df['card_no'].tolist())
            with c2:
                st.write("#") # Padding
                if st.button("👁️ View Full Card", use_container_width=True):
                    st.session_state.view_card_no = sel
                    st.rerun()
        else:
            st.info("No records found for your account.")

import streamlit as st
import pandas as pd

def show_dashboard():
    # User Info from Session (Like PHP $_SESSION)
    my_id = str(st.session_state.user_id)
    role = st.session_state.user_role
    username = st.session_state.user_name

    st.markdown(f"### 📋 Dashboard - Health Card Management")
    st.write(f"Logged in as: *{username}* ({role.upper()})")

    # Load Data
    df_cards = pd.read_csv("health_cards.csv")
    df_users = pd.read_csv("users_registry.csv")

    # --- SEARCH BOX (Like PHP search logic) ---
    search_txt = st.text_input("🔍 Search by Name or Card No...")
    if search_txt:
        df_cards = df_cards[df_cards['head_name'].str.contains(search_txt, case=False, na=False) | 
                            df_cards['card_no'].astype(str).str.contains(search_txt)]

    # --- HIERARCHY LOGIC (The PHP IF/ELSE logic) ---
    if role in ['admin', 'staff']:
        display_df = df_cards
    elif role == 'block':
        # Get IDs of Panchayat coordinators under this Block
        sub_ids = df_users[df_users['ParentID'].astype(str) == my_id]['UserID'].tolist()
        display_df = df_cards[df_cards['created_by'].astype(str).isin([my_id] + [str(i) for i in sub_ids])]
    else: # Panchayat
        display_df = df_cards[df_cards['created_by'].astype(str) == my_id]

    # New Registration Button for Panchayat
    if role == 'panchayat':
        if st.button("+ NEW REGISTRATION"):
            st.info("Registration form opening...")

    # --- DATA TABLE (Like PHP <table>) ---
    if not display_df.empty:
        # Display Table
        st.table(display_df[['card_no', 'head_name', 'panchayat', 'status']])
        
        # Action Buttons
        selected_id = st.selectbox("Select Card No for Action", display_df['card_no'].tolist())
        c1, c2, c3 = st.columns(3)
        with c1: st.button("👁️ View Card")
        with c2: 
            if role == 'block': st.button("✅ Verify")
        with c3:
            if role == 'admin': st.button("🗑️ Delete")
    else:
        st.warning("No records found.")

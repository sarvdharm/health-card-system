import streamlit as st
import pandas as pd
import os

# Database files
USER_DB = "users_registry.csv"
CARD_DB = "health_cards.csv"

def show_dashboard():
    # Session se user info lena (Jaise PHP mein $_SESSION hota hai)
    my_id = str(st.session_state.user_id)
    role = st.session_state.user_role
    username = st.session_state.user_name

    st.markdown(f"### Dashboard - Health Card Management")
    st.info(f"Welcome, {username} ({role.upper()})")

    # 1. Database Load Karna
    if not os.path.exists(CARD_DB):
        pd.DataFrame(columns=['id', 'card_no', 'head_name', 'panchayat', 'created_by', 'status']).to_csv(CARD_DB, index=False)
    
    df_cards = pd.read_csv(CARD_DB)
    df_users = pd.read_csv(USER_DB)

    # 2. SEARCH LOGIC (Jaise PHP mein $_POST['search_btn'] tha)
    search_query = st.text_input("🔍 Search by Name or Card No...")
    if search_query:
        df_cards = df_cards[df_cards['head_name'].str.contains(search_query, case=False) | 
                            df_cards['card_no'].astype(str).str.contains(search_query)]

    # 3. HIERARCHY LOGIC (Kaun kya dekhega)
    if role in ['admin', 'staff']:
        display_df = df_cards
    elif role == 'block':
        # Un coordinators ki list nikalna jinka parent ye Block admin hai
        my_subordinates = df_users[df_users['ParentID'].astype(str) == my_id]['UserID'].tolist()
        display_df = df_cards[df_cards['created_by'].astype(str).isin([my_id] + [str(x) for x in my_subordinates])]
    else: # Panchayat role
        display_df = df_cards[df_cards['created_by'].astype(str) == my_id]

    # 4. ACTION BUTTONS
    if role == 'panchayat':
        if st.button("➕ NEW REGISTRATION"):
            st.session_state.page = "create_card"
            st.rerun()

    # 5. DATA TABLE (Jaise PHP mein <table> hota hai)
    if not display_df.empty:
        # Table dikhana
        st.dataframe(display_df, use_container_width=True)
        
        # Action selector (Streamlit mein table ke andar button ki jagah select box use hota hai)
        selected_card = st.selectbox("Select Card to Action", display_df['card_no'].tolist())
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("👁️ View/Print"):
                st.write(f"Printing Card: {selected_card}")
        
        with col2:
            if role == 'block':
                if st.button("✅ Verify"):
                    st.success(f"Card {selected_card} Verified!")
        
        with col3:
            if role == 'admin':
                if st.button("🗑️ Delete", help="Delete karein?"):
                    st.warning("Card Deleted!")
    else:
        st.write("No records found.")

import streamlit as st
import pandas as pd
import os

# --- DATABASE CONFIG ---
USER_DB = "users_registry.csv"
CARD_DB = "health_cards.csv"

def show_dashboard():
    # Session se info lena (Jaise PHP mein $_SESSION['user_id'] hota hai)
    my_id = str(st.session_state.user_id)
    role = st.session_state.user_role.lower()
    username = st.session_state.user_name

    # --- HEADER SECTION (Jaise aapka .nav class hai) ---
    st.markdown(f"""
        <div style="background-color: #134e4a; color: white; padding: 15px; border-radius: 8px; display: flex; justify-content: space-between;">
            <span><strong>SARV DHARM NGO</strong> | Welcome, {username} ({role.upper()})</span>
        </div>
        <br>
    """, unsafe_allow_html=True)

    st.subheader("Dashboard - Health Card Management")

    # Files load karna
    if not os.path.exists(CARD_DB):
        pd.DataFrame(columns=['id', 'card_no', 'head_name', 'panchayat', 'created_by', 'status']).to_csv(CARD_DB, index=False)
    
    df_cards = pd.read_csv(CARD_DB)
    df_users = pd.read_csv(USER_DB)

    # --- SEARCH LOGIC (Jaise PHP mein isset($_POST['search_btn']) hai) ---
    search_txt = st.text_input("Search by Name or Card No...", placeholder="Enter name or card number...")

    # --- HIERARCHY LOGIC (PHP SQL logic ka Python version) ---
    if role in ['admin', 'staff']:
        # Admin sab dekh sakta hai
        display_df = df_cards
    elif role == 'block':
        # Block coordinator sirf unka data dekhega jinka ParentID uska UserID hai
        subordinates = df_users[df_users['ParentID'].astype(str) == my_id]['UserID'].tolist()
        # Filter: created_by in (subordinate_ids)
        display_df = df_cards[df_cards['created_by'].astype(str).isin([my_id] + [str(x) for x in subordinates])]
    else:
        # Panchayat coordinator sirf apna data dekhega
        display_df = df_cards[df_cards['created_by'].astype(str) == my_id]

    # Search filter apply karna
    if search_txt:
        display_df = display_df[
            display_df['head_name'].str.contains(search_txt, case=False, na=False) | 
            display_df['card_no'].astype(str).str.contains(search_txt)
        ]

    # --- ACTION BUTTONS ---
    if role == 'panchayat':
        if st.button("+ NEW REGISTRATION", type="primary"):
            st.session_state.page = "create_card"
            st.rerun()

    # --- DATA TABLE (Jaise aapka <table> tag hai) ---
    if not display_df.empty:
        # Column names change for better display
        ui_df = display_df[['card_no', 'head_name', 'panchayat', 'status']].copy()
        st.table(ui_df) # Streamlit ki clean table

        # Action Buttons (Har row ke liye)
        st.write("---")
        st.write("### Actions")
        selected_card = st.selectbox("Select Card No to Action", display_df['card_no'].tolist())
        
        row = display_df[display_df['card_no'] == selected_card].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button(f"👁️ View Card {selected_card}")
        
        with col2:
            if role == 'block' and row['status'] == 'Pending':
                if st.button("✅ Verify Status"):
                    # Update Logic
                    df_cards.loc[df_cards['card_no'] == selected_card, 'status'] = 'Verified'
                    df_cards.to_csv(CARD_DB, index=False)
                    st.success("Verified!")
                    st.rerun()
        
        with col3:
            if role == 'admin':
                if st.button("🗑️ Delete Card", key="del"):
                    df_cards = df_cards[df_cards['card_no'] != selected_card]
                    df_cards.to_csv(CARD_DB, index=False)
                    st.warning("Deleted!")
                    st.rerun()
    else:
        st.info("No records found.")

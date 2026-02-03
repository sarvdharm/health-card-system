import streamlit as st
import pandas as pd
import database
import view_card

def show_dashboard():
    my_id = str(st.session_state.user_id)
    role = st.session_state.user_role
    
    # 1. Load Data
    df_cards = database.get_cards()
    df_users = database.get_users()

    # 2. View Card Session Logic
    if 'view_card_no' not in st.session_state:
        st.session_state.view_card_no = None

    if st.session_state.view_card_no:
        view_card.show_card_details(st.session_state.view_card_no)
    else:
        st.subheader("📊 Health Card Records")

        # 3. Hierarchy Filter (Aapka PHP Logic)
        if role in ['admin', 'staff']:
            display_df = df_cards
        elif role == 'block':
            sub_ids = df_users[df_users['ParentID'].astype(str) == my_id]['UserID'].tolist()
            display_df = df_cards[df_cards['created_by'].astype(str).isin([my_id] + [str(i) for i in sub_ids])]
        else:
            display_df = df_cards[df_cards['created_by'].astype(str) == my_id]

        # 4. Table Display
        if not display_df.empty:
            st.dataframe(display_df[['card_no', 'head_name', 'panchayat', 'status']], use_container_width=True)
            
            # 5. Action Area
            st.write("---")
            col1, col2 = st.columns(2)
            
            with col1:
                selected_card = st.selectbox("Select Card No", display_df['card_no'].tolist())
                if st.button("👁️ View & Print Card"):
                    st.session_state.view_card_no = selected_card
                    st.rerun()
            
            with col2:
                # Sirf Block/Admin ko 'Verify' button dikhega
                if role in ['admin', 'block']:
                    current_status = display_df[display_df['card_no'] == selected_card]['status'].values[0]
                    if current_status == "Pending":
                        if st.button("✅ Mark as Verified"):
                            # CSV Update Logic
                            df_all = pd.read_csv("health_cards.csv")
                            df_all.loc[df_all['card_no'] == selected_card, 'status'] = 'Verified'
                            df_all.to_csv("health_cards.csv", index=False)
                            st.success(f"Card {selected_card} verified successfully!")
                            st.rerun()
        else:
            st.info("Abhi tak koi record nahi mila.")

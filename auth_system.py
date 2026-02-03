import streamlit as st
import database

def login():
    st.markdown("### 🔐 Multi-Level Coordinator Login")
    uid = st.text_input("UserID (Mobile Number)")
    pwd = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if uid == "admin" and pwd == "ngo786":
            st.session_state.update({"logged_in": True, "user_role": "admin", "user_name": "Chief Admin", "user_id": "0"})
            st.rerun()
        else:
            df = database.get_users()
            user = df[(df['UserID'].astype(str) == uid) & (df['Pass'].astype(str) == pwd)]
            if not user.empty:
                st.session_state.update({
                    "logged_in": True, "user_id": uid, 
                    "user_role": user.iloc[0]['Role'].lower(), "user_name": user.iloc[0]['Name']
                })
                st.rerun()
            else:
                st.error("Invalid Credentials!")

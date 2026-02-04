import streamlit as st
import pandas as pd
import database

def show_admin_controls():
    st.header("👑 Admin Panel")
    with st.form("staff_form"):
        name = st.text_input("Staff Name")
        uid = st.text_input("Mobile (UserID)")
        pwd = st.text_input("Password")
        role = st.selectbox("Role", ["District", "Block", "Panchayat"])
        parent = st.text_input("Parent ID (Mobile of Superior)")
        if st.form_submit_button("Add Staff"):
            df = database.get_users()
            new_user = {"UserID": uid, "Name": name, "Pass": pwd, "Role": role, "ParentID": parent, "Area": "Bihar"}
            pd.concat([df, pd.DataFrame([new_user])]).to_csv("users_registry.csv", index=False)
            st.success("Staff Added!")

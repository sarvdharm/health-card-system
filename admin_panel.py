import streamlit as st
import pandas as pd
import database

def show_admin_controls():
    st.header("👑 Admin Master Control")
    
    # Do Tabs banayenge: Ek Add karne ke liye, ek List dekhne ke liye
    tab1, tab2 = st.tabs(["➕ Add Coordinator", "📋 View All Staff"])
    
    with tab1:
        with st.form("registration_form"):
            st.write("### Register New Staff/Coordinator")
            name = st.text_input("Full Name")
            uid = st.text_input("Mobile No (This will be UserID)")
            pwd = st.text_input("Set Password")
            role = st.selectbox("Select Role", ["District", "Block", "Panchayat"])
            
            # Hierarchy Logic: Kaun kiske under hai
            parent = st.text_input("Parent ID (Kiske under kaam karega?)", help="Enter the Mobile/UserID of the senior officer")
            area = st.text_input("Assigned Area (District/Block/Panchayat Name)")
            
            submit = st.form_submit_button("Create Account")
            
            if submit:
                if name and uid and pwd:
                    df = database.get_users()
                    # Check if user already exists
                    if uid in df['UserID'].astype(str).values:
                        st.error("Ye Mobile Number pehle se registered hai!")
                    else:
                        new_user = {
                            "UserID": uid, "Name": name, "Pass": pwd, 
                            "Role": role, "ParentID": parent, "Area": area
                        }
                        # Save to CSV via database module
                        df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
                        df.to_csv("users_registry.csv", index=False)
                        st.success(f"Successfully Registered: {name} as {role}")
                else:
                    st.warning("Please fill all required fields.")

    with tab2:
        st.write("### Registered User Registry")
        df_list = database.get_users()
        if not df_list.empty:
            st.dataframe(df_list, use_container_width=True)
        else:
            st.info("Abhi tak koi user register nahi hua hai.")

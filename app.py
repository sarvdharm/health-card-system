import streamlit as st
import pandas as pd
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="SDSKS Management", layout="wide")

# Database setup
USER_DB = "users_registry.csv"
if not os.path.exists(USER_DB):
    pd.DataFrame(columns=['UserID', 'Name', 'Pass', 'Role', 'ParentID', 'Area']).to_csv(USER_DB, index=False)

# --- STYLING (Professional Green Theme) ---
st.markdown("""
    <style>
    .main-header { background-color: #0c352f; color: white; padding: 15px; text-align: center; border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 5px; font-weight: bold; }
    .status-card { background-color: #e8f5e9; padding: 15px; border-radius: 10px; border-left: 5px solid #2e7d32; }
    </style>
    <div class="main-header"><h1>Sarv Dharm Smanya Kalyan Samiti</h1></div>
""", unsafe_allow_html=True)

# --- SESSION LOGIC ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None

# --- NAVIGATION ---
cols = st.columns(6)
if cols[0].button("🏠 Home"): st.session_state.page = "home"
if cols[4].button("👥 Login Portal"): st.session_state.page = "login"
if cols[5].button("💳 Health Card"): st.session_state.page = "card"

if "page" not in st.session_state: st.session_state.page = "home"

# --- LOGIN LOGIC ---
if st.session_state.page == "login":
    if not st.session_state.logged_in:
        st.subheader("🔐 Staff & Coordinator Login")
        u_id = st.text_input("UserID (Mobile)")
        u_pw = st.text_input("Password", type="password")
        
        if st.button("Sign In"):
            if u_id == "admin" and u_pw == "ngo786":
                st.session_state.update({"logged_in": True, "user_role": "Admin", "user_name": "Chief Admin", "user_id": "admin"})
                st.rerun()
            else:
                df = pd.read_csv(USER_DB)
                user = df[(df['UserID'].astype(str) == u_id) & (df['Pass'].astype(str) == u_pw)]
                if not user.empty:
                    st.session_state.update({
                        "logged_in": True, "user_id": u_id, 
                        "user_role": user.iloc[0]['Role'], "user_name": user.iloc[0]['Name']
                    })
                    st.rerun()
                else: st.error("Invalid Credentials!")
    
    else:
        # LOGGED IN VIEW (Identify User)
        st.markdown(f"""<div class="status-card">
            <h3>✅ Profile: {st.session_state.user_name}</h3>
            <p><b>Role:</b> {st.session_state.user_role} | <b>ID:</b> {st.session_state.user_id}</p>
        </div>""", unsafe_allow_html=True)
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

        st.divider()

        # 1. ADMIN PANEL (Yahan dikhenge District/Block/Panchayat Coordinators)
        if st.session_state.user_role == "Admin":
            st.header("👑 Admin Master Control")
            
            tab1, tab2 = st.tabs(["View All Coordinators", "Add New Coordinator"])
            
            with tab1:
                df_all = pd.read_csv(USER_DB)
                if not df_all.empty:
                    # Filter by Role
                    role_filter = st.selectbox("Filter by Role", ["All", "District", "Block", "Panchayat"])
                    if role_filter != "All":
                        st.dataframe(df_all[df_all['Role'] == role_filter])
                    else:
                        st.dataframe(df_all)
                else: st.info("No coordinators found.")

            with tab2:
                with st.form("add_coord"):
                    n = st.text_input("Name")
                    p = st.text_input("Mobile (UserID)")
                    pw = st.text_input("Password")
                    r = st.selectbox("Role", ["District", "Block", "Panchayat"])
                    parent = st.text_input("Parent ID (Kiske under kaam karega?)")
                    area = st.text_input("Area (District/Block Name)")
                    if st.form_submit_button("Create ID"):
                        df = pd.read_csv(USER_DB)
                        new_data = {"UserID": p, "Name": n, "Pass": pw, "Role": r, "ParentID": parent, "Area": area}
                        pd.concat([df, pd.DataFrame([new_data])]).to_csv(USER_DB, index=False)
                        st.success(f"ID Created for {n}!")

        # 2. BLOCK COORDINATOR VIEW (Aapne kaha tha ki apne under walon ka data dikhe)
        if st.session_state.user_role == "Block":
            st.header("📊 My Panchayat Team")
            df_all = pd.read_csv(USER_DB)
            my_team = df_all[df_all['ParentID'].astype(str) == str(st.session_state.user_id)]
            st.table(my_team[['Name', 'UserID', 'Area']])

# --- HEALTH CARD PAGE ---
elif st.session_state.page == "card":
    if st.session_state.logged_in:
        st.header("💳 Health Card Generation")
        st.write(f"Logged in as: {st.session_state.user_name} ({st.session_state.user_role})")
        # Card form logic...
    else:
        st.warning("Please Login first to access Health Card System.")

elif st.session_state.page == "home":
    st.image("https://img.freepik.com/free-vector/medical-care-concept-landing-page_52683-20202.jpg")

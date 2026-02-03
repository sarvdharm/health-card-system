import streamlit as st
import pandas as pd
import os

# --- 1. CONFIGURATION (Jaise config.php) ---
st.set_page_config(page_title="SDSKS Digital Portal", layout="wide")

# Database Files
USER_DB = "users_registry.csv"

def init_db():
    if not os.path.exists(USER_DB):
        # ParentID se pata chalega kaun kiske under hai
        pd.DataFrame(columns=['UserID', 'Name', 'Pass', 'Role', 'ParentID', 'Area']).to_csv(USER_DB, index=False)

init_db()

# --- 2. CSS & HEADER (Jaise Image 1000102888) ---
st.markdown("""
    <style>
    .main-header { background-color: #0c352f; color: white; padding: 20px; text-align: center; border-radius: 10px; }
    .user-info { background-color: #e8f5e9; padding: 10px; border-radius: 5px; border-left: 5px solid #2e7d32; margin-bottom: 20px; }
    .stButton>button { border-radius: 8px; font-weight: bold; }
    </style>
    <div class="main-header">
        <h1>Sarv Dharm Smanya Kalyan Samiti</h1>
        <p>स्वास्थ्य और सेवा, हर घर तक</p>
    </div>
""", unsafe_allow_html=True)

# --- 3. SESSION & NAVIGATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Top Menu Buttons
cols = st.columns(6)
if cols[0].button("🏠 Home"): st.session_state.page = "home"
if cols[4].button("👥 Login Portal"): st.session_state.page = "login"
if cols[5].button("💳 Health Card"): st.session_state.page = "card"

if "page" not in st.session_state: st.session_state.page = "home"

# --- 4. LOGIN SYSTEM ---
if st.session_state.page == "login":
    if not st.session_state.logged_in:
        st.subheader("🔐 Multi-Level Login")
        uid = st.text_input("UserID (Mobile)")
        upw = st.text_input("Password", type="password")
        
        if st.button("Login"):
            # Master Admin Login
            if uid == "admin" and upw == "ngo786":
                st.session_state.update({"logged_in": True, "user_role": "Admin", "user_name": "Chief Admin", "user_id": "admin"})
                st.rerun()
            else:
                df = pd.read_csv(USER_DB)
                user = df[(df['UserID'].astype(str) == uid) & (df['Pass'].astype(str) == upw)]
                if not user.empty:
                    st.session_state.update({
                        "logged_in": True, "user_id": uid, 
                        "user_role": user.iloc[0]['Role'], "user_name": user.iloc[0]['Name']
                    })
                    st.rerun()
                else: st.error("Galt ID ya Password!")
    
    else:
        # LOGGED IN VIEW (Identify Who is Logged In)
        st.markdown(f"""
            <div class="user-info">
                <h4>✅ Welcome: {st.session_state.user_name}</h4>
                <p><b>Role:</b> {st.session_state.user_role} | <b>UserID:</b> {st.session_state.user_id}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

        st.divider()

        # --- ROLE BASED DASHBOARDS ---

        # 1. ADMIN: Can create District/Block/Panchayat IDs
        if st.session_state.user_role == "Admin":
            st.header("👑 Admin: Manage All Coordinators")
            with st.expander("➕ Create New Staff/Coordinator ID"):
                with st.form("add_user"):
                    n = st.text_input("Full Name")
                    m = st.text_input("Mobile (UserID)")
                    p = st.text_input("Set Password")
                    r = st.selectbox("Role", ["District", "Block", "Panchayat"])
                    parent = st.text_input("Parent ID (Kiske under kaam karega?)")
                    area = st.text_input("Assign Area (District/Block Name)")
                    if st.form_submit_button("Generate & Save"):
                        df = pd.read_csv(USER_DB)
                        new_row = {"UserID": m, "Name": n, "Pass": p, "Role": r, "ParentID": parent, "Area": area}
                        pd.concat([df, pd.DataFrame([new_row])]).to_csv(USER_DB, index=False)
                        st.success(f"ID Created for {n} successfully!")
            
            st.write("### Registered Staff List")
            st.dataframe(pd.read_csv(USER_DB))

        # 2. BLOCK COORDINATOR: Can see their Panchayat Coordinators
        if st.session_state.user_role == "Block":
            st.header("📊 My Panchayat Team")
            df_all = pd.read_csv(USER_DB)
            # Logic: Show only those whose ParentID matches my UserID
            my_team = df_all[df_all['ParentID'].astype(str) == str(st.session_state.user_id)]
            st.table(my_team[['Name', 'UserID', 'Area']])

# --- 5. HOME PAGE ---
elif st.session_state.page == "home":
    st.image("https://img.freepik.com/free-vector/medical-care-concept-landing-page_52683-20202.jpg")
    st.write("### NGO Beneficiaries (Image 1000102887)")
    st.info("Laborers, Farmers, and Small Businessmen are our priority.")

import streamlit as st
import pandas as pd
import os

# --- 1. CONFIG & UI ---
st.set_page_config(page_title="SDSKS Management", layout="wide")

st.markdown("""
    <style>
    .main-header { background-color: #0c352f; color: white; padding: 15px; text-align: center; border-radius: 10px; }
    .user-profile { background-color: #f1f8e9; border-left: 5px solid #2e7d32; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
    .role-tag { background-color: #1a7b8c; color: white; padding: 2px 10px; border-radius: 10px; font-size: 14px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Header (Image 1000102888 jaisa)
st.markdown('<div class="main-header"><h1>Sarv Dharm Smanya Kalyan Samiti</h1><p>सेवा, स्वास्थ्य और समानता</p></div>', unsafe_allow_html=True)

# Navigation
cols = st.columns(6)
if cols[0].button("🏠 Home"): st.session_state.page = "home"
if cols[4].button("👥 Login Portal"): st.session_state.page = "login"
if cols[5].button("💳 Health Card"): st.session_state.page = "card"

# --- 2. LOGIN IDENTIFICATION LOGIC ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    # Ye section dikhayega ki kaun login hai
    st.markdown(f"""
        <div class="user-profile">
            <span style='font-size: 18px;'>👋 Welcome, <b>{st.session_state.user_name}</b></span> | 
            <span>Role: <span class="role-tag">{st.session_state.user_role}</span></span> |
            <span>ID: {st.session_state.user_id}</span>
        </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- 3. PAGE CONTENT ---
page = st.session_state.get("page", "home")

if page == "login":
    if not st.session_state.logged_in:
        st.subheader("🔐 Staff & Coordinator Login")
        u_id = st.text_input("UserID (Mobile)")
        u_pw = st.text_input("Password", type="password")
        
        if st.button("Login"):
            # Master Admin Check
            if u_id == "admin" and u_pw == "ngo786":
                st.session_state.update({"logged_in": True, "user_role": "Admin", "user_name": "NGO Admin", "user_id": "001"})
                st.rerun()
            else:
                # Yahan hum CSV se baaki coordinators (District/Block/Panchayat) ko verify karenge
                try:
                    df = pd.read_csv("users_registry.csv")
                    user = df[(df['UserID'].astype(str) == u_id) & (df['Pass'].astype(str) == u_pw)]
                    if not user.empty:
                        st.session_state.update({
                            "logged_in": True, "user_id": u_id, 
                            "user_role": user.iloc[0]['Role'], "user_name": user.iloc[0]['Name']
                        })
                        st.rerun()
                    else: st.error("Invalid Credentials!")
                except: st.error("No users registered yet. Please contact Admin.")

elif page == "home":
    st.image("https://img.freepik.com/free-vector/medical-care-concept-landing-page_52683-20202.jpg")

import streamlit as st
import database
import auth_system
import main_controller

# Page Config
st.set_page_config(page_title="Sarv Dharm NGO Portal", layout="wide")

# Initialize Session State (Error Fix)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "home"

database.init_db()

# --- PROFESSIONAL NGO TOP NAV BAR ---
st.markdown("""
    <div style="background: linear-gradient(90deg, #0c352f 0%, #134e4a 100%); padding: 10px; border-radius: 5px; display: flex; justify-content: space-between; align-items: center; color: white;">
        <div style="display: flex; align-items: center;">
            <img src="https://raw.githubusercontent.com/your-username/your-repo/main/logo.jpg" width="40" style="margin-right: 10px;">
            <span style="font-weight: bold; font-size: 14px;">Sarv Dharm Smanya Kalyan Samiti</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Navigation Buttons (Jaise aapki image mein hai)
nav_cols = st.columns([1,1,1,1,1,1,2])
if nav_cols[0].button("🏠 Home"): st.session_state.page = "home"
if nav_cols[1].button("👨‍⚕️ Doctors"): st.info("Doctor list jald aa rahi hai...")
if nav_cols[2].button("📄 Docs"): st.info("Documents section maintenance mein hai.")
if nav_cols[3].button("🔬 Labs"): st.info("Lab tie-ups jald update honge.")
if nav_cols[4].button("💼 Employer"): st.info("Employer portal process mein hai.")
if nav_cols[5].button("💳 Health Card"): st.session_state.page = "login"

if not st.session_state.logged_in:
    if st.session_state.page == "login":
        auth_system.login()
    else:
        # HOME PAGE HERO SECTION (Image 1000102888 look)
        st.markdown("""
            <div style="text-align: center; padding: 40px 0;">
                <h1 style="color: #134e4a;">सर्व धर्म समान कल्याण समिति</h1>
                <p style="font-size: 18px; color: #666;">सेवा, स्वास्थ्य और समानता - हर व्यक्ति का अधिकार</p>
            </div>
            <div style="background-color: #134e4a; color: white; padding: 40px; border-radius: 15px; text-align: center;">
                <h2 style="font-size: 32px;">स्वास्थ्य और सेवा, हर घर तक - ग्रामीण बिहार में स्वास्थ्य क्रांति</h2>
                <p style="font-size: 18px; opacity: 0.9;">हमारी NGO का उद्देश्य ग्रामीण क्षेत्रों में स्वास्थ्य जागरूकता और प्राथमिक चिकित्सा पहुँचाना है।</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Features Section
        f1, f2, f3 = st.columns(3)
        with f1:
            st.markdown("""<div style="background: #f8fafc; padding: 20px; border-radius: 10px; border-bottom: 5px solid #134e4a; height: 200px;">
                <h3>🏥 निःशुल्क मेडिकल कैंप</h3><p>मासिक स्वास्थ्य जाँच शिविर - बीपी, शुगर, आँख जाँच</p></div>""", unsafe_allow_html=True)
        with f2:
            st.markdown("""<div style="background: #f8fafc; padding: 20px; border-radius: 10px; border-bottom: 5px solid #134e4a; height: 200px;">
                <h3>🍏 स्वास्थ्य जागरूकता</h3><p>स्वच्छता, पोषण एवं टीकाकरण जागरूकता कार्यक्रम</p></div>""", unsafe_allow_html=True)
        with f3:
            st.markdown("""<div style="background: #f8fafc; padding: 20px; border-radius: 10px; border-bottom: 5px solid #134e4a; height: 200px;">
                <h3>🤝 रिफरल सहायता</h3><p>गंभीर मामलों के लिए बड़े अस्पतालों में समन्वय</p></div>""", unsafe_allow_html=True)
else:
    main_controller.route_user()

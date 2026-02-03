import streamlit as st
import database
import auth_system
import main_controller

# Page Setup
st.set_page_config(page_title="Sarv Dharm NGO Portal", layout="wide")

# Initialize Session State (Error fix karne ke liye)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "home"

database.init_db()

# --- NGO STYLE TOP BANNER (As per image 1000102888) ---
st.markdown("""
    <div style="background: linear-gradient(90deg, #0c352f 0%, #134e4a 100%); padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0; font-family: 'Arial';">सर्व धर्म समान कल्याण समिति</h1>
        <p style="color: #fbbf24; margin: 5px 0 0 0; font-weight: bold;">सेवा, स्वास्थ्य और समानता - हर व्यक्ति का अधिकार</p>
    </div>
""", unsafe_allow_html=True)

if not st.session_state.logged_in:
    # Navigation Buttons with Icons
    cols = st.columns([1,1,1,1,1])
    if cols[0].button("🏠 Home"): st.session_state.page = "home"
    if cols[4].button("🔐 Staff Login"): st.session_state.page = "login"

    if st.session_state.page == "login":
        auth_system.login()
    else:
        # NGO Home Page Content (As per image 1000102888)
        st.markdown("""
            <div style="background-color: #f0fdf4; padding: 30px; border-radius: 15px; border-left: 8px solid #134e4a;">
                <h2 style="color: #064e3b;">स्वास्थ्य और सेवा, हर घर तक - ग्रामीण बिहार में स्वास्थ्य क्रांति</h2>
                <p>हमारी NGO का उद्देश्य ग्रामीण और शहरी क्षेत्रों में स्वास्थ्य जागरूकता, निःशुल्क जाँच शिविर और प्राथमिक चिकित्सा सेवाएँ पहुँचाना है।</p>
            </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1: st.info("🏥 *निःशुल्क मेडिकल कैंप*\nमासिक स्वास्थ्य जाँच शिविर")
        with c2: st.success("🍏 *स्वास्थ्य जागरूकता*\nस्वच्छता, पोषण एवं शिशु स्वास्थ्य")
        with c3: st.warning("🤝 *रिफरल सहायता*\nगंभीर मामलों के लिए अस्पताल समन्वय")
else:
    main_controller.route_user()

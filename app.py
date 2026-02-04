import streamlit as st
import database
import auth_system
import main_controller

# Page Config
st.set_page_config(page_title="Sarv Dharm NGO Portal", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = "home"

database.init_db()

# --- TOP NAVIGATION BAR (As per Image 1000102888) ---
st.markdown("""
    <div style="background: linear-gradient(90deg, #0c352f 0%, #134e4a 100%); padding: 15px; border-radius: 5px; text-align: center; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0; font-family: 'Arial';">सर्व धर्म समान कल्याण समिति</h1>
        <p style="color: #fbbf24; margin: 5px 0 0 0; font-weight: bold;">सेवा, स्वास्थ्य और समानता - हर व्यक्ति का अधिकार</p>
    </div>
""", unsafe_allow_html=True)

if not st.session_state.logged_in:
    # Navigation Buttons
    nav_cols = st.columns([1,1,1,1,1])
    if nav_cols[0].button("🏠 Home"): st.session_state.page = "home"
    if nav_cols[4].button("🔐 Staff Login"): st.session_state.page = "login"

    if st.session_state.page == "login":
        auth_system.login()
    else:
        # --- HERO SECTION ---
        st.markdown("""
            <div style="background-color: #134e4a; color: white; padding: 50px; border-radius: 20px; text-align: center; margin-bottom: 30px;">
                <h2 style="font-size: 30px; margin-bottom: 15px;">Shiksha स्वास्थ्य एवं सुरक्षा योजना</h2>
                <p style="font-size: 18px; opacity: 0.9; max-width: 800px; margin: 0 auto;">
                यह योजना समाज के हर वर्ग को स्वास्थ्य सुरक्षा, शिक्षा और आर्थिक विकास के अवसर प्रदान करने के लिए बनाई गई है। हमारा लक्ष्य है कि कोई भी व्यक्ति आर्थिक अभाव के कारण स्वास्थ्य सेवाओं से वंचित न रहे।
                </p>
            </div>
        """, unsafe_allow_html=True)

        # --- MISSION, VISION, PLAN (Side by Side) ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""<div style="background: #fdfcf0; padding: 20px; border-radius: 15px; border-top: 5px solid #fbbf24; height: 350px;">
                <h3 style="color: #134e4a;">🎯 मिशन (Mission)</h3>
                <p style="font-size: 14px; color: #333;">हर नागरिक को समय पर, सस्ती और गुणवत्तापूर्ण स्वास्थ्य सेवाएं उपलब्ध कराई जाएं। ग्रामीण और वंचित वर्ग के लोगों के जीवन की गुणवत्ता सुधारना ही हमारा मुख्य लक्ष्य है।</p>
                </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown("""<div style="background: #f0fdf4; padding: 20px; border-radius: 15px; border-top: 5px solid #134e4a; height: 350px;">
                <h3 style="color: #134e4a;">👁️ विजन (Vision)</h3>
                <p style="font-size: 14px; color: #333;">एक ऐसा भारत, जहाँ कोई भी व्यक्ति आर्थिक कारणों से स्वास्थ्य सेवाओं से वंचित न रहे। सपना: 'स्वस्थ भारत, जागरूक भारत, सशक्त भारत'</p>
                </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown("""<div style="background: #fef2f2; padding: 20px; border-radius: 15px; border-top: 5px solid #ef4444; height: 350px;">
                <h3 style="color: #134e4a;">👥 लाभार्थी (Beneficiaries)</h3>
                <ul style="font-size: 13px; color: #333;">
                    <li>ग्रामीण और शहरी गरीब परिवार</li>
                    <li>महिलाएं, बच्चे और वरिष्ठ नागरिक</li>
                    <li>मजदूर, किसान और छोटे व्यवसायी</li>
                    <li>दिव्यांगजन और निम्न आय वर्ग</li>
                </ul>
                </div>""", unsafe_allow_html=True)

        # --- KEY FEATURES SECTION (Card Benefits) ---
        st.write("##")
        st.markdown("<h2 style='text-align:center; color: #134e4a;'>💎 योजना की मुख्य विशेषताएं</h2>", unsafe_allow_html=True)
        
        f1, f2, f3 = st.columns(3)
        with f1:
            st.info("💳 *हेल्थ कार्ड योजना*\nसिर्फ ₹200 में 4 सदस्यों का वार्षिक स्वास्थ्य संरक्षण।")
            st.success("🏥 *मुफ्त जांच शिविर*\nहर पंचायत में महीने में 1 बार मुफ्त स्वास्थ्य शिविर।")
        with f2:
            st.info("👨‍⚕️ *डॉक्टर फीस में छूट*\nNGO डॉक्टरों की फीस में 20% से 50% तक की भारी बचत।")
            st.success("💊 *दवाओं पर बचत*\nदवाओं पर 30% - 50% और टेस्ट पर 20% - 40% छूट।")
        with f3:
            st.info("📢 *जागरूकता कार्यक्रम*\nस्वच्छता, पोषण और जीवनशैली में सुधार के कार्यक्रम।")
            st.success("📚 *सामाजिक विकास*\nशिक्षा, कौशल प्रशिक्षण और विकास गतिविधियां।")

        # --- FOOTER / CONTACT SECTION ---
        st.write("---")
        st.markdown("""
            <div style="background: #0c352f; color: white; padding: 30px; border-radius: 15px; text-align: center;">
                <h4>संपर्क सूत्र | Contact Us</h4>
                <p>📍 कार्यालय: Bettiah Branch, West Champaran, Bihar</p>
                <p>📞 हेल्पलाइन: +91-XXXXXXXXXX | 📧 ईमेल: info@sarvdharmngo.org</p>
                <hr style="border-color: #134e4a;">
                <p style="font-size: 12px; opacity: 0.7;">Sarv Dharm Smanya Kalyan Samiti © 2026 | Registration No: S000338/2021/2022</p>
            </div>
        """, unsafe_allow_html=True)

else:
    main_controller.route_user()

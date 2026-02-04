import streamlit as st
import database

def show_card_details(card_no):
    df = database.get_cards()
    row = df[df['card_no'] == card_no].iloc[0]
    
    # CSS for exact match with your uploaded photo 1000095004.jpg
    st.markdown(f"""
    <style>
    .card-box {{ width: 450px; border: 1px solid #000; border-radius: 8px; overflow: hidden; font-family: sans-serif; background: white; }}
    .c-header {{ background: black; color: white; padding: 10px; display: flex; align-items: center; gap: 10px; }}
    .c-sub {{ background: #fbbf24; color: black; text-align: center; font-weight: bold; font-size: 12px; border-top: 1px solid #000; border-bottom: 1px solid #000; }}
    .c-table {{ width: 100%; border-collapse: collapse; font-size: 11px; }}
    .c-table th {{ background: #f0f0f0; text-align: left; }}
    .c-table td, .c-table th {{ border: 0.5px solid #eee; padding: 4px; }}
    </style>
    
    <div class="card-box">
        <div class="c-header">
            <img src="{database.LOGO_URL}" width="40">
            <div>SARV DHARM SMANYA KALYAN SAMITI<br><small>Reg No: NGO/8000333/2021-22</small></div>
        </div>
        <div class="c-sub">FAMILY HEALTH PROTECTION CARD</div>
        <div style="padding:5px; font-weight:bold; background:#000; color:#fff; display:inline-block; margin:5px; border-radius:3px;">ID: {row['card_no']}</div>
        <table class="c-table">
            <tr><th>Member Name</th><th>Father/Husband</th><th>Aadhar</th></tr>
            <tr><td>{row['head_name']} (H)</td><td>{row['father_husband']}</td><td>-</td></tr>
            <tr><td>{row['m2_name']}</td><td>{row['m2_father']}</td><td>{row['m2_aadhar']}</td></tr>
            <tr><td>{row['m3_name']}</td><td>{row['m3_father']}</td><td>{row['m3_aadhar']}</td></tr>
            <tr><td>{row['m4_name']}</td><td>{row['m4_father']}</td><td>{row['m4_aadhar']}</td></tr>
        </table>
        <div style="display:flex; justify-content:space-between; padding:10px; align-items:center;">
            <div style="font-size:10px;">Issue: {row['issue_date']}<br>Expiry: One Year from Issue</div>
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=80x80&data={row['card_no']}" width="60">
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Download / Back"):
        st.session_state.view_card_no = None
        st.rerun()

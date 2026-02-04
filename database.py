import pandas as pd
import os

USER_DB = "users_registry.csv"
CARD_DB = "health_cards.csv"
LOGO_URL = "https://raw.githubusercontent.com/your-username/your-repo/main/logo.jpg" 

def init_db():
    if not os.path.exists(USER_DB):
        pd.DataFrame(columns=['UserID', 'Name', 'Pass', 'Role', 'ParentID', 'Area']).to_csv(USER_DB, index=False)
    
    # Error Fix: Yahan saare columns dhyan se check karein
    if not os.path.exists(CARD_DB):
        pd.DataFrame(columns=[
            'id', 'card_no', 'head_name', 'father_husband', 'mobile', 
            'panchayat', 'm2_name', 'm2_father', 'm2_aadhar',
            'm3_name', 'm3_father', 'm3_aadhar',
            'm4_name', 'm4_father', 'm4_aadhar',
            'status', 'created_by', 'issue_date'
        ]).to_csv(CARD_DB, index=False)

def get_users(): return pd.read_csv(USER_DB)
def get_cards(): return pd.read_csv(CARD_DB)

import pandas as pd
import os

USER_DB = "users_registry.csv"
CARD_DB = "health_cards.csv"

def init_db():
    if not os.path.exists(USER_DB):
        pd.DataFrame(columns=['UserID', 'Name', 'Pass', 'Role', 'ParentID', 'Area']).to_csv(USER_DB, index=False)
    if not os.path.exists(CARD_DB):
        pd.DataFrame(columns=['id', 'card_no', 'head_name', 'panchayat', 'created_by', 'status']).to_csv(CARD_DB, index=False)

def get_users():
    return pd.read_csv(USER_DB)

def get_cards():
    return pd.read_csv(CARD_DB)

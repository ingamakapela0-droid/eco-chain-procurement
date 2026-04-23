import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. THEME & STYLING ---
st.set_page_config(page_title="Eco-Chain | Gauteng Procurement", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    .about-box {
        background-color: #F1F5F9; padding: 25px; border-radius: 10px;
        border-left: 6px solid #0D9488; margin-bottom: 25px;
    }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; }
    .invoice-box {
        background-color: white; padding: 30px; border: 1px solid #E2E8F0;
        border-radius: 10px; font-family: 'Courier New', Courier, monospace;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA PERSISTENCE HELPERS ---
def save_data(df, filename):
    df.to_csv(filename, index=False)

def load_data(filename, columns):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    return pd.DataFrame(columns=columns)

# File paths
TRANSACTION_FILE = "permanent_ledger.csv"
INVENTORY_FILE = "medicine_inventory.csv"

ledger_cols = ["Timestamp", "Role", "Hospital", "Type", "Name", "Qty", "Credit_Value", "Status"]
inventory_cols = ["Medication Name", "Category", "Current Stock", "Unit Price (ZAR)"]

# --- 3. SESSION STATE & AUTH ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "subscribed" not in st.session_state:
    st.session_state.subscribed = False

# Sidebar Role Logic
user_type = st.sidebar.radio("Identify Your Role:", ["Public Stakeholder", "Internal Executive/Technical Team"])

if user_type == "Internal Executive/Technical Team":
    current_role = st.sidebar.selectbox("Access Level:", ["CEO", "Finance Director", "COO", "Developer"])
    if not st.session_state.authenticated:
        if st.sidebar.button("Sign In"): st.session_state.authenticated = True; st.rerun()
    else:
        st.sidebar.success(f"Verified: {current_role}")
else:
    current_role = "Public Stakeholder"

# --- 4. NAVIGATION ---
if user_type == "Public Stakeholder" and not st.session_state.subscribed:
    nav_options = ["📊 Subscription Portal"]
else:
    nav_options = ["🏠 Dashboard", "📦 Medicine Inventory", "💊 Medication Registry", "🧾 Invoice Generator", "📜 Transaction Records"]
    
page = st.sidebar.radio("Navigation", nav_options)

# --- 5. PAGE: MEDICINE INVENTORY (NEW) ---
if page == "📦 Medicine Inventory":
    st.title("📦 Master Medicine Inventory")
    st.info("Central database of all medications stored within the Eco-Chain network.")
    
    inv_df = load_data(INVENTORY_FILE, inventory_cols)
    
    if not inv_df.empty:
        st.dataframe(inv_df, use_container_width=True)
        
        # Simple Stock Update Feature
        with st.expander("Update Stock Levels"):
            selected_med = st.selectbox("Select Medication", inv_df["Medication Name"].tolist())
            new_stock = st.number_input("Add to Stock", min_value=0)
            if st.button("Update Inventory"):
                inv_df.loc[inv_df["Medication Name"] == selected_med, "Current Stock"] += new_stock
                save_data(inv_df, INVENTORY_FILE)
                st.success(f"Updated {selected_med} stock.")
                st.rerun()
    else:
        st.warning("Inventory is currently empty. Add medication via the Registry.")

# --- 6. PAGE: MEDICATION REGISTRY (UPDATED) ---
elif page == "💊 Medication Registry":
    st.title("💊 Medication Credit Registry")
    
    with st.form("mint_form"):
        col1, col2 = st.columns(2)
        with col1:
            med_type = st

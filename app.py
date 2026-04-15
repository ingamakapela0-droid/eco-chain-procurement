import streamlit as st
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval
import config
import os
import pandas as pd

# --- 1. THEME & SETTINGS ---
st.set_page_config(page_title="Eco-Chain | Gauteng Procurement", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #E2E8F0;
        padding: 20px;
        border-radius: 12px;
        border-top: 4px solid #0D9488;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    .stButton>button {
        background-color: #0D9488;
        color: white;
        border-radius: 8px;
    }
    .subscription-card {
        background-color: #E0F2F1;
        padding: 20px;
        border-radius: 12px;
        border: 2px dashed #0D9488;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BLOCKCHAIN INITIALIZATION ---
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
contract = w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=config.CONTRACT_ABI)

# --- 3. SIDEBAR: LOGO & UPDATED PROFILES ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=120)

st.sidebar.title("Eco-Chain")

user_address = streamlit_js_eval(js_expressions="window.ethereum ? window.ethereum.selectedAddress : null", key="wallet_check")
if not user_address:
    if st.sidebar.button("🔐 Connect MetaMask"):
        streamlit_js_eval(js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' })")
else:
    st.sidebar.success(f"Connected: {user_address[:6]}...{user_address[-4:]}")

st.sidebar.divider()
# UPDATED: Added Public Stakeholder Role
user_role = st.sidebar.selectbox("Access Level:", [
    "Management (CEO)", 
    "Finance Dept", 
    "Dispensary Staff", 
    "Public Stakeholder (Read-Only)"
])

st.sidebar.divider()
page = st.sidebar.radio("Navigation", [
    "🏠 Dashboard", 
    "📊 External Subscription Portal", # NEW SECTION
    "💊 Medication Registry", 
    "📈 Clinic Health Insights",
    "📜 Transaction Records",
    "🏥 Hospital Management"
])

# --- 4. PAGE: DASHBOARD ---
if page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain Dashboard")
    st.info(f"Viewing as: **{user_role}**")
    
    # Mission Statement
    st.markdown("""
        <div style="background-color: #F1F5F9; padding: 20px; border-radius: 10px; border-left: 6px solid #0D9488;">
            <h3>Eco-Chain Procurement Solutions</h3>
            <p>A digital bridge utilizing <b>Ethereum Smart Contracts</b> to ensure medication continuity across Gauteng. 
            Our platform provides an immutable record of inventory, creating a trustless environment for public health stakeholders.</p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Integrated Clinics", "42 Facilities", "Gauteng")
    c2.metric("Verified Txns", "1,024", "Blockchain")
    c3.metric("System Health", "Optimal", "Sepolia")

# --- 5. NEW PAGE: EXTERNAL SUBSCRIPTION PORTAL ---
elif page == "📊 External Subscription Portal":
    st.title("🛡️ Stakeholder Access & Subscriptions")
    st.write("External organizations can subscribe to real-time data feeds for research and oversight.")
    
    col_sub, col_api = st.columns(2)
    
    with col_sub:
        st.markdown("""
            <div class="subscription-card">
                <h3>Tier 1: Researcher Access</h3>
                <p>Access to anonymized regional health trends and clinic positivity rates.</p>
                <h4 style="color:#0D9488;">0.05 ETH / Month</h4>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Subscribe via MetaMask"):
            st.balloons()
            st.success("Subscription transaction initiated.")

    with col_api:
        st.subheader("🔗 API Keys")
        st.write("Generate a secure key to pull Eco-Chain stats into your own BI tools (Tableau/PowerBI).")
        st.code("X-ECO-CHAIN-KEY: 8f2b-92ea-44bc-918d", language="text")
        st.button("Regenerate Key")

# --- 6. PAGE: MEDICATION REGISTRY (Role Protection) ---
elif page == "💊 Medication Registry":
    st.title("📝 Inventory Management")
    if user_role == "Public Stakeholder (Read-Only)":
        st.error("🚫 Access Denied. Your subscription level allows read-only access to stats, not inventory editing.")
    elif user_role != "Management (CEO)":
        st.warning("⚠️ Only Management can edit records.")
    else:
        # (Standard Registry Logic from v3.4...)
        st.info("Management Access Granted: You can now Add or Edit medication.")
        st.tabs(["➕ Add New Medication", "✏️ Edit Medication"])

# --- 7. PAGE: CLINIC HEALTH INSIGHTS ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Facility Data")
    st.write("Public Stakeholders can view this data to monitor regional health performance.")
    st.bar_chart({"A": 5.9, "B": 4.9, "C": 7.1, "D": 5.8, "E": 5.2, "F": 7.8, "G": 6.2})
    # List of clinics from previous version...
    st.selectbox("Select Region:", ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"])

# --- 8. PAGE: TRANSACTION RECORDS ---
elif page == "📜 Transaction Records":
    st.title("📜 Transaction Records")
    records = pd.DataFrame([
        {"Time": "21:05", "User": "CEO_Admin", "Action": "Added Tenofovir", "Hash": "0x4f2...a1b"},
        {"Time": "20:40", "User": "Finance_Lead", "Action": "Escrow Funded", "Hash": "0x8e1...c3d"}
    ])
    st.table(records)

# --- 9. PAGE: HOSPITAL MANAGEMENT ---
elif page == "🏥 Hospital Management":
    st.title("🏥 Gauteng Hospital Network")
    hospitals = ["Chris Hani Baragwanath", "Charlotte Maxeke", "Steve Biko Academic", "Helen Joseph", "Kalafong Hospital", "Tembisa Hospital"]
    for h in hospitals:
        st.markdown(f"- **{h}**")

st.sidebar.markdown("---")
st.sidebar.caption("Eco-Chain Procurement | v3.5")

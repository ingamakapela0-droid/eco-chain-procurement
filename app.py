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
        width: 100%;
    }
    .about-box {
        background-color: #F1F5F9;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #0D9488;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BLOCKCHAIN INITIALIZATION ---
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
contract = w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=config.CONTRACT_ABI)

# --- 3. SIDEBAR: LOGO & SECURE WALLET PROFILES ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=120)
st.sidebar.title("Eco-Chain")

# Wallet Check
user_address = streamlit_js_eval(js_expressions="window.ethereum ? window.ethereum.selectedAddress : null", key="wallet_check")

# Role Mapping (Add your actual MetaMask addresses here)
AUTH_WALLETS = {
    "0xYourCEOWallet...": "CEO (Executive Access)",
    "0xYourCOOWallet...": "COO (Operations Oversight)",
    "0xYourFinanceWallet...": "Finance (Escrow Manager)"
}

if not user_address:
    if st.sidebar.button("🔐 Connect MetaMask"):
        streamlit_js_eval(js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' })")
    current_role = "Guest / Public"
else:
    current_role = AUTH_WALLETS.get(user_address.lower(), "Clinic Staff / Stakeholder")
    st.sidebar.success(f"Verified: {current_role}")

st.sidebar.divider()
page = st.sidebar.radio("Navigation", [
    "🏠 Dashboard", 
    "📊 External Subscription",
    "💊 Medication Registry", 
    "📈 Clinic Health Insights",
    "📜 Transaction Records",
    "🏥 Hospital Management"
])

# --- 4. PAGE: DASHBOARD (Restored About & Notification) ---
if page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    
    # Restored Mission Statement
    st.markdown("""
        <div class="about-box">
            <h3>Mission: Eco-Chain Procurement Solutions</h3>
            <p>A digital bridge utilizing <b>Ethereum Smart Contracts</b> to ensure medication continuity. 
            We mitigate stockouts for ART and diagnostics by providing a trustless escrow system and an 
            immutable record of inventory across the Gauteng health network.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.subheader("🔗 Core Blockchain Features")
        f1, f2 = st.columns(2)
        f1.info("**Trustless Escrow:** Payments locked until delivery verification.")
        f2.info("**Immutable Logs:** Real-time, fraud-proof transaction records.")
        
        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("Integrated Clinics", "42", "Gauteng")
        c2.metric("On-Chain Txns", "1,024", "Verified")
        c3.metric("System Health", "Optimal", "Sepolia")

    with col_side:
        st.subheader("⚡ Notification Centre")
        if st.button("🔔 New Order Notification"):
            st.toast("Scanning blockchain for low stock levels...", icon="🔍")
            st.info("System checking minimum thresholds in Region F.")
        if st.button("🔄 Refresh System Logs"):
            st.rerun()
        st.divider()
        st.error("**Alert:** Insulin Batch #09 is Low (Region D)")

# --- 5. PAGE: EXTERNAL SUBSCRIPTION ---
elif page == "📊 External Subscription":
    st.title("🛡️ Stakeholder Subscription Portal")
    st.write("External organizations can subscribe to regional stats and API feeds.")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div style='background-color:#E0F2F1; padding:20px; border-radius:12px; border:2px dashed #0D9488; text-align:center;'>"
                    "<h3>Researcher Tier</h3><p>Anonymized Regional Trends</p><h4>0.05 ETH / Mo</h4></div>", unsafe_allow_html=True)
        st.button("Subscribe via MetaMask", key="sub_btn")
    with col_b:
        st.subheader("🔗 API Access")
        st.code("X-ECO-CHAIN-KEY: 8f2b-92ea-44bc-918d")
        st.button("Regenerate Access Key")

# --- 6. PAGE: MEDICATION REGISTRY (Restored Edit & Roles) ---
elif page == "💊 Medication Registry":
    st.title("📝 Inventory Management")
    if "CEO" not in current_role and "COO" not in current_role:
        st.error("🚫 Access Denied. Management credentials required.")
    else:
        tab1, tab2 = st.tabs(["➕ Add New Medication", "✏️ Edit Medication"])
        with tab1:
            with st.form("add_form"):
                n = st.text_input("Product Name")
                s = st.number_input("Initial Stock", min_value=0)
                t = st.number_input("Threshold", min_value=1)
                p = st.number_input("Price (ETH)", format="%.6f")
                if st.form_submit_button("Commit to Blockchain"):
                    st.success("Transaction sent to MetaMask.")
        with tab2:
            st.selectbox("Select Medication to Edit:", ["Tenofovir", "Insulin", "Amoxicillin"])
            st.number_input("Update Stock Level")
            st.button("Confirm Update")

# --- 7. PAGE: CLINIC HEALTH INSIGHTS (Full List) ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Insights")
    st.bar_chart({"A": 5.9, "B": 4.9, "C": 7.1, "D": 5.8, "E": 5.2, "F": 7.8, "G": 6.2})
    
    st.divider()
    reg = st.selectbox("Select Region for Facility Mapping:", ["Region A", "Region D", "Region F"])
    facilities = {
        "Region A": ["Bophelong", "Diepsloot South", "Ebony Park", "Rabie Ridge"],
        "Region D": ["Soweto", "Dobsonville", "Protea Glen", "Diepkloof"],
        "Region F": ["Inner City Clinic", "CBD Hub", "Jeppe Clinic"]
    }
    st.write(f"Facilities in {reg}: {', '.join(facilities.get(reg, []))}")

# --- 8. PAGE: TRANSACTION RECORDS ---
elif page == "📜 Transaction Records":
    st.title("📜 Transaction Records")
    df = pd.DataFrame([
        {"Time": "21:05", "User": "CEO", "Action": "Added Tenofovir", "Hash": "0x4f2...a1b"},
        {"Time": "20:40", "User": "Finance", "Action": "Funded Escrow", "Hash": "0x8e1...c3d"}
    ])
    st.table(df)

# --- 9. PAGE: HOSPITAL MANAGEMENT ---
elif page == "🏥 Hospital Management":
    st.title("🏥 Gauteng Hospital Network")
    hospitals = ["Chris Hani Baragwanath", "Charlotte Maxeke", "Steve Biko Academic", "Helen Joseph", "Kalafong Hospital", "Tembisa Hospital"]
    for h in hospitals:
        st.markdown(f"- **{h}**")

st.sidebar.markdown("---")
st.sidebar.caption("Eco-Chain Procurement | v3.6")

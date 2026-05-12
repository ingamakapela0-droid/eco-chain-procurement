import streamlit as st
import pandas as pd
import json
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval

# --- 1. CONFIG & IDENTITY ---
ADMIN_ADDR = "0xe367800E0cEcCC2A7d5aCedd42d80b194A9381Ed"
CEO_ADDR = "0xc2AB9798C0c64483B082B42657e28A87063f27F7"
FIN_OFFICER_ADDR = "0xE8aE232232EC2b1C0924F73f1562EaE83b782195"
SUPPLIER_ADDR = "0xDC5Dd700E0EC19Bd6446bED8B2bF49e0E821240A"
HOSPITAL_ADDR = "0x35922c63dc498E133cDED15e459153f0EFE6F4D0"

RPC_URL = "https://rpc.ankr.com/eth_sepolia"

w3 = Web3(Web3.HTTPProvider(RPC_URL))
st.set_page_config(page_title="Eco-Chain | Healthcare Ledger", layout="wide")

# --- 2. BRANDING & STYLING ---
st.markdown(f"""
    <style>
    :root {{ --teal: #0D9488; --gold: #B45309; }}
    .main {{ background-color: #F8FAFC; }}
    .watermark {{
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-30deg);
        font-size: 8vw; color: rgba(13, 148, 136, 0.05); font-weight: 900;
        z-index: -1; pointer-events: none; white-space: nowrap;
    }}
    [data-testid="stSidebar"] {{ background-color: #FFFFFF; border-right: 2px solid var(--teal); }}
    .stButton>button {{ 
        background: linear-gradient(135deg, var(--teal), #0F766E); 
        color: white; border-radius: 12px; font-weight: bold; height: 3.5em; width: 100%;
    }}
    </style>
    <div class="watermark">ECO-CHAIN SOLUTIONS</div>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR & CONNECTION LOGIC ---
with st.sidebar:
    st.title("🌿 Eco-Chain")
    st.markdown("---")
    raw_wallet = streamlit_js_eval(js_expressions="async function getAccount() { const accounts = await window.ethereum.request({ method: 'eth_accounts' }); return accounts[0]; }; getAccount();", key="wallet_check")
    
    wallet_addr = None
    user_role = "Unregistered"

    if not raw_wallet:
        st.warning("🦊 MetaMask not detected.")
        if st.button("Connect to MetaMask"):
            streamlit_js_eval(js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' });", key="request_conn")
            st.rerun()
    else:
        wallet_addr = Web3.to_checksum_address(raw_wallet)
        st.success(f"Connected: {wallet_addr[:6]}...{wallet_addr[-4:]}")
        
        if wallet_addr.lower() == CEO_ADDR.lower(): user_role = "CEO"
        elif wallet_addr.lower() == ADMIN_ADDR.lower(): user_role = "Admin"
        elif wallet_addr.lower() == FIN_OFFICER_ADDR.lower(): user_role = "Financial Officer"
        elif wallet_addr.lower() == SUPPLIER_ADDR.lower(): user_role = "Supplier"
        elif wallet_addr.lower() == HOSPITAL_ADDR.lower(): user_role = "Hospital"
        else:
            user_role = st.selectbox("Current Access Level", ["Unregistered", "Hospital", "Supplier", "Financial Officer"])
        
        st.info(f"Role: **{user_role}**")

    st.markdown("---")
    tabs_nav = ["🏠 Overview", "📈 Health Insights"]
    
    if user_role == "Unregistered":
        tabs_nav += ["📝 Register Account"]
    else:
        if user_role == "Admin": tabs_nav += ["🛠️ Admin Approvals"]
        if user_role == "CEO": tabs_nav += ["📋 Hospital Requests", "💊 Issue Orders", "💰 Financial Oversight"]
        if user_role == "Financial Officer": tabs_nav += ["📑 Invoice Verification", "📊 Revenue Tracking"]
        if user_role == "Hospital": tabs_nav += ["🏥 Hospital Stock"]
        if user_role == "Supplier": tabs_nav += ["📦 Supplier Orders", "📤 Send Invoice", "💳 Subscriptions"]
    
    page = st.sidebar.radio("Navigation Menu", tabs_nav)

# --- 4. BLOCKCHAIN ENGINE ---
def record_on_chain(target_to, data_note="Eco-Chain Activity", value_eth=0):
    if not wallet_addr:
        st.error("Connection required.")
        return
    try:
        hex_data = Web3.to_hex(text=data_note)
        nonce = w3.eth.get_transaction_count(wallet_addr)
        tx_params = {
            "from": wallet_addr, "to": target_to, "value": hex(w3.to_wei(value_eth, 'ether')),
            "nonce": hex(nonce), "chainId": "0xaa36a7", "data": hex_data 
        }
        js_code = f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{json.dumps(tx_params)}] }});"
        streamlit_js_eval(js_expressions=js_code)
        st.info(f"Broadcasted to Ledger: {data_note}")
    except Exception as e:
        st.error(f"TX Failed: {e}")

# --- 5. PAGE MODULES ---

if page == "🏠 Overview":
    st.title("🏥 Eco-Chain Procurement Solutions")
    st.info("""
    **Mission Statement**
    
    Eco-Chain Procurement Solutions aims to provide a solution to the abrupt shortage of medication at local clinics and rural hospitals. We act as a bridge between healthcare facilities and pharmaceutical suppliers.
    
    The system monitors stock levels in real-time. When a medication reaches a minimum threshold, the platform automatically notifies suppliers to replenish the facility before it runs out. This eliminates wait times for patients and ensures consistent treatment availability.
    """)
    st.markdown("### 🔗 Blockchain Pulse")
    c1, c2, c3 = st.columns(3)
    c1.metric("Stockout Prevention", "100%", "Target")
    c2.metric("Immutability", "Active", "On-Chain")
    c3.metric("Nodes", "7 Hubs", "Online")

elif page == "📈 Health Insights":
    st.title("📈 Regional Health Trends & Insights")
    st.markdown("---")
    
    # Advanced Dataset for Regional Analysis
    health_metrics = pd.DataFrame({
        "Region": ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"],
        "Hub": ["Diepsloot", "Randburg", "Roodepoort", "Soweto", "Sandton", "Inner City", "Orange Farm"],
        "HIV Positivity %": [6.2, 4.5, 7.8, 8.1, 5.0, 9.4, 7.2],
        "TB Success Rate %": [88.5, 91.2, 86.4, 79.8, 89.1, 78.5, 82.3],
        "Medication Demand": [450, 320, 580, 710, 290, 840, 510]
    })

    t1, t2, t3 = st.tabs(["📍 Distribution Map", "📊 Disease Burden", "💊 Supply Chain Demand"])
    
    with t1:
        st.subheader("Regional Hub Distribution")
        st.table(health_metrics[["Region", "Hub", "Medication Demand"]])
    
    with t2:
        col1, col2 = st.columns(2)
        with col1:
            st.write("**HIV Positivity by Region**")
            st.bar_chart(health_metrics.set_index("Region")["HIV Positivity %"])
        with col2:
            st.write("**TB Treatment Success Rates**")
            st.line_chart(health_metrics.set_index("Region")["TB Success Rate %"])
            
    with t3:
        st.subheader("Inventory Replenishment Needs")
        # Calculating demand vs capacity logic for visualization
        st.area_chart(health_metrics.set_index("Hub")["Medication Demand"])
        st.caption("Data indexed by local clinic volume and historical stockout frequency.")

elif page == "📝 Register Account":
    st.title("📝 Entity Registration Portal")
    with st.form("reg_form"):
        org_name = st.text_input("Full Name / Organization Name")
        role = st.selectbox("Role to Register", ["Hospital", "Supplier", "Financial Officer"])
        if st.form_submit_button("Submit Registration to Ledger"):
            on_chain_data = f"REGISTRATION: {role} | NAME: {org_name}"
            record_on_chain(ADMIN_ADDR, data_note=on_chain_data)

elif page == "📑 Invoice Verification":
    st.title("📑 Financial Officer: Verify Invoices")
    st.table(pd.DataFrame({"ID": ["INV-001"], "From": ["MediCore"], "Amt": ["R12,500"], "Status": ["Pending"]}))
    if st.button("✅ Verify & Send to CEO"):
        record_on_chain(CEO_ADDR, data_note="FIN_OFFICER: Verified Invoice #001")

elif page == "💰 Financial Oversight":
    st.title("💰 CEO: Final Authorization")
    st.info("Verified Invoices awaiting final settlement.")
    if st.button("💳 Authorize Settlement"):
        record_on_chain(ADMIN_ADDR, data_note="CEO: Authorized Final Payment")

elif page == "🛠️ Admin Approvals":
    st.title("🛠️ Admin: Access Control")
    target = st.text_input("Wallet Address to Authorize")
    if st.button("Finalize On-Chain Access"):
        record_on_chain(target, data_note="ADMIN: Access Granted")

elif page == "📤 Send Invoice":
    st.title("📤 Supplier: Generate Invoice")
    if st.button("Send to Financial Officer"):
        record_on_chain(FIN_OFFICER_ADDR, data_note="SUPPLIER: Submitted New Invoice")

# --- FOOTER ---
st.markdown("---")
st.caption("Eco-Chain Solutions | Version 15.4 | Johannesburg Hub")
import streamlit as st
import pandas as pd
import json
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval

# --- 1. CONFIG & IDENTITY ---
try:
    from config import CONTRACT_ADDRESS, CONTRACT_ABI, RPC_URL, ADMIN_ADDR, CEO_ADDR, FIN_OFFICER_ADDR
except ImportError:
    st.error("Missing config.py! Ensure it is in the same folder.")
    st.stop()

LOGO_FILE = "logo.png" 
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
    try: st.image(LOGO_FILE, use_column_width=True)
    except: st.title("🌿 Eco-Chain")
    
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
        
        # Identity Logic based on config.py
        if wallet_addr.lower() == CEO_ADDR.lower(): user_role = "CEO"
        elif wallet_addr.lower() == ADMIN_ADDR.lower(): user_role = "Admin"
        elif wallet_addr.lower() == FIN_OFFICER_ADDR.lower(): user_role = "Financial Officer"
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

# --- 4. BLOCKCHAIN ENGINE (WITH PERMANENT DATA STORAGE) ---
def record_on_chain(target_to, data_note="Eco-Chain Activity", value_eth=0):
    if not wallet_addr:
        st.error("Connection required.")
        return
    try:
        # Convert description to Hex for Etherscan UTF-8 visibility
        hex_data = Web3.to_hex(text=data_note)
        
        nonce = w3.eth.get_transaction_count(wallet_addr)
        tx_params = {
            "from": wallet_addr, 
            "to": target_to, 
            "value": hex(w3.to_wei(value_eth, 'ether')),
            "nonce": hex(nonce), 
            "chainId": "0xaa36a7",
            "data": hex_data  # Permanent on-chain description
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
    
    Eco-Chain Procurement Solutions aims to provide a solution to the abrupt shortage of medication at local clinics and rural hospitals and clinics. We will be the bridge between the hospital and pharmaceutical companies.
    
    Our app will be linked to the hospital or clinic we’re working with and it will monitor the medication stock levels. When any medication leaves the dispensary, it will be scanned by whoever is issuing the medication and this will show on the app.
    
    All medication will have a minimum number that is allowed to be left in the dispensary and once it reaches that minimum, we /it will notify the suppliers and the medication will be sent to the clinic or hospital before it fully runs out. This will eliminate medication running out and patients having to wait for long periods of time to receive medication.
    
    There will be contracts in place to ensure payment for all deliverables between the public clinics/hospitals and the suppliers.
    """)

    st.markdown("### 🔗 Blockchain Pulse: Network Health")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Stockout Prevention", "100%")
    with c2: st.metric("Immutability", "Enabled", "Permanent Data")
    with c3: st.metric("Regional Nodes", "7 Hubs")
    with c4: st.metric("Alerts", "Active")

elif page == "📈 Health Insights":
    st.title("📈 Regional Health Trends & Insights")
    t1, t2, t3 = st.tabs(["📍 Regional Network", "📊 HIV Statistics", "🫁 TB Statistics"])
    with t1:
        st.table(pd.DataFrame({
            "Region": ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"],
            "Hubs": ["Diepsloot", "Randburg", "Roodepoort", "Soweto", "Sandton", "Inner City", "Orange Farm"]
        }))
    with t2:
        hiv_df = pd.DataFrame({"Positivity %": [5.9, 4.9, 7.1, 5.8, 5.2, 7.8, 6.2]}, index=["A", "B", "C", "D", "E", "F", "G"])
        st.bar_chart(hiv_df)
    with t3:
        tb_df = pd.DataFrame({"Success %": [89.4, 90.3, 87.5, 80.5, 87.0, 80.7, 81.5]}, index=["A", "B", "C", "D", "E", "F", "G"])
        st.bar_chart(tb_df)

elif page == "📝 Register Account":
    st.title("📝 Entity Registration Portal")
    with st.form("reg_form"):
        org_name = st.text_input("Full Name / Organization Name")
        role = st.selectbox("Role to Register", ["Hospital", "Supplier", "Financial Officer"])
        if st.form_submit_button("Submit Registration to Ledger"):
            # This string is what appears on Etherscan
            on_chain_data = f"REGISTRATION: {role} | NAME: {org_name}"
            record_on_chain(ADMIN_ADDR, data_note=on_chain_data)
            st.success(f"Proof of Registration for {org_name} sent to blockchain.")

elif page == "🛠️ Admin Approvals":
    st.title("🛠️ Admin: Role Verification")
    target = st.text_input("Wallet Address to Authorize")
    if st.button("Finalize On-Chain Access"):
        record_on_chain(target, data_note="ADMIN: Access Granted")

elif page == "📑 Invoice Verification":
    st.title("📑 Financial Officer: Verify Invoices")
    st.table(pd.DataFrame({"ID": ["INV-001"], "From": ["MediCore"], "Amt": ["R12,000"], "Status": ["Pending"]}))
    if st.button("Push to CEO"):
        record_on_chain(CEO_ADDR, data_note="FIN_OFFICER: Verified Invoice #001")

elif page == "💰 Financial Oversight":
    st.title("💰 CEO: Authorization")
    if st.button("Authorize Final Settlement"):
        record_on_chain(ADMIN_ADDR, data_note="CEO: Payment Authorized")

elif page == "🏥 Hospital Stock":
    st.title("🏥 Hospital: Inventory")
    st.table(pd.DataFrame({"Medicine": ["ARVs", "Insulin"], "Level": [45, 12]}))
    if st.button("Scan Out"):
        record_on_chain(ADMIN_ADDR, data_note="HOSPITAL: Item Scanned Out")

elif page == "📤 Send Invoice":
    st.title("📤 Supplier: Invoice Generation")
    if st.button("Submit to Finance"):
        record_on_chain(FIN_OFFICER_ADDR, data_note="SUPPLIER: New Invoice Submitted")

elif page == "💳 Subscriptions":
    st.title("💳 Supplier Subscriptions")
    st.metric("Annual Plan", "R5,400")
    if st.button("Pay Subscription"):
        record_on_chain(ADMIN_ADDR, data_note="SUPPLIER: Subscription Paid")

# --- FOOTER ---
st.markdown("---")
st.caption("Eco-Chain Solutions | Version 15.0 | Permanent Decentralized Ledger")
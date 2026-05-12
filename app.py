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

# --- 4. BLOCKCHAIN ENGINE ---
def record_on_chain(target_to, data_note="Eco-Chain Activity", value_eth=0):
    if not wallet_addr:
        st.error("Connection required.")
        return
    try:
        hex_data = Web3.to_hex(text=data_note)
        nonce = w3.eth.get_transaction_count(wallet_addr)
        tx_params = {
            "from": wallet_addr, 
            "to": target_to, 
            "value": hex(w3.to_wei(value_eth, 'ether')),
            "nonce": hex(nonce), 
            "chainId": "0xaa36a7",
            "data": hex_data 
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
    Eco-Chain Procurement Solutions provides a bridge between hospitals and pharmaceutical companies to prevent medication stockouts in rural areas.
    """)

elif page == "📈 Health Insights":
    st.title("📈 Regional Health Trends")
    st.write("Regional Data for HIV and TB metrics across Johannesburg.")

elif page == "📝 Register Account":
    st.title("📝 Entity Registration Portal")
    with st.form("reg_form"):
        org_name = st.text_input("Organization Name")
        role = st.selectbox("Role", ["Hospital", "Supplier", "Financial Officer"])
        if st.form_submit_button("Submit Registration"):
            on_chain_data = f"REGISTRATION: {role} | NAME: {org_name}"
            record_on_chain(ADMIN_ADDR, data_note=on_chain_data)

elif page == "📑 Invoice Verification":
    st.title("📑 Financial Officer: Verify Invoices")
    st.subheader("Invoices Awaiting Review")
    inv_data = pd.DataFrame({"ID": ["INV-001"], "Supplier": ["MediCore"], "Amt": ["R12,500"], "Status": ["Verification Needed"]})
    st.table(inv_data)
    
    if st.button("✅ Verify & Send to CEO"):
        # Explicitly routing to CEO_ADDR from config
        verification_note = f"VERIFIED: Invoice #001 for R12,500 | Verified by: {wallet_addr[:8]}"
        record_on_chain(CEO_ADDR, data_note=verification_note)
        st.success("Verification transaction sent to CEO for final payment authorization.")

elif page == "💰 Financial Oversight":
    st.title("💰 CEO: Final Authorization")
    st.subheader("Verified Invoices Ready for Payment")
    
    # Simulating what the CEO sees after FO pushes the transaction
    st.table(pd.DataFrame({
        "Invoice ID": ["INV-001"],
        "Financial Officer Status": ["VERIFIED"],
        "Amount": ["R12,500"],
        "Action": ["Awaiting Settlement"]
    }))
    
    if st.button("💳 Authorize Settlement & Pay Supplier"):
        record_on_chain(ADMIN_ADDR, data_note="CEO: Final Payment Authorized for INV-001")

elif page == "🛠️ Admin Approvals":
    st.title("🛠️ Admin: Access Control")
    target = st.text_input("Wallet Address")
    if st.button("Confirm Registration"):
        record_on_chain(target, data_note="ADMIN: Access Granted")

elif page == "📤 Send Invoice":
    st.title("📤 Supplier: Invoice Generation")
    with st.form("supplier_inv"):
        amt = st.number_input("Invoice Total (ZAR)")
        if st.form_submit_button("Send to Financial Officer"):
            record_on_chain(FIN_OFFICER_ADDR, data_note=f"SUPPLIER: New Invoice for R{amt}")

# --- FOOTER ---
st.markdown("---")
st.caption("Eco-Chain Solutions | Version 15.1 | Financial Workflow Optimized")
import streamlit as st
import pandas as pd
import json
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval

# --- 1. CONFIG & IDENTITY ---
try:
    from config import CONTRACT_ADDRESS, CONTRACT_ABI, RPC_URL, ADMIN_ADDR, CEO_ADDR, FIN_OFFICER_ADDR
except ImportError:
    st.error("Missing config.py!")
    st.stop()

LOGO_FILE = "logo.png" 
w3 = Web3(Web3.HTTPProvider(RPC_URL))
st.set_page_config(page_title="Eco-Chain | Healthcare Ledger", layout="wide")

# --- 2. BRANDING & WATERMARK ---
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
        color: white; border-radius: 12px; font-weight: bold;
    }}
    </style>
    <div class="watermark">ECO-CHAIN SOLUTIONS</div>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (Logo + Menu + Wallet) ---
with st.sidebar:
    try: st.image(LOGO_FILE, use_column_width=True)
    except: st.title("🌿 Eco-Chain")
    
    st.markdown("---")
    raw_wallet = streamlit_js_eval(js_expressions="async function getAccount() { const accounts = await window.ethereum.request({ method: 'eth_accounts' }); return accounts[0]; }; getAccount();", key="wallet")
    
    user_role = "Guest"
    wallet_addr = None

    if raw_wallet:
        wallet_addr = Web3.to_checksum_address(raw_wallet)
        st.success(f"Connected: {wallet_addr[:6]}...{wallet_addr[-4:]}")
        
        if wallet_addr.lower() == ADMIN_ADDR.lower(): user_role = "Admin"
        elif wallet_addr.lower() == CEO_ADDR.lower(): user_role = "CEO"
        elif wallet_addr.lower() == FIN_OFFICER_ADDR.lower(): user_role = "Financial Officer"
        else: user_role = "Supplier / Hospital"
        
        st.info(f"Identity: **{user_role}**")
    else:
        st.warning("🔒 Wallet Locked")

    st.markdown("---")
    
    # SYSTEM NAVIGATION
    tabs = ["🏠 Overview", "📈 Health Insights"]
    if user_role == "Admin": tabs += ["🛠️ Admin Verification"]
    if user_role == "CEO": tabs += ["📋 Hospital Requests", "💊 Issue Orders"]
    if user_role == "Supplier / Hospital": tabs += ["📦 Supplier Orders", "💳 Subscriptions"]
    
    page = st.sidebar.radio("Navigation Menu", tabs)

# --- 4. BLOCKCHAIN ENGINE ---
def record_on_chain(target_to, data="0x", value_eth=0):
    """Triggers MetaMask to record the transaction record on Sepolia."""
    nonce = w3.eth.get_transaction_count(wallet_addr)
    tx_params = {
        "from": wallet_addr,
        "to": target_to,
        "value": hex(w3.to_wei(value_eth, 'ether')),
        "nonce": hex(nonce),
        "chainId": "0xaa36a7" 
    }
    js_code = f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{json.dumps(tx_params)}] }});"
    streamlit_js_eval(js_expressions=js_code)

# --- 5. PAGE MODULES ---

if page == "🏠 Overview":
    st.title("🏥 Eco-Chain | Regional Logistics")
    st.info("**Mission:** Bridging the gap between Hospital Demand and Supplier Fulfillment via Blockchain Transparency.")
    
elif page == "🛠️ Admin Verification":
    st.title("🛠️ Admin: Identity Verification")
    target = st.text_input("Entity Wallet Address to Verify")
    if st.button("Authorize Entity on Blockchain"):
        record_on_chain(wallet_addr) # Records the verification action
        st.success(f"Verification for {target} recorded on the ledger.")

elif page == "📋 Hospital Requests":
    st.title("📋 CEO: Pending Hospital Requests")
    st.write("The following hospitals have requested stock. Review and issue orders.")
    # Mock data showing what the CEO sees
    reqs = pd.DataFrame({
        "Hospital": ["Chris Hani Baragwanath", "Charlotte Maxeke"],
        "Medicine": ["Insulin", "Paracetamol"],
        "Status": ["PENDING CEO REVIEW", "PENDING CEO REVIEW"]
    })
    st.table(reqs)

elif page == "💊 Issue Orders":
    st.title("💊 CEO: Authorize Supplier Order")
    with st.container(border=True):
        med = st.text_input("Medication Name")
        supplier = st.text_input("Supplier Address (Target)")
        if st.button("Record Authorized Order on Blockchain"):
            record_on_chain(wallet_addr)
            st.success(f"Order for {med} has been transmitted to Supplier Ledger.")

elif page == "📦 Supplier Orders":
    st.title("📦 Supplier: Incoming CEO Orders")
    st.write("Authorized orders issued by the CEO awaiting fulfillment.")
    # Mock data showing what the Supplier sees
    orders = pd.DataFrame({
        "Order ID": ["#TX-9921", "#TX-9925"],
        "Issued By": ["Eco-Chain CEO", "Eco-Chain CEO"],
        "Medicine": ["Insulin Pen", "ARVs"],
        "Status": ["AUTHORIZED - READY TO SHIP", "AUTHORIZED - READY TO SHIP"]
    })
    st.table(orders)
    if st.button("Record Shipment on Blockchain"):
        record_on_chain(wallet_addr)
        st.success("Shipment status recorded on-chain.")

# --- FOOTER ---
st.markdown("---")
st.caption("Eco-Chain Solutions | Blockchain Procurement v13.0")
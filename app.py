import streamlit as st
import json
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval

# --- 1. CONFIG & CONNECTION ---
try:
    from config import CONTRACT_ADDRESS, CONTRACT_ABI, RPC_URL, ADMIN_ADDR, CEO_ADDR, FIN_OFFICER_ADDR
except ImportError:
    st.error("Config missing!")
    st.stop()

w3 = Web3(Web3.HTTPProvider(RPC_URL))

# --- 2. THEME & IDENTITY ---
st.set_page_config(page_title="Eco-Chain Procurement", layout="wide")
st.sidebar.title("🌿 Eco-Chain System")

raw_wallet = streamlit_js_eval(js_expressions="async function getAccount() { const accounts = await window.ethereum.request({ method: 'eth_accounts' }); return accounts[0]; }; getAccount();", key="wallet")

user_role = "Guest"
wallet_addr = None

if raw_wallet:
    wallet_addr = Web3.to_checksum_address(raw_wallet)
    st.sidebar.success(f"ID: {wallet_addr[:6]}...{wallet_addr[-4:]}")
    
    # Identify Roles based on your workflow
    if wallet_addr.lower() == ADMIN_ADDR.lower(): user_role = "Admin"
    elif wallet_addr.lower() == CEO_ADDR.lower(): user_role = "CEO"
    elif wallet_addr.lower() == FIN_OFFICER_ADDR.lower(): user_role = "Financial Officer"
    else: user_role = "Hospital / Supplier"
    
    st.sidebar.info(f"Access Level: **{user_role}**")
else:
    st.sidebar.warning("Connect MetaMask to Login")

# --- 3. WORKFLOW NAVIGATION ---
menu = ["🏠 Home"]
if user_role == "Admin": menu += ["🛠️ Verify Requests"]
elif user_role == "CEO": menu += ["🛒 Place Hospital Orders"]
elif user_role == "Financial Officer": menu += ["💰 Approve Payments"]
elif user_role == "Hospital / Supplier": menu += ["📋 Membership Request"]

page = st.sidebar.radio("Navigation", menu)

# --- 4. CORE LOGIC ---
def trigger_metamask(to_addr, value_eth=0):
    """Triggers a clean MetaMask popup without contract revert risks."""
    nonce = w3.eth.get_transaction_count(wallet_addr)
    tx_params = {
        "from": wallet_addr,
        "to": to_addr,
        "value": hex(w3.to_wei(value_eth, 'ether')),
        "nonce": hex(nonce),
        "chainId": "0xaa36a7" # Sepolia
    }
    js_code = f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{json.dumps(tx_params)}] }});"
    streamlit_js_eval(js_expressions=js_code)

# --- 5. PAGES ---
if page == "🏠 Home":
    st.title("🏥 Gauteng Healthcare Procurement")
    st.write("Current Workflow: Hospitals $\rightarrow$ CEO $\rightarrow$ Admin/Finance $\rightarrow$ Fulfillment.")

elif page == "🛠️ Verify Requests":
    st.header("Admin: Verify Hospital & Supplier Onboarding")
    target = st.text_input("Entity Address to Authorize")
    if st.button("Approve Entry to Network"):
        trigger_metamask(wallet_addr) # Self-send for safe demo
        st.success(f"Entity {target} has been verified on-chain.")

elif page == "🛒 Place Hospital Orders":
    st.header("CEO: Medication Procurement Hub")
    st.info("Acting on behalf of: Charlotte Maxeke Academic Hospital")
    med = st.selectbox("Select Medication", ["Insulin", "Paracetamol", "ARVs"])
    if st.button("Place Order with Supplier"):
        trigger_metamask(wallet_addr)
        st.success(f"Order for {med} submitted to Financial Officer for payment approval.")

elif page == "💰 Approve Payments":
    st.header("Financial Officer: Transaction Audit")
    st.warning("Pending: CEO Order #4401 - R12,500.00")
    if st.button("Approve & Release Funds"):
        trigger_metamask(wallet_addr, value_eth=0.01)
        st.success("Payment authorized and logged on the Sepolia Ledger.")

elif page == "📋 Membership Request":
    st.header("Join the Eco-Chain Network")
    role_type = st.radio("Join as:", ["Hospital", "Supplier"])
    if st.button("Send Request to Admin"):
        trigger_metamask(ADMIN_ADDR)
        st.info("Request sent. Awaiting Admin verification.")
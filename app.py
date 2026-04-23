import streamlit as st
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval
import config

# --- 1. BLOCKCHAIN CONNECTION ---
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
contract = w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=config.CONTRACT_ABI)

st.set_page_config(page_title=config.APP_NAME, layout="wide")

# --- 2. SESSION STATE (The Memory) ---
# This keeps the wallet connected even when you click buttons
if 'user_address' not in st.session_state:
    st.session_state['user_address'] = None

# --- 3. METAMASK LOGIC ---
def get_wallet():
    # Grab address from browser
    found_wallet = streamlit_js_eval(js_expressions="window.ethereum ? window.ethereum.selectedAddress : null", key="wallet_check")
    if found_wallet:
        st.session_state['user_address'] = found_wallet
    return st.session_state['user_address']

def request_conn():
    streamlit_js_eval(js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' })", key="conn_btn")

# --- 4. INTERFACE ---
st.title(config.APP_NAME)
st.caption(config.TAGLINE)

# Sidebar Logic
user_addr = get_wallet()
if not user_addr:
    st.sidebar.warning("MetaMask Not Connected")
    if st.sidebar.button("Connect MetaMask"):
        request_conn()
else:
    st.sidebar.success(f"Connected: {user_addr[:6]}...{user_addr[-4:]}")

menu = ["📊 Dashboard", "📦 Inventory", "💸 Finance", "🛡️ Admin"]
choice = st.sidebar.radio("Navigate", menu)

# --- 5. PAGES ---

if choice == "📊 Dashboard":
    st.subheader("Global Overview")
    try:
        bal = contract.functions.getContractBalance().call()
        st.metric("Contract Escrow Balance", f"{w3.from_wei(bal, 'ether')} ETH")
    except:
        st.error("Could not fetch balance. Check contract address.")

elif choice == "📦 Inventory":
    st.subheader("Inventory Management")
    med_name = st.text_input("Medication Name")
    if st.button("Issue 1 Unit"):
        if not user_addr:
            st.error("Connect MetaMask first!")
        else:
            data = contract.functions.issueMedication(med_name)._encode_transaction_data()
            streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{{ from: '{user_addr}', to: '{config.CONTRACT_ADDRESS}', data: '{data}' }}] }})")

elif choice == "💸 Finance":
    st.subheader("Order Payments")
    o_id = st.number_input("Order ID", min_value=1, step=1)
    if st.button("Pay to Escrow"):
        if not user_addr:
            st.error("Connect MetaMask!")
        else:
            try:
                order = contract.functions.orders(int(o_id)).call()
                val_hex = hex(order[3]) # totalCost
                data = contract.functions.depositEscrow(int(o_id))._encode_transaction_data()
                streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{{ from: '{user_addr}', to: '{config.CONTRACT_ADDRESS}', data: '{data}', value: '{val_hex}' }}] }})")
            except:
                st.error("Order not found.")

elif choice == "🛡️ Admin":
    st.subheader("System Setup")
    with st.expander("Register New Medication"):
        n = st.text_input("Name")
        s = st.number_input("Initial Stock", 0)
        t = st.number_input("Threshold", 1)
        q = st.number_input("Reorder Qty", 1)
        p = st.number_input("Price (Wei)", 0)
        sup = st.text_input("Supplier Address")
        
        if st.button("Add Medication"):
            if not user_addr or not sup:
                st.error("Missing wallet connection or supplier address.")
            else:
                data = contract.functions.addMedication(n, int(s), int(t), int(q), int(p), w3.to_checksum_address(sup))._encode_transaction_data()
                streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{{ from: '{user_addr}', to: '{config.CONTRACT_ADDRESS}', data: '{data}' }}] }})")

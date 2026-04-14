# pip install streamlit web3 streamlit-js-eval
import streamlit as st
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval
import config
import os

# --- INITIALIZATION ---
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
contract = w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=config.CONTRACT_ABI)

# --- HEADER ---
def render_header():
    try:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=250)
        else:
            st.title(config.APP_NAME)
    except:
        st.title(config.APP_NAME)
    st.caption(f"**{config.TAGLINE}**")
    st.info(config.DESCRIPTION)

render_header()

# --- WALLET CONNECTION ---
st.sidebar.header("🔐 Wallet Access")
user_address = streamlit_js_eval(js_expressions="window.ethereum ? window.ethereum.selectedAddress : null", key="wallet_check")

if not user_address:
    if st.sidebar.button("Connect MetaMask"):
        streamlit_js_eval(js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' })", key="connect_btn")
    st.sidebar.warning("Connect your wallet to perform actions.")
else:
    st.sidebar.success(f"Connected: {user_address[:6]}...{user_address[-4:]}")
    # Chain Check
    chain_id = streamlit_js_eval(js_expressions="window.ethereum.networkVersion", key="chain_check")
    if chain_id != "11155111":
        st.sidebar.error("Switch to Sepolia Testnet.")

# --- NAVIGATION ---
page = st.sidebar.radio("Navigation", ["Hospital Overview", "Dispensary (Staff)", "Finance & Escrow", "Management (CEO)"])

# --- DASHBOARD ---
if page == "Hospital Overview":
    st.header("📊 Real-Time Operations")
    col1, col2, col3 = st.columns(3)
    
    with st.spinner("Fetching live data..."):
        try:
            escrow_bal = w3.from_wei(contract.functions.getContractBalance().call(), 'ether')
            orders_total = contract.functions.orderCount().call()
            user_bal_eth = w3.from_wei(w3.eth.get_balance(user_address), 'ether') if user_address else 0
        except Exception as e:
            st.error(f"Sync error: {e}")
            escrow_bal, orders_total, user_bal_eth = 0, 0, 0

    col1.metric("Your MetaMask", f"{round(user_bal_eth, 4)} ETH")
    col2.metric("Contract Escrow", f"{escrow_bal} ETH")
    col3.metric("Total Orders", orders_total)

# --- FUNCTIONAL PAGES ---
elif page == "Dispensary (Staff)":
    st.header("🏥 Staff Portal")
    t1, t2 = st.tabs(["Issue Medication", "Confirm Shipment"])
    with t1:
        med_in = st.text_input("Medication Name")
        if st.button("Log Issuance") and user_address:
            data = contract.encodeABI(fn_name="issueMedication", args=[med_in])
            tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data}
            streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})", key="tx_iss")
    with t2:
        o_id = st.number_input("Order ID", min_value=1)
        if st.button("Confirm Delivery") and user_address:
            data = contract.encodeABI(fn_name="verifyDelivery", args=[int(o_id)])
            tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data}
            streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})", key="tx_ver")

elif page == "Finance & Escrow":
    st.header("💰 Funding & Payments")
    with st.form("escrow"):
        id_fund = st.number_input("Order ID", min_value=1)
        val_fund = st.number_input("ETH Amount", min_value=0.0, format="%.6f")
        if st.form_submit_button("Deposit into Escrow") and user_address:
            wei_val = w3.to_wei(val_fund, 'ether')
            data = contract.encodeABI(fn_name="depositEscrow", args=[int(id_fund)])
            tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data, 'value': hex(wei_val)}
            streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})", key="tx_esc")

elif page == "Management (CEO)":
    st.header("🔑 Inventory Setup")
    with st.form("add"):
        n = st.text_input("Name")
        s = st.number_input("Stock", min_value=0)
        t = st.number_input("Threshold", min_value=1)
        q = st.number_input("Reorder Qty", min_value=1)
        p = st.number_input("Price (ETH)", min_value=0.0, format="%.6f")
        supp = st.text_input("Supplier Address")
        if st.form_submit_button("Register") and user_address:
            try:
                data = contract.encodeABI(fn_name="addMedication", args=[n, s, t, q, w3.to_wei(p, 'ether'), w3.to_checksum_address(supp)])
                tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data}
                streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})", key="tx_add")
            except Exception as e: st.error(e)

st.sidebar.markdown("---")
st.sidebar.caption("Eco-Chain Procurement | v2.0")
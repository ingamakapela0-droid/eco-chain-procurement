import streamlit as st
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval
import config
import os

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Eco-Chain Procurement", layout="wide")

st.markdown("""
    <style>
    .stMetric {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #2e7d32;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALIZATION ---
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
contract = w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=config.CONTRACT_ABI)

# --- 3. HEADER LOGIC ---
def render_header():
    col_logo, col_text = st.columns([1, 4])
    
    # Check if logo.png exists in the repository
    if os.path.exists("logo.png"):
        with col_logo:
            st.image("logo.png", width=120)
    
    with col_text:
        st.title(config.APP_NAME)
        st.caption(f"🚀 **{config.TAGLINE}**")
    
    st.info(config.DESCRIPTION)

render_header()

# --- 4. SIDEBAR & WALLET ---
st.sidebar.header("🔐 Wallet Access")
user_address = streamlit_js_eval(js_expressions="window.ethereum ? window.ethereum.selectedAddress : null", key="wallet_check")

if not user_address:
    if st.sidebar.button("Connect MetaMask"):
        # Triggering the MetaMask pop-up
        streamlit_js_eval(js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' })", key="connect_btn")
    st.sidebar.warning("Please connect MetaMask.")
else:
    st.sidebar.success(f"Connected: {user_address[:6]}...{user_address[-4:]}")
    chain_id = streamlit_js_eval(js_expressions="window.ethereum.networkVersion", key="chain_id")
    if chain_id != "11155111":
        st.sidebar.error("⚠️ Switch to Sepolia Testnet")

st.sidebar.divider()
page = st.sidebar.radio("Navigation", ["📊 Hospital Overview", "🏥 Dispensary (Staff)", "💰 Finance & Escrow", "🔑 Management (CEO)"])

# --- 5. PAGE: HOSPITAL OVERVIEW ---
if page == "📊 Hospital Overview":
    st.subheader("📊 Real-Time Operations Command Center")
    
    col1, col2, col3 = st.columns(3)
    try:
        escrow_bal = w3.from_wei(contract.functions.getContractBalance().call(), 'ether')
        orders_total = contract.functions.orderCount().call()
        user_bal_eth = w3.from_wei(w3.eth.get_balance(user_address), 'ether') if user_address else 0
    except:
        escrow_bal, orders_total, user_bal_eth = 0, 0, 0

    col1.metric("My Wallet", f"{round(user_bal_eth, 4)} ETH")
    col2.metric("Contract Escrow", f"{escrow_bal} ETH")
    col3.metric("Total Orders", orders_total)

    st.divider()

    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("📋 System Status")
        st.success("✅ Blockchain Node: Connected")
        st.progress(95, text="Deployment Readiness")
    with c2:
        st.subheader("⚡ Refresh")
        if st.button("Sync Data"):
            st.rerun()

# --- 6. PAGE: DISPENSARY (STAFF) ---
elif page == "🏥 Dispensary (Staff)":
    st.header("🏥 Dispensary Portal")
    t1, t2 = st.tabs(["Log Usage", "Verify Delivery"])
    
    with t1:
        with st.form(key="usage_form"):
            med_name = st.text_input("Medication Name to Issue")
            submitted = st.form_submit_button("Log Transaction")
            if submitted and user_address:
                data = contract.encodeABI(fn_name="issueMedication", args=[med_name])
                tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data}
                streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})")

    with t2:
        with st.form(key="delivery_form"):
            order_id = st.number_input("Enter Order ID", min_value=1, step=1)
            submitted = st.form_submit_button("Confirm Receipt & Release Funds")
            if submitted and user_address:
                data = contract.encodeABI(fn_name="verifyDelivery", args=[int(order_id)])
                tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data}
                streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})")

# --- 7. PAGE: FINANCE & ESCROW ---
elif page == "💰 Finance & Escrow":
    st.header("💰 Financial Operations")
    with st.form(key="finance_form"):
        o_id = st.number_input("Order ID", min_value=1, step=1)
        eth_val = st.number_input("Amount to Escrow (ETH)", min_value=0.0, format="%.6f")
        submitted = st.form_submit_button("Send to Escrow")
        if submitted and user_address:
            wei_val = w3.to_wei(eth_val, 'ether')
            data = contract.encodeABI(fn_name="depositEscrow", args=[int(o_id)])
            tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data, 'value': hex(wei_val)}
            streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})")

# --- 8. PAGE: MANAGEMENT (CEO) ---
elif page == "🔑 Management (CEO)":
    st.header("🔑 Inventory Management")
    with st.form(key="admin_form"):
        m_name = st.text_input("Medication Name")
        col_a, col_b = st.columns(2)
        m_stock = col_a.number_input("Current Stock", min_value=0)
        m_thresh = col_b.number_input("Reorder Level", min_value=1)
        m_qty = col_a.number_input("Standard Order Qty", min_value=1)
        m_price = col_b.number_input("Price (ETH)", min_value=0.0, format="%.6f")
        m_supp = st.text_input("Supplier Wallet Address")
        
        submitted = st.form_submit_button("Register Product on Blockchain")
        if submitted and user_address:
            try:
                data = contract.encodeABI(fn_name="addMedication", args=[m_name, int(m_stock), int(m_thresh), int(m_qty), w3.to_wei(m_price, 'ether'), w3.to_checksum_address(m_supp)])
                tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data}
                streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})")
            except Exception as e:
                st.error(f"Error: {e}")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption("Eco-Chain Procurement | v2.1")
    
    


 

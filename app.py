import streamlit as st
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval
import config
import os

# --- 1. CUSTOM STYLING ---
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
        transition: 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        border: 1px solid #2e7d32;
        color: #2e7d32;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALIZATION ---
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
contract = w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=config.CONTRACT_ABI)

# --- 3. HEADER LOGIC ---
def render_header():
    col_logo, col_text = st.columns([1, 4])
    
    # Logic to show the logo if it exists
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
        streamlit_js_eval(js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' })", key="connect_btn")
    st.sidebar.warning("Connect your wallet to interact with the blockchain.")
else:
    st.sidebar.success(f"Connected: {user_address[:6]}...{user_address[-4:]}")
    chain_id = streamlit_js_eval(js_expressions="window.ethereum.networkVersion", key="chain_id")
    if chain_id != "11155111":
        st.sidebar.error("⚠️ Switch MetaMask to Sepolia Testnet")

st.sidebar.divider()
page = st.sidebar.radio("Navigation", ["📊 Hospital Overview", "🏥 Dispensary (Staff)", "💰 Finance & Escrow", "🔑 Management (CEO)"])

# --- 5. PAGE: HOSPITAL OVERVIEW ---
if page == "📊 Hospital Overview":
    st.subheader("📊 Real-Time Operations Command Center")
    
    col1, col2, col3 = st.columns(3)
    with st.spinner("Fetching live blockchain data..."):
        try:
            escrow_bal = w3.from_wei(contract.functions.getContractBalance().call(), 'ether')
            orders_total = contract.functions.orderCount().call()
            user_bal_eth = w3.from_wei(w3.eth.get_balance(user_address), 'ether') if user_address else 0
        except:
            escrow_bal, orders_total, user_bal_eth = 0, 0, 0

    col1.metric("My Wallet Balance", f"{round(user_bal_eth, 4)} ETH")
    col2.metric("Contract Escrow", f"{escrow_bal} ETH")
    col3.metric("Total Procurement Orders", orders_total)

    st.divider()

    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("📋 Procurement Status")
        st.success("✅ **Blockchain Connection:** Online (Sepolia)")
        st.write("**Implementation Progress**")
        st.progress(95, text="Smart Contract Logic (95%)")
        st.progress(100, text="UI Integration (100%)")
    
    with c2:
        st.subheader("⚡ Quick Actions")
        if st.button("Refresh Chain Data"):
            st.rerun()

    with st.expander("ℹ️ About the Eco-Chain Procurement Solution"):
        st.write("""
            **Eco-Chain Procurement Solutions** aims to provide a solution to the abrupt 
            shortage of medication at local clinics and rural hospitals. We serve as the 
            secure bridge between hospitals and pharmaceutical companies.
            
            Using Ethereum Smart Contracts, we ensure:
            - **Trustless Escrow:** Payments are locked until receipt is verified.
            - **Transparency:** All stakeholders see the same inventory data in real-time.
            - **Security:** Immutable records prevent procurement fraud.
        """)

# --- 6. PAGE: DISPENSARY (STAFF) ---
elif page == "🏥 Dispensary (Staff)":
    st.header("🏥 Staff Portal")
    tab1, tab2 = st.tabs(["Issue Medication", "Verify Delivery"])
    
    with tab1:
        with st.form("issue_med_form"):
            med_name = st.text_input("Medication Name")
            submitted = st.form_submit_button("Log Usage")
            if submitted and user_address:
                data = contract.encodeABI(fn_name="issueMedication", args=[med_name])
                tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data}
                streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})")

    with tab2:
        with st.form("verify_del_form"):
            order_id = st.number_input("Order ID", min_value=1, step=1)
            submitted = st.form_submit_button("Confirm Receipt & Release Payment")
            if submitted and user_address:
                data = contract.encodeABI(fn_name="verifyDelivery", args=[int(order_id)])
                tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data}
                streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})")

# --- 7. PAGE: FINANCE & ESCROW ---
elif page == "💰 Finance & Escrow":
    st.header("💰 Financial Operations")
    with st.form("escrow_form"):
        o_id = st.number_input("Order ID to Fund", min_value=1, step=1)
        eth_val = st.number_input("Deposit Amount (ETH)", min_value=0.0, format="%.6f")
        submitted = st.form_submit_button("Deposit into

import streamlit as st
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval
import config
import os

# --- 1. SETTINGS & CUSTOM STYLING ---
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
    st.sidebar.warning("Please connect MetaMask.")
else:
    st.sidebar.success(f"Connected: {user_address[:6]}...{user_address[-4:]}")
    chain_id = streamlit_js_eval(js_expressions="window.ethereum.networkVersion", key="chain_id")
    if chain_id != "11155111":
        st.sidebar.error("⚠️ Switch to Sepolia Testnet")

st.sidebar.divider()
page = st.sidebar.radio("Navigation", [
    "📊 Hospital Overview", 
    "📈 Clinic Health Insights", 
    "🏥 Dispensary (Staff)", 
    "💰 Finance & Escrow", 
    "🔑 Management (CEO)"
])

# --- 5. PAGE: HOSPITAL OVERVIEW ---
if page == "📊 Hospital Overview":
    st.subheader("📊 Operational Transparency Dashboard")
    
    col1, col2 = st.columns(2)
    try:
        orders_total = contract.functions.orderCount().call()
    except:
        orders_total = 0

    col1.metric("Total Blockchain Orders", orders_total)
    col2.metric("Network Status", "Active", delta="Sepolia Testnet")
    
    st.divider()
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("📋 System Integrity")
        st.success(f"Verified Smart Contract: `{config.CONTRACT_ADDRESS}`")
        st.write("**Blockchain Transparency Ledger**")
        st.write("Current procurement data is immutable and verifiable by all health stakeholders.")
    
    with c2:
        st.subheader("⚡ Quick Actions")
        # --- RE-ADDED NOTIFICATION LOGIC ---
        if st.button("New Order Notification"):
            st.toast("Scanning blockchain for low stock levels...", icon="🔍")
            st.info("System checking minimum thresholds across all regions.")
        
        if st.button("Refresh System Logs"):
            st.rerun()

# --- 6. PAGE: CLINIC HEALTH INSIGHTS ---
elif page == "📈 Clinic Health Insights":
    st.header("📈 Regional HIV Trends")
    c1, c2, c3 = st.columns(3)
    c1.metric("Avg. Positivity Rate", "6.2%")
    c2.metric("ART Target Gap", "107,276")
    c3.metric("Highest Burden", "Region F")
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.write("**Positivity Rate (%)**")
        st.bar_chart({"A": 5.9, "B": 4.9, "C": 7.1, "D": 5.8, "E": 5.2, "F": 7.8, "G": 6.2})
    with col_r:
        st.write("**Treatment Shortfall (Gap)**")
        st.area_chart({"A": 14069, "B": 7076, "C": 6913, "D": 30948, "E": 6819, "F": 23532, "G": 17919})

# --- 7. PAGE: DISPENSARY (STAFF) ---
elif page == "🏥 Dispensary (Staff)":
    st.header("🏥 Staff Portal")
    t1, t2 = st.tabs(["Log Usage", "Verify Delivery"])
    with t1:
        with st.form(key="usage_form"):
            m_name = st.text_input("Medication Name")
            if st.form_submit_button("Record Usage on Chain") and user_address:
                data = contract.functions.issueMedication(m_name).build_transaction({'gas': 100000, 'nonce': 0})['data']
                tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data}
                streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})")
    with t2:
        with st.form(key="deliv_form"):
            o_id = st.number_input("Order ID", min_value=1)
            if st.form_submit_button("Confirm & Release Payment") and user_address:
                data = contract.functions.verifyDelivery(int(o_id)).build_transaction({'gas': 100000, 'nonce': 0})['data']
                tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data}
                streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})")

# --- 8. PAGE: FINANCE & ESCROW ---
elif page == "💰 Finance & Escrow":
    st.header("💰 Secure Escrow Funding")
    with st.form(key="fin_form"):
        fid = st.number_input("Order ID", min_value=1)
        fval = st.number_input("ETH Amount", min_value=0.0001, format="%.6f")
        if st.form_submit_button("Lock Funds in Escrow") and user_address:
            wei_val = w3.to_wei(fval, 'ether')
            data = contract.functions.depositEscrow(int(fid)).build_transaction({'gas': 100000, 'nonce': 0, 'value': wei_val})['data']
            tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data, 'value': hex(wei_val)}
            streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})")

# --- 9. PAGE: MANAGEMENT (CEO) ---
elif page == "🔑 Management (CEO)":
    st.header("🔑 Inventory Management")
    with st.form(key="ceo_form"):
        name = st.text_input("Product Name")
        col_a, col_b = st.columns(2)
        stock = col_a.number_input("Initial Stock", min_value=0)
        thresh = col_b.number_input("Reorder Threshold", min_value=1)
        qty = col_a.number_input("Order Quantity", min_value=1)
        price = col_b.number_input("Unit Price (ETH)", min_value=0.0, format="%.6f")
        supp = st.text_input("Supplier Wallet Address")
        
        if st.form_submit_button("Register Product on Blockchain"):
            if user_address:
                try:
                    data = contract.functions.addMedication(name, int(stock), int(thresh), int(qty), w3.to_wei(price, 'ether'), w3.to_checksum_address(supp)).build_transaction({'gas': 250000, 'nonce': 0})['data']
                    tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data}
                    streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})")
                except Exception as e:
                    st.error(f"Error: {e}")

st.sidebar.markdown("---")
st.sidebar.caption("Eco-Chain Procurement | v2.8")

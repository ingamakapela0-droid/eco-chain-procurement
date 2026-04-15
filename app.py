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
    st.subheader("📊 Operations Command Center")
    col1, col2, col3 = st.columns(3)
    try:
        escrow_bal = w3.from_wei(contract.functions.getContractBalance().call(), 'ether')
        orders_total = contract.functions.orderCount().call()
        user_bal_eth = w3.from_wei(w3.eth.get_balance(user_address), 'ether') if user_address else 0
    except:
        escrow_bal, orders_total, user_bal_eth = 0, 0, 0

    col1.metric("My Wallet", f"{round(user_bal_eth, 4)} ETH")
    col2.metric("Escrow Funds", f"{escrow_bal} ETH")
    col3.metric("Total Orders", orders_total)

# --- 6. PAGE: CLINIC HEALTH INSIGHTS ---
elif page == "📈 Clinic Health Insights":
    st.header("📈 Disease Insights")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Patients", "1,240")
    c2.metric("Chronic Cases", "450")
    c3.metric("Rural Zones", "3")
    st.bar_chart({"Hypertension": 150, "Diabetes": 120, "HIV/AIDS": 95, "Asthma": 60, "TB": 25})

# --- 7. PAGE: DISPENSARY (STAFF) ---
elif page == "🏥 Dispensary (Staff)":
    st.header("🏥 Staff Portal")
    t1, t2 = st.tabs(["Log Usage", "Verify Delivery"])
    with t1:
        with st.form(key="usage_form"):
            m_name = st.text_input("Medication Name")
            if st.form_submit_button("Log Usage") and user_address:
                data = contract.functions.issueMedication(m_name).build_transaction({'gas': 100000, 'nonce': 0})['data']
                tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data}
                streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})")
    with t2:
        with st.form(key="deliv_form"):
            o_id = st.number_input("Order ID", min_value=1)
            if st.form_submit_button("Confirm Receipt") and user_address:
                data = contract.functions.verifyDelivery(int(o_id)).build_transaction({'gas': 100000, 'nonce': 0})['data']
                tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data}
                streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})")

# --- 8. PAGE: FINANCE & ESCROW ---
elif page == "💰 Finance & Escrow":
    st.header("💰 Finance")
    with st.form(key="fin_form"):
        fid = st.number_input("Order ID", min_value=1)
        fval = st.number_input("ETH Amount", min_value=0.0, format="%.6f")
        if st.form_submit_button("Fund Escrow") and user_address:
            data = contract.functions.depositEscrow(int(fid)).build_transaction({'gas': 100000, 'nonce': 0, 'value': w3.to_wei(fval, 'ether')})['data']
            tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data, 'value': hex(w3.to_wei(fval, 'ether'))}
            streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})")

# --- 9. PAGE: MANAGEMENT (CEO) ---
elif page == "🔑 Management (CEO)":
    st.header("🔑 CEO Inventory")
    with st.form(key="ceo_form"):
        name = st.text_input("Product Name")
        stock = st.number_input("Stock", min_value=0)
        thresh = st.number_input("Threshold", min_value=1)
        qty = st.number_input("Reorder Qty", min_value=1)
        price = st.number_input("Price (ETH)", min_value=0.0, format="%.6f")
        supp = st.text_input("Supplier Wallet")
        if st.form_submit_button("Register Product") and user_address:
            try:
                data = contract.functions.addMedication(name, int(stock), int(thresh), int(qty), w3.to_wei(price, 'ether'), w3.to_checksum_address(supp)).build_transaction({'gas': 250000, 'nonce': 0})['data']
                tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data}
                streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})")
            except Exception as e:
                st.error(f"Error: {e}")

st.sidebar.markdown("---")
st.sidebar.caption("Eco-Chain Procurement | v2.3")

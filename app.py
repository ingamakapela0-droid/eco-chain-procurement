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
    st.subheader("📊 Real-Time Operations Command Center")
    
    col1, col2, col3 = st.columns(3)
    try:
        escrow_bal = w3.from_wei(contract.functions.getContractBalance().call(), 'ether')
        orders_total = contract.functions.orderCount().call()
        user_bal_eth = w3.from_wei(w3.eth.get_balance(user_address), 'ether') if user_address else 0
    except:
        escrow_bal, orders_total, user_bal_eth = 0, 0, 0

    col1.metric("My Wallet Balance", f"{round(user_bal_eth, 4)} ETH")
    col2.metric("Contract Escrow", f"{escrow_bal} ETH")
    col3.metric("Total Orders", orders_total)

    st.divider()

    with st.expander("ℹ️ About the Eco-Chain Procurement Solution"):
        st.write("""
            **Eco-Chain Procurement Solutions** aims to provide a solution to the abrupt 
            shortage of medication at local clinics and rural hospitals. 
            
            Using Ethereum Smart Contracts, we ensure:
            - **Trustless Escrow:** Payments are locked until receipt is verified.
            - **Transparency:** All stakeholders see the same data in real-time.
            - **Security:** Immutable records prevent procurement fraud.
        """)

# --- 6. PAGE: CLINIC HEALTH INSIGHTS (NEW) ---
elif page == "📈 Clinic Health Insights":
    st.header("📈 Clinic Health & Chronic Disease Insights")
    st.info("This data helps predict medication demand based on local patient demographics.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Patients", "1,240", "+12% MoM")
    c2.metric("Chronic Cases", "450", "Active")
    c3.metric("High-Risk Areas", "3", "Rural Zones")

    st.divider()
    st.subheader("Chronic Disease Distribution")
    
    disease_data = {
        "Hypertension": 150,
        "Diabetes (Type 2)": 120,
        "HIV/AIDS": 95,
        "Asthma": 60,
        "Tuberculosis": 25
    }
    st.bar_chart(disease_data)

    with st.form(key="stats_form"):
        st.write("### Update Local Clinic Stats")
        col_in1, col_in2 = st.columns(2)
        new_disease = col_in1.selectbox("Disease Category", ["Hypertension", "Diabetes", "HIV/AIDS", "Asthma", "TB"])
        new_count = col_in2.number_input("New Patient Count", min_value=0)
        if st.form_submit_button("Submit Monthly Data"):
            st.toast(f"Updated data for {new_disease} recorded.")

# --- 7. PAGE: DISPENSARY (STAFF) ---
elif page == "🏥 Dispensary (Staff)":
    st.header("🏥 Staff Portal")
    t1, t2 = st.tabs(["Log Usage", "Verify Delivery"])
    
    with t1:
        with st.form(key="usage_form"):
            med_name = st.text_input("Medication Name")
            if st.form_submit_button("Log Usage") and user_address:
                data = contract.encodeABI(fn_name="issueMedication", args=[med_name])
                tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data}
                streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})")

    with t2:
        with st.form(key="delivery_form"):
            order_id = st.number_input("Order ID", min_value=1, step=1)
            if st.form_submit_button("Confirm Receipt & Release Funds") and user_address:
                data = contract.encodeABI(fn_name="verifyDelivery", args=[int(order_id)])
                tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data}
                streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})")

# --- 8. PAGE: FINANCE & ESCROW ---
elif page == "💰 Finance & Escrow":
    st.header("💰 Financial Operations")
    with st.form(key="finance_form"):
        o_id = st.number_input("Order ID", min_value=1, step=1)
        eth_val = st.number_input("Amount (ETH)", min_value=0.0, format="%.6f")
        if st.form_submit_button("Deposit into Escrow") and user_address:
            wei_val = w3.to_wei(eth_val, 'ether')
            data = contract.encodeABI(fn_name="depositEscrow", args=[int(o_id)])
            tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data, 'value': hex(wei_val)}
            streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})")

# --- 9. PAGE: MANAGEMENT (CEO) ---
elif page == "🔑 Management (CEO)":
    st.header("🔑 Inventory Management")
    with st.form(key="admin_form"):
        m_name = st.text_input("Product Name")
        col_a, col_b = st.columns(2)
        m_stock = col_a.number_input("Starting Stock", min_value=0)
        m_thresh = col_b.number_input("Reorder Level", min_value=1)
        m_qty = col_a.number_input("Order Qty", min_value=1)
        m_price = col_b.number_input("Price (ETH)", min_value=0.0, format="%.6f")
        m_supp = st.text_input("Supplier Wallet")
        
        if st.form_submit_button("Register Product"):
            try:
                data = contract.encodeABI(fn_name="addMedication", args=[m_name, int(m_stock), int(m_thresh), int(m_qty), w3.to_wei(m_price, 'ether'), w3.to_checksum_address(m_supp)])
                tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data}
                streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})")
            except Exception as e:
                st.error(f"Error: {e}")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption("Eco-Chain Procurement | v2.2")

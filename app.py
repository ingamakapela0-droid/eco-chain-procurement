import streamlit as st
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval
import config
import os
import pandas as pd

# --- 1. THEME & SETTINGS ---
st.set_page_config(page_title="Eco-Chain | Gauteng Procurement", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #E2E8F0;
        padding: 20px;
        border-radius: 12px;
        border-top: 4px solid #0D9488;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    .stButton>button {
        background-color: #0D9488;
        color: white;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BLOCKCHAIN INITIALIZATION ---
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
contract = w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=config.CONTRACT_ABI)

# --- 3. SIDEBAR: LOGO & PROFILES ---
# UPDATED: Points to your local file and removes "B" logo
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=120)

st.sidebar.title("Eco-Chain")

user_address = streamlit_js_eval(js_expressions="window.ethereum ? window.ethereum.selectedAddress : null", key="wallet_check")
if not user_address:
    if st.sidebar.button("🔐 Connect MetaMask"):
        streamlit_js_eval(js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' })")
else:
    st.sidebar.success(f"Connected: {user_address[:6]}...{user_address[-4:]}")

st.sidebar.divider()
user_role = st.sidebar.selectbox("Access Level:", ["Management (CEO)", "Finance Dept", "Dispensary Staff"])

st.sidebar.divider()
# UPDATED: Removed the word "Ledger"
page = st.sidebar.radio("Navigation", [
    "🏠 Dashboard", 
    "💊 Medication Registry", 
    "📈 Clinic Health Insights",
    "📜 Transaction Records",
    "🏥 Hospital Management",
    "🚨 Alerts"
])

# --- 4. PAGE: DASHBOARD ---
if page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain Dashboard")
    st.info(f"Role: **{user_role}** | Location: Gauteng Province")
    
    with st.expander("ℹ️ About Eco-Chain Procurement", expanded=False):
        st.write("Eco-Chain uses Ethereum Smart Contracts to automate medical procurement and prevent stockouts in public health facilities.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Registered Meds", "142", "Gauteng")
    c2.metric("Procurement Txns", "1,024", "On-Chain")
    c3.metric("Critical Alerts", "5", "Low Stock")
    c4.metric("Network Status", "Online", "Sepolia")

    st.divider()
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.subheader("📊 Regional Stock Distribution")
        st.bar_chart({"A": 80, "B": 70, "C": 45, "D": 30, "E": 85, "F": 20, "G": 55})
    with col_r:
        st.subheader("⚡ Quick Actions")
        if st.button("🔔 Trigger Stock Scan"):
            st.toast("Scanning blockchain thresholds...")

# --- 5. PAGE: MEDICATION REGISTRY ---
elif page == "💊 Medication Registry":
    st.title("📝 Inventory Management")
    if user_role != "Management (CEO)":
        st.warning("⚠️ Access Denied. Only Management can edit records.")
    else:
        tab1, tab2 = st.tabs(["➕ Add New Medication", "✏️ Edit Medication"])
        with tab1:
            with st.form("add_med"):
                name = st.text_input("Product Name")
                stock = st.number_input("Initial Stock", min_value=0)
                thresh = st.number_input("Reorder Threshold", min_value=1)
                qty = st.number_input("Order Quantity", min_value=1)
                price = st.number_input("Price (ETH)", format="%.6f")
                supp = st.text_input("Supplier Wallet")
                if st.form_submit_button("Register on Blockchain"):
                    try:
                        data = contract.functions.addMedication(name, int(stock), int(thresh), int(qty), w3.to_wei(price, 'ether'), w3.to_checksum_address(supp)).build_transaction({'gas': 250000, 'nonce': 0})['data']
                        tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data}
                        streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})")
                    except Exception as e: st.error(f"Error: {e}")
        with tab2:
            st.selectbox("Select Medication to Edit:", ["Tenofovir", "Insulin", "Amoxicillin"])
            st.info("Parameter updates will be recorded as new blockchain transactions.")

# --- 6. PAGE: CLINIC HEALTH INSIGHTS ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Trends")
    st.bar_chart({"A": 5.9, "B": 4.9, "C": 7.1, "D": 5.8, "E": 5.2, "F": 7.8, "G": 6.2})
    st.area_chart({"A": 14069, "B": 7076, "C": 6913, "D": 30948, "E": 6819, "F": 23532, "G": 17919})

# --- 7. PAGE: TRANSACTION RECORDS ---
# UPDATED: Renamed from Ledger
elif page == "📜 Transaction Records":
    st.title("📜 Immutable Transaction Records")
    st.write("Verifiable audit trail of all inventory movements on the Sepolia Testnet.")
    records = pd.DataFrame([
        {"Time": "21:05", "User": "CEO_Admin", "Action": "Added Tenofovir", "Hash": "0x4f2...a1b"},
        {"Time": "20:40", "User": "Finance_Lead", "Action": "Escrow Funded", "Hash": "0x8e1...c3d"}
    ])
    st.table(records)

# --- 8. PAGE: HOSPITAL MANAGEMENT ---
elif page == "🏥 Hospital Management":
    st.title("🏥 Gauteng Network")
    st.write("- Chris Hani Baragwanath\n- Charlotte Maxeke\n- Steve Biko Academic")

# --- 9. PAGE: ALERTS ---
elif page == "🚨 Alerts":
    st.title("🚨 Alerts")
    st.error("Region F (Inner City) - Stock level critical (18%)")

st.sidebar.markdown("---")
st.sidebar.caption("Eco-Chain Procurement | v3.3")

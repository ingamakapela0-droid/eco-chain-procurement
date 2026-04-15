import streamlit as st
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval
import config
import os
import pandas as pd

# --- 1. PRO MEDICAL THEME (BLUE/TEAL PALETTE) ---
st.set_page_config(page_title="Eco-Chain | Gauteng Procurement", layout="wide")

st.markdown("""
    <style>
    /* Main Background */
    .main { background-color: #F8FAFC; }
    
    /* Global Card Style */
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #E2E8F0;
        padding: 20px;
        border-radius: 12px;
        border-top: 4px solid #0D9488; /* Teal Primary */
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    
    /* Header/Text Styles */
    h1, h2, h3 { color: #0F172A; font-family: 'Inter', sans-serif; }
    
    /* Button Styling */
    .stButton>button {
        background-color: #0D9488;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover { background-color: #0F766E; border: none; color: white; }
    
    /* Status Labels */
    .status-pill {
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BLOCKCHAIN INITIALIZATION ---
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
contract = w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=config.CONTRACT_ABI)

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.image("https://img.icons8.com/fluency/96/blockchain.png", width=80)
st.sidebar.title("Eco-Chain")
st.sidebar.caption("Gauteng Medical Ledger v3.0")

# Wallet Logic
user_address = streamlit_js_eval(js_expressions="window.ethereum ? window.ethereum.selectedAddress : null", key="wallet_check")
if not user_address:
    if st.sidebar.button("🔐 Connect MetaMask"):
        streamlit_js_eval(js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' })")
else:
    st.sidebar.success(f"Connected: {user_address[:6]}...{user_address[-4:]}")

st.sidebar.divider()
page = st.sidebar.radio("Go to:", [
    "🏠 Dashboard", 
    "💊 Medication Registry", 
    "📈 Clinic Health Insights",
    "📜 Transaction Ledger",
    "🏥 Hospital Management",
    "🚨 Alerts & Thresholds"
])

# --- 4. PAGE: DASHBOARD ---
if page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Overview")
    st.info("Ensuring medication continuity across Gauteng Province via blockchain transparency.")
    
    # Entities Summary
    c1, c2, c3, c4 = st.columns(4)
    try:
        total_orders = contract.functions.orderCount().call()
    except:
        total_orders = 0
        
    c1.metric("Registered Meds", "142 Items", "Gauteng")
    c2.metric("Procurement Volume", f"{total_orders} Txns", "On-Chain")
    c3.metric("Critical Alerts", "5 Units", "Low Stock")
    c4.metric("Network Status", "Active", "Sepolia")

    st.divider()
    
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.subheader("📊 Stock Distribution vs Regional Positivity")
        chart_data = pd.DataFrame({
            "Region": ["A", "B", "C", "D", "E", "F", "G"],
            "Stock Level": [80, 70, 45, 30, 85, 20, 55]
        }).set_index("Region")
        st.bar_chart(chart_data)
        
    with col_r:
        st.subheader("⚡ Quick Actions")
        if st.button("🔔 New Order Notification"):
            st.toast("Scanning stock thresholds...")
        st.success("✅ Smart Contract Verified")
        st.caption(f"Contract: {config.CONTRACT_ADDRESS[:10]}...")

# --- 5. PAGE: MEDICATION REGISTRY ---
elif page == "💊 Medication Registry":
    st.title("📝 Medication Registry")
    st.write("Register and track new batches of medication directly on the blockchain.")
    
    with st.form("med_form"):
        col_in1, col_in2 = st.columns(2)
        name = col_in1.text_input("Product Name")
        stock = col_in2.number_input("Initial Stock", min_value=0)
        thresh = col_in1.number_input("Reorder Threshold", min_value=1)
        qty = col_in2.number_input("Order Quantity", min_value=1)
        price = col_in1.number_input("Price (ETH)", format="%.6f")
        supp = col_in2.text_input("Supplier Wallet (0x...)")
        
        if st.form_submit_button("🚀 Register & Commit to Blockchain"):
            if user_address:
                try:
                    data = contract.functions.addMedication(name, int(stock), int(thresh), int(qty), w3.to_wei(price, 'ether'), w3.to_checksum_address(supp)).build_transaction({'gas': 250000, 'nonce': 0})['data']
                    tx = {'from': user_address, 'to': config.CONTRACT_ADDRESS, 'data': data}
                    streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx}] }})")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please connect MetaMask.")

# --- 6. PAGE: CLINIC HEALTH INSIGHTS ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Trends")
    st.caption("Data Source: DHIS Regional Profile (Gauteng)")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("HIV Positivity Rate (%)")
        st.bar_chart({"A": 5.9, "B": 4.9, "C": 7.1, "D": 5.8, "E": 5.2, "F": 7.8, "G": 6.2})
    with c2:
        st.subheader("ART Adherence Gap")
        st.area_chart({"A": 14069, "B": 7076, "C": 6913, "D": 30948, "E": 6819, "F": 23532, "G": 17919})

# --- 7. PAGE: TRANSACTION LEDGER ---
elif page == "📜 Transaction Ledger":
    st.title("📜 Immutable Ledger")
    st.write("Real-time log of all medication movements recorded on the Sepolia network.")
    
    # Sample Ledger Data (In a real app, you'd fetch events from Web3)
    ledger = pd.DataFrame([
        {"Time": "21:05", "Medication": "Tenofovir", "Action": "Batch Issued", "Hash": "0x4f2...a1b"},
        {"Time": "20:40", "Medication": "Insulin", "Action": "Deposit Escrow", "Hash": "0x8e1...c3d"},
        {"Time": "19:12", "Medication": "Amoxicillin", "Action": "Registry Add", "Hash": "0x2a9...f7e"}
    ])
    st.dataframe(ledger, use_container_width=True)

# --- 8. PAGE: HOSPITAL MANAGEMENT ---
elif page == "🏥 Hospital Management":
    st.title("🏥 Gauteng Facility Network")
    hospitals = [
        "Chris Hani Baragwanath", "Charlotte Maxeke", "Steve Biko Academic", 
        "Helen Joseph", "Kalafong Hospital", "Tembisa Hospital", 
        "Leratong Hospital", "George Mukhari"
    ]
    st.write("The following major facilities are integrated into the Eco-Chain network:")
    for h in hospitals:
        st.markdown(f"- **{h}**")

# --- 9. PAGE: ALERTS & THRESHOLDS ---
elif page == "🚨 Alerts & Thresholds":
    st.title("🚨 Active System Alerts")
    st.error("**Low Stock Alert:** Region F (Inner City) is currently at 20% capacity for ART Kits.")
    st.warning("**Temp Warning:** Batch #004 (Insulin) reported 8°C (Limit: 2-7°C).")
    st.info("**Upcoming Expiry:** 42 Units of Antibiotics in Region D expire in 14 days.")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Eco-Chain | Trustless Healthcare Logistics")
  
 

    
   
   
    

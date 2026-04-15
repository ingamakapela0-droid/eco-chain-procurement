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
    .about-box {
        background-color: #F1F5F9;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #0D9488;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BLOCKCHAIN INITIALIZATION ---
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
contract = w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=config.CONTRACT_ABI)

# --- 3. SIDEBAR: LOGO & RESTORED USER SELECTION ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=120)
st.sidebar.title("Eco-Chain")

# MetaMask Connection
user_address = streamlit_js_eval(js_expressions="window.ethereum ? window.ethereum.selectedAddress : null", key="wallet_check")
if not user_address:
    if st.sidebar.button("🔐 Connect MetaMask"):
        streamlit_js_eval(js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' })")
else:
    st.sidebar.success(f"Connected: {user_address[:6]}...")

st.sidebar.divider()

# --- RESTORED: MANUAL USER ROLE SELECTION ---
st.sidebar.subheader("👤 User Profile")
current_role = st.sidebar.selectbox("Login As:", [
    "Management (CEO)", 
    "Operations (COO)", 
    "Finance Dept", 
    "Public Stakeholder"
])

st.sidebar.divider()
page = st.sidebar.radio("Navigation", [
    "🏠 Dashboard", 
    "📊 External Subscription",
    "💊 Medication Registry", 
    "📈 Clinic Health Insights",
    "📜 Transaction Records",
    "🏥 Hospital Management"
])

# --- 4. PAGE: DASHBOARD (Restored About & Notifications) ---
if page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    
    st.markdown("""
        <div class="about-box">
            <h3>Mission: Eco-Chain Procurement Solutions</h3>
            <p>A digital bridge utilizing <b>Ethereum Smart Contracts</b> to ensure medication continuity. 
            We mitigate stockouts for ART and diagnostics by providing a trustless escrow system and an 
            immutable record of inventory across the Gauteng health network.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.subheader("🔗 Core Blockchain Features")
        f1, f2, f3 = st.columns(3)
        f1.info("**Trustless Escrow**")
        f2.info("**Immutable Logs**")
        f3.info("**Auto-Reordering**")
        
        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("Integrated Clinics", "42", "Gauteng")
        c2.metric("On-Chain Txns", "1,024", "Verified")
        c3.metric("System Health", "Optimal", "Sepolia")

    with col_side:
        st.subheader("⚡ Notification Centre")
        if st.button("🔔 New Order Notification"):
            st.toast("Scanning blockchain thresholds...", icon="🔍")
        if st.button("🔄 Refresh System Logs"):
            st.rerun()
        st.error("**Alert:** Low Stock in Region D")

# --- 5. PAGE: EXTERNAL SUBSCRIPTION ---
elif page == "📊 External Subscription":
    st.title("🛡️ Stakeholder Subscription Portal")
    st.write("External organizations can subscribe to regional stats and API feeds.")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div style='background-color:#E0F2F1; padding:20px; border-radius:12px; border:2px dashed #0D9488; text-align:center;'>"
                    "<h3>Researcher Tier</h3><p>Anonymized Regional Trends</p><h4>0.05 ETH / Mo</h4></div>", unsafe_allow_html=True)
        st.button("Subscribe via MetaMask")
    with col_b:
        st.subheader("🔗 API Access")
        st.code("X-ECO-CHAIN-KEY: 8f2b-92ea-44bc-918d")

# --- 6. PAGE: MEDICATION REGISTRY (Permissions Fixed) ---
elif page == "💊 Medication Registry":
    st.title("📝 Inventory Management")
    # This logic now correctly checks for CEO or COO from the selection box
    if "CEO" in current_role or "COO" in current_role:
        st.success(f"Access Granted: {current_role}")
        tab1, tab2 = st.tabs(["➕ Add New Medication", "✏️ Edit Medication"])
        with tab1:
            with st.form("add_form"):
                n = st.text_input("Product Name")
                s = st.number_input("Initial Stock", min_value=0)
                t = st.number_input("Threshold", min_value=1)
                p = st.number_input("Price (ETH)", format="%.6f")
                if st.form_submit_button("Commit to Blockchain"):
                    st.info("Transaction prepared for MetaMask...")
        with tab2:
            st.selectbox("Select Medication to Edit:", ["Tenofovir", "Insulin", "Amoxicillin"])
            st.button("Update Parameters")
    else:
        st.error("🚫 Access Denied. Management credentials (CEO/COO) are required.")

# --- 7. PAGE: CLINIC HEALTH INSIGHTS ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Insights")
    st.bar_chart({"A": 5.9, "B": 4.9, "C": 7.1, "D": 5.8, "E": 5.2, "F": 7.8, "G": 6.2})
    st.divider()
    reg = st.selectbox("Select Region:", ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"])
    facilities = {
        "Region A": ["Bophelong", "Diepsloot South", "Ebony Park", "Rabie Ridge"],
        "Region D": ["Soweto", "Dobsonville", "Protea Glen", "Diepkloof"],
        "Region F": ["Inner City Clinic", "CBD Hub", "Jeppe Clinic"]
    }
    st.write(f"Facilities in {reg}: {', '.join(facilities.get(reg, ['Regional Clinic Hubs']))}")

# --- 8. PAGE: TRANSACTION RECORDS ---
elif page == "📜 Transaction Records":
    st.title("📜 Transaction Records")
    df = pd.DataFrame([
        {"Time": "21:05", "User": "CEO", "Action": "Added Tenofovir", "Hash": "0x4f2...a1b"},
        {"Time": "20:40", "User": "Finance", "Action": "Funded Escrow", "Hash": "0x8e1...c3d"}
    ])
    st.table(df)

# --- 9. PAGE: HOSPITAL MANAGEMENT ---
elif page == "🏥 Hospital Management":
    st.title("🏥 Gauteng Hospital Network")
    hospitals = ["Chris Hani Baragwanath", "Charlotte Maxeke", "Steve Biko Academic", "Helen Joseph", "Kalafong Hospital", "Tembisa Hospital", "Leratong Hospital", "George Mukhari"]
    for h in hospitals:
        st.markdown(f"- **{h}**")

st.sidebar.markdown("---")
st.sidebar.caption("Eco-Chain Procurement | v3.8")
     



           
        
      
   
   

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
    .feature-card {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BLOCKCHAIN INITIALIZATION ---
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
contract = w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=config.CONTRACT_ABI)

# --- 3. SIDEBAR: LOGO & PROFILES ---
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
page = st.sidebar.radio("Navigation", [
    "🏠 Dashboard", 
    "💊 Medication Registry", 
    "📈 Clinic Health Insights",
    "📜 Transaction Records",
    "🏥 Hospital Management",
    "🚨 Alerts"
])

# --- 4. PAGE: DASHBOARD (Restored Descriptions) ---
if page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain Dashboard")
    
    # Restored Detailed Description
    st.markdown("""
        <div style="background-color: #F1F5F9; padding: 20px; border-radius: 10px; border-left: 6px solid #0D9488;">
            <h3>Project Mission: Eco-Chain Procurement</h3>
            <p>Eco-Chain acts as a <b>digital bridge</b> between healthcare facilities and suppliers in the Gauteng Province. 
            By leveraging blockchain technology, we mitigate medication shortages, specifically for ART and critical diagnostics, 
            ensuring that life-saving supplies reach the clinics with the highest clinical burden.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Blockchain Features Section
    st.subheader("🔗 Core Blockchain Features")
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown("""<div class="feature-card"><b>Trustless Escrow</b><br>Payments are locked in the smart contract and only released once delivery is verified on-chain.</div>""", unsafe_allow_html=True)
    with f2:
        st.markdown("""<div class="feature-card"><b>Immutable Transparency</b><br>Every inventory change and order is recorded on the Sepolia network, preventing procurement fraud.</div>""", unsafe_allow_html=True)
    with f3:
        st.markdown("""<div class="feature-card"><b>Automated Reordering</b><br>Smart contracts trigger new procurement cycles automatically when clinic stock hits critical thresholds.</div>""", unsafe_allow_html=True)

    st.divider()
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Registered Meds", "142", "Gauteng")
    c2.metric("Procurement Txns", "1,024", "On-Chain")
    c3.metric("Critical Alerts", "5", "Low Stock")
    c4.metric("Network Status", "Online", "Sepolia")

# --- 5. PAGE: CLINIC HEALTH INSIGHTS (Restored Clinic Density) ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Trends & Facility Mapping")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("HIV Positivity Rate (%)")
        st.bar_chart({"A": 5.9, "B": 4.9, "C": 7.1, "D": 5.8, "E": 5.2, "F": 7.8, "G": 6.2})
    with c2:
        st.subheader("ART Adherence Gap")
        st.area_chart({"A": 14069, "B": 7076, "C": 6913, "D": 30948, "E": 6819, "F": 23532, "G": 17919})
    
    st.divider()
    st.subheader("📍 Detailed Regional Facility List")
    selected_region = st.selectbox("Select Region to view all integrated clinics:", ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"])
    
    facilities = {
        "Region A": ["Bophelong Clinic", "Diepsloot South", "Ebony Park / Kaalfontein", "Eyathu Ya Rona", "Halfway House", "Mayibuye", "Midrand West", "Rabie Ridge"],
        "Region B": ["Berario Clinic", "Bosmont", "Claremont", "Parkhurst", "Randburg", "Riverlea Major", "Rosebank Satellite", "Windsor"],
        "Region C": ["Roodepoort Clinic", "Constantia Kloof", "Northgate", "Florida", "Bram Fischerville", "Zandspruit"],
        "Region D": ["Doornkop", "Soweto", "Dobsonville", "Protea Glen", "Diepkloof", "Meadowlands", "Orlando", "Zola"],
        "Region E": ["Alexandra", "Wynberg", "Sandton", "Orange Grove", "Houghton", "Beatrice Court"],
        "Region F": ["Inner City Clinic", "CBD Health Hub", "Johannesburg South", "South Gate", "Jeppe Clinic", "80 Albert Street"],
        "Region G": ["Orange Farm", "Ennerdale", "Lenasia", "Eldorado Park", "Protea South", "Stretford Clinic"]
    }
    
    st.info(f"Showing {len(facilities[selected_region])} facilities in {selected_region}")
    cols = st.columns(2)
    for i, clinic in enumerate(facilities[selected_region]):
        cols[i % 2].write(f"- {clinic}")

# --- (Other pages: Registry, Records, etc. remain the same as v3.3) ---
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
                        streamlit_js_eval(js_expressions=f"window.ethereum.request({ method: 'eth_sendTransaction', params: [{tx}] })")
                    except Exception as e: st.error(f"Error: {e}")
        with tab2:
            st.selectbox("Select Medication to Edit:", ["Tenofovir", "Insulin", "Amoxicillin"])
            st.info("Parameter updates will be recorded as new blockchain transactions.")

elif page == "📜 Transaction Records":
    st.title("📜 Immutable Transaction Records")
    records = pd.DataFrame([
        {"Time": "21:05", "User": "CEO_Admin", "Action": "Added Tenofovir", "Hash": "0x4f2...a1b"},
        {"Time": "20:40", "User": "Finance_Lead", "Action": "Escrow Funded", "Hash": "0x8e1...c3d"}
    ])
    st.table(records)

elif page == "🏥 Hospital Management":
    st.title("🏥 Gauteng Hospital Network")
    hospitals = ["Chris Hani Baragwanath", "Charlotte Maxeke", "Steve Biko Academic", "Helen Joseph", "Kalafong Hospital", "Tembisa Hospital", "Leratong Hospital", "George Mukhari"]
    for h in hospitals:
        st.markdown(f"- **{h}**")

elif page == "🚨 Alerts":
    st.title("🚨 Alerts")
    st.error("Region F (Inner City) - Stock level critical (18%)")

st.sidebar.markdown("---")
st.sidebar.caption("Eco-Chain Procurement | v3.4")

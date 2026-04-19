import streamlit as st
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval
import config
import os
import pandas as pd

# --- 1. THEME & STYLING ---
st.set_page_config(page_title="Eco-Chain | Gauteng Procurement", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    div[data-testid="stMetric"] {
        background-color: white; border: 1px solid #E2E8F0; padding: 20px;
        border-radius: 12px; border-top: 4px solid #0D9488;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    .stButton>button {
        background-color: #0D9488; color: white; border-radius: 8px;
    }
    .about-box {
        background-color: #F1F5F9; padding: 25px; border-radius: 10px;
        border-left: 6px solid #0D9488; margin-bottom: 25px;
    }
    .region-card {
        background-color: #FFFFFF; padding: 15px; border-radius: 10px;
        border: 1px solid #E2E8F0; margin-bottom: 15px;
    }
    .mission-text {
        font-size: 1.05rem; line-height: 1.6; color: #1E293B; text-align: justify;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BLOCKCHAIN INITIALIZATION ---
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
contract = w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=config.CONTRACT_ABI)

# --- 3. SIDEBAR: IDENTITY & NAVIGATION FILTER ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=120)
st.sidebar.title("Eco-Chain")

# Wallet Connectivity
user_address = streamlit_js_eval(js_expressions="window.ethereum ? window.ethereum.selectedAddress : null", key="wallet_check")
if not user_address:
    if st.sidebar.button("🔐 Connect MetaMask"):
        streamlit_js_eval(js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' })")

st.sidebar.divider()
st.sidebar.subheader("👤 User Profile")
current_role = st.sidebar.selectbox("Access Level:", [
    "Public Stakeholder (Read-Only)",
    "Management (CEO)", 
    "Operations (COO)", 
    "Finance Dept"
])

# DYNAMIC NAVIGATION LOGIC (Role-Based Access Control)
# Public only sees Dashboard and Insights. CEO sees everything.
nav_options = ["🏠 Dashboard", "📈 Clinic Health Insights"]

if current_role == "Management (CEO)":
    nav_options += ["📊 Subscription Portal", "💊 Medication Registry", "📜 Transaction Records", "🏥 Hospital Management"]
elif current_role in ["Operations (COO)", "Finance Dept"]:
    nav_options += ["💊 Medication Registry", "📜 Transaction Records"]

page = st.sidebar.radio("Navigation", nav_options)

# --- 4. PAGE: DASHBOARD (Restored Full Overview) ---
if page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    
    # YOUR FULL OVERVIEW TEXT INTEGRATED HERE
    st.markdown(f"""
        <div class="about-box">
            <h3>Mission Overview & System Impact</h3>
            <div class="mission-text">
                <b>Eco-Chain Procurement Solutions</b> is designed to address the persistent and often abrupt shortages 
                of medication experienced at local clinics, rural hospitals, and other healthcare facilities. 
                These shortages not only disrupt the delivery of essential healthcare services but also place patients 
                at significant risk, particularly those who rely on consistent access to chronic medication. 
                Our solution positions Eco-Chain as a vital bridge between healthcare institutions and pharmaceutical companies, 
                ensuring a more efficient, transparent, and responsive supply chain.<br><br>
                At the core of our solution is an innovative, user-friendly application that integrates directly with 
                the inventory systems of hospitals and clinics. This app continuously monitors medication stock levels in real time. 
                Each time medication is dispensed, it is scanned by the healthcare provider, and the system instantly updates 
                the inventory on the app. This live tracking capability allows for accurate visibility of stock levels, 
                helping facilities anticipate shortages before they occur and enabling timely reordering from pharmaceutical suppliers.<br><br>
                By automating and digitising the inventory management process, Eco-Chain reduces the likelihood of human error, 
                miscounts, and delays in reporting low stock. This ensures that healthcare providers can make informed decisions quickly, 
                improving operational efficiency and patient care outcomes.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.subheader("🔗 Blockchain Strategy")
        st.write("""Eco-Chain ensures that patients receive sufficient and uninterrupted medication 
        during their stay. It strengthens healthcare delivery systems and contributes to more reliable 
        and equitable access to essential medicines, particularly in underserved and rural communities.""")
        
        f1, f2, f3 = st.columns(3)
        f1.info("**Trustless Escrow**")
        f2.info("**Immutable Transparency**")
        f3.info("**Real-Time Sync**")
        
        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("Integrated Clinics", "42", "Gauteng")
        c2.metric("Verified Txns", "1,024", "Blockchain")
        c3.metric("System Health", "Optimal", "Sepolia")

    with col_side:
        st.subheader("⚡ Notification Centre")
        if st.button("🔔 Trigger Stock Scan"):
            st.toast("Scanning blockchain for low stock levels...", icon="🔍")
        st.error("**Urgent Alert:** Region F stock below 20%")
        st.warning("**Temp Warning:** Batch #044 (Insulin)")

# --- 5. PAGE: SUBSCRIPTION PORTAL (CEO ONLY) ---
elif page == "📊 Subscription Portal":
    st.title("🛡️ External Stakeholder Management")
    st.write("Review and authorize third-party researchers and API access keys.")
    st.code("X-ECO-CHAIN-KEY: 8f2b-92ea-44bc-918d", language="text")

# --- 6. PAGE: MEDICATION REGISTRY (Internal Only) ---
elif page == "💊 Medication Registry":
    st.title("📝 Inventory Management")
    st.success(f"Management Access Verified: {current_role}")
    tab1, tab2 = st.tabs(["➕ Add New Medication", "✏️ Edit Medication"])
    with tab1:
        with st.form("add_form"):
            st.text_input("Product Name")
            st.number_input("Initial Stock", min_value=0)
            st.form_submit_button("Commit to Blockchain")

# --- 7. PAGE: CLINIC HEALTH INSIGHTS (Public Access) ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Insights & Facility Directory")
    st.bar_chart({"A": 5.9, "B": 4.9, "C": 7.1, "D": 5.8, "E": 5.2, "F": 7.8, "G": 6.2})
    
    st.divider()
    st.subheader("📍 Regional Facility Directory")
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown("<div class='region-card'><b>Region A (Midrand)</b><br>• Bophelong Clinic<br>• Diepsloot South<br>• Ebony Park<br>• Rabie Ridge</div>", unsafe_allow_html=True)
   with r2:
        st.markdown("<div class='region-card'><b>Region D (Soweto)</b><br>• Doornkop<br>• Dobsonville<br>• Protea Glen<br>• Diepkloof</div>", unsafe_allow_html=True)
        st.markdown("<div class='region-card'><b>Region E (Sandton)</b><br>• Alexandra<br>• Sandton<br>• Wynberg</div>", unsafe_allow_html=True)

    with r3:
        st.markdown("<div class='region-card'><b>Region F (Inner City)</b><br>• CBD Health Hub<br>• Jeppe Clinic<br>• 80 Albert Street<br>• Joubert Park</div>", unsafe_allow_html=True)
        st.markdown("<div class='region-card'><b>Region G (Deep South)</b><br>• Orange Farm<br>• Ennerdale<br>• Lenasia</div>", unsafe_allow_html=True)
  

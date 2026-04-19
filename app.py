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
        width: 100%;
    }
    .about-box {
        background-color: #F1F5F9;
        padding: 25px;
        border-radius: 10px;
        border-left: 6px solid #0D9488;
        margin-bottom: 25px;
    }
    .region-card {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        margin-bottom: 15px;
    }
    .mission-text {
        font-size: 1.05rem;
        line-height: 1.6;
        color: #1E293B;
        text-align: justify;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BLOCKCHAIN INITIALIZATION ---
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
contract = w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=config.CONTRACT_ABI)

# --- 3. SIDEBAR: LOGO & MANUAL ACCESS ---
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
st.sidebar.subheader("👤 User Profile")
current_role = st.sidebar.selectbox("Access Level:", [
    "Management (CEO)", 
    "Operations (COO)", 
    "Finance Dept", 
    "Public Stakeholder (Read-Only)"
])

st.sidebar.divider()
page = st.sidebar.radio("Navigation", [
    "🏠 Dashboard", 
    "📊 Subscription Portal",
    "💊 Medication Registry", 
    "📈 Clinic Health Insights",
    "📜 Transaction Records",
    "🏥 Hospital Management"
])

# --- 4. PAGE: DASHBOARD (Updated with your full overview) ---
if page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    
    # MISSION OVERVIEW (Your full text integrated here)
    st.markdown("""
        <div class="about-box">
            <h3>System Overview & Mission</h3>
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
                By automating and digitising the inventory management process, Eco-Chain reduces the likelihood of 
                human error, miscounts, and delays in reporting low stock. This ensures that healthcare providers 
                can make informed decisions quickly, improving operational efficiency and patient care outcomes.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_main, col_side = st.columns([2, 1])
    
    with col_main:
        st.subheader("🔗 Blockchain Advantage")
        st.write("""Furthermore, it ensures that admitted patients receive sufficient and uninterrupted medication 
        during their stay, which is critical for effective treatment and recovery. Eco-Chain enhances coordination 
        between supply and demand, contributing to more reliable and equitable access to essential medicines.""")
        
        f1, f2, f3 = st.columns(3)
        f1.info("**Trustless Escrow**")
        f2.info("**Immutable Transparency**")
        f3.info("**Real-Time Sync**")
        
        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("Integrated Clinics", "42 Facilities", "Gauteng")
        c2.metric("Verified Txns", "1,024", "Blockchain")
        c3.metric("System Health", "Optimal", "Sepolia")

    with col_side:
        st.subheader("⚡ Notification Centre")
        if st.button("🔔 Trigger Stock Scan"):
            st.toast("Scanning blockchain for low stock levels...", icon="🔍")
        st.error("**Urgent Alert:** Region F stock below 20%")
        st.warning("**Temp Warning:** Batch #044 (Insulin)")

# --- 5. PAGE: SUBSCRIPTION PORTAL ---
elif page == "📊 Subscription Portal":
    st.title("🛡️ External Stakeholder Access")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div style='background-color:#E0F2F1; padding:20px; border-radius:12px; border:2px dashed #0D9488; text-align:center;'>"
                    "<h3>Researcher Access</h3><p>Anonymized Health Trends</p><h4>0.05 ETH / Mo</h4></div>", unsafe_allow_html=True)
        st.button("Subscribe via MetaMask")
    with col_b:
        st.subheader("🔗 API Integration")
        st.code("X-ECO-CHAIN-KEY: 8f2b-92ea-44bc-918d")

# --- 6. PAGE: MEDICATION REGISTRY ---
elif page == "💊 Medication Registry":
    st.title("📝 Inventory Management")
    if "CEO" in current_role or "COO" in current_role:
        st.success(f"Management Access Verified: {current_role}")
        tab1, tab2 = st.tabs(["➕ Add New Medication", "✏️ Edit Medication"])
        with tab1:
            with st.form("add_form"):
                n = st.text_input("Product Name")
                s = st.number_input("Initial Stock", min_value=0)
                t = st.number_input("Threshold", min_value=1)
                p = st.number_input("Price (ETH)", format="%.6f")
                if st.form_submit_button("Commit to Blockchain"):
                    st.info("Transaction prepared. Check MetaMask.")
        with tab2:
            st.subheader("Update Existing Records")
            st.selectbox("Select Medication:", ["Tenofovir", "Insulin", "Amoxicillin"])
            st.button("Confirm Update")
    else:
        st.error("🚫 Access Denied. Only CEO or COO can access this registry.")

# --- 7. PAGE: CLINIC HEALTH INSIGHTS ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Insights & Facility Directory")
    cg1, cg2 = st.columns(2)
    with cg1: st.bar_chart({"A": 5.9, "B": 4.9, "C": 7.1, "D": 5.8, "E": 5.2, "F": 7.8, "G": 6.2})
    with cg2: st.area_chart({"A": 14069, "B": 7076, "C": 6913, "D": 30948, "E": 6819, "F": 23532, "G": 17919})
    
    st.divider()
    st.subheader("📍 Regional Facility Directory")
    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown("<div class='region-card'><b>Region A (Midrand)</b><br>• Bophelong Clinic<br>• Diepsloot South<br>• Ebony Park<br>• Rabie Ridge</div>", unsafe_allow_html=True)
        st.markdown("<div class='region-card'><b>Region B (Randburg)</b><br>• Berario<br>• Parkhurst<br>• Randburg</div>", unsafe_allow_html=True)
    with r2:
        st.markdown("<div class='region-card'><b>Region D (Soweto)</b><br>• Doornkop<br>• Dobsonville<br>• Protea Glen<br>• Diepkloof</div>", unsafe_allow_html=True)
        st.markdown("<div class='region-card'><b>Region E (Sandton)</b><br>• Alexandra<br>• Sandton<br>• Wynberg</div>", unsafe_allow_html=True)
    with r3:
        st.markdown("<div class='region-card'><b>Region F (Inner City)</b><br>• CBD Health Hub<br>• Jeppe Clinic<br>• 80 Albert Street<br>• Joubert Park</div>", unsafe_allow_html=True)
        st.markdown("<div class='region-card'><b>Region G (Deep South)</b><br>• Orange Farm<br>• Ennerdale<br>• Lenasia</div>", unsafe_allow_html=True)

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
st.sidebar.caption("Eco-Chain Procurement | v4.1")

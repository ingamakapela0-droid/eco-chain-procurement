import streamlit as st
import pandas as pd
import json
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval

# --- 1. CONFIG & IDENTITY ---
try:
    from config import CONTRACT_ADDRESS, CONTRACT_ABI, RPC_URL, ADMIN_ADDR, CEO_ADDR, FIN_OFFICER_ADDR
except ImportError:
    st.error("Missing config.py! Ensure it is in the same folder.")
    st.stop()

LOGO_FILE = "logo.png" 
w3 = Web3(Web3.HTTPProvider(RPC_URL))
st.set_page_config(page_title="Eco-Chain | Healthcare Ledger", layout="wide")

# --- 2. BRANDING & STYLING ---
st.markdown(f"""
    <style>
    :root {{ --teal: #0D9488; --gold: #B45309; }}
    .main {{ background-color: #F8FAFC; }}
    .watermark {{
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-30deg);
        font-size: 8vw; color: rgba(13, 148, 136, 0.05); font-weight: 900;
        z-index: -1; pointer-events: none; white-space: nowrap;
    }}
    [data-testid="stSidebar"] {{ background-color: #FFFFFF; border-right: 2px solid var(--teal); }}
    .stButton>button {{ 
        background: linear-gradient(135deg, var(--teal), #0F766E); 
        color: white; border-radius: 12px; font-weight: bold; height: 3.5em; width: 100%;
    }}
    .connect-btn>button {{
        background: linear-gradient(135deg, #F6851B, #E2761B) !important;
        border: none !important;
    }}
    </style>
    <div class="watermark">ECO-CHAIN SOLUTIONS</div>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR & CONNECTION LOGIC ---
with st.sidebar:
    try: st.image(LOGO_FILE, use_column_width=True)
    except: st.title("🌿 Eco-Chain")
    
    st.markdown("---")
    
    # JavaScript logic to check for accounts and request connection
    raw_wallet = streamlit_js_eval(js_expressions="async function getAccount() { const accounts = await window.ethereum.request({ method: 'eth_accounts' }); return accounts[0]; }; getAccount();", key="wallet_check")
    
    wallet_addr = None
    user_role = "Unregistered"

    if not raw_wallet:
        st.warning("🦊 MetaMask is not connected.")
        # Connect Button for all roles
        if st.button("Connect to MetaMask", key="connect_metamask_btn", help="Link your wallet to access Eco-Chain features"):
            streamlit_js_eval(js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' });", key="request_conn")
            st.rerun()
    else:
        wallet_addr = Web3.to_checksum_address(raw_wallet)
        st.success(f"Connected: {wallet_addr[:6]}...{wallet_addr[-4:]}")
        
        # Identity Mapping
        if wallet_addr.lower() == CEO_ADDR.lower(): user_role = "CEO"
        elif wallet_addr.lower() == ADMIN_ADDR.lower(): user_role = "Admin"
        elif wallet_addr.lower() == FIN_OFFICER_ADDR.lower(): user_role = "Financial Officer"
        else:
            user_role = st.selectbox("Switch Testing Role", ["Unregistered", "Hospital", "Supplier"])
        
        st.info(f"Identity: **{user_role}**")

    st.markdown("---")
    tabs_nav = ["🏠 Overview", "📈 Health Insights"]
    
    # Dynamic Navigation
    if user_role == "Unregistered":
        tabs_nav += ["📝 Register Account"]
    else:
        if user_role == "Admin": tabs_nav += ["🛠️ Admin Approvals"]
        if user_role == "CEO": tabs_nav += ["📋 Hospital Requests", "💊 Issue Orders", "💰 Financial Oversight"]
        if user_role == "Financial Officer": tabs_nav += ["📑 Invoice Verification", "📊 Revenue Tracking"]
        if user_role == "Hospital": tabs_nav += ["🏥 Hospital Stock"]
        if user_role == "Supplier": tabs_nav += ["📦 Supplier Orders", "📤 Send Invoice", "💳 Subscriptions"]
    
    page = st.sidebar.radio("Navigation Menu", tabs_nav)

# --- 4. BLOCKCHAIN ENGINE ---
def record_on_chain(target_to, value_eth=0):
    if not wallet_addr:
        st.error("No wallet connected. Transaction aborted.")
        return
    try:
        nonce = w3.eth.get_transaction_count(wallet_addr)
        tx_params = {
            "from": wallet_addr, "to": target_to, "value": hex(w3.to_wei(value_eth, 'ether')),
            "nonce": hex(nonce), "chainId": "0xaa36a7" 
        }
        js_code = f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{json.dumps(tx_params)}] }});"
        streamlit_js_eval(js_expressions=js_code)
    except Exception as e:
        st.error(f"Execution Error: {e}")

# --- 5. PAGE MODULES ---

if page == "🏠 Overview":
    st.title("🏥 Eco-Chain Procurement Solutions")
    st.info("""
    **Mission Statement**
    
    Eco-Chain Procurement Solutions aims to provide a solution to the abrupt shortage of medication at local clinics and rural hospitals and clinics. We will be the bridge between the hospital and pharmaceutical companies.
    
    Our app will be linked to the hospital or clinic we’re working with and it will monitor the medication stock levels. When any medication leaves the dispensary, it will be scanned by whoever is issuing the medication and this will show on the app.
    
    All medication will have a minimum number that is allowed to be left in the dispensary and once it reaches that minimum, we /it will notify the suppliers and the medication will be sent to the clinic or hospital before it fully runs out. This will eliminate medication running out and patients having to wait for long periods of time to receive medication.
    
    There will be contracts in place to ensure payment for all deliverables between the public clinics/hospitals and the suppliers.
    """)

    st.markdown("### 🔗 Blockchain Pulse: System Metrics")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Stockout Prevention", "100%", "System Target")
    with c2: st.metric("Contract Security", "Verified", "On-Chain")
    with c3: st.metric("Regional Coverage", "7 Hubs", "Online")
    with c4: st.metric("Automated Alerts", "Active", "24/7 Monitoring")

elif page == "📈 Health Insights":
    st.title("📈 Regional Health Trends & Insights")
    tab_regions, tab_hiv, tab_tb = st.tabs(["📍 Regional Network", "📊 HIV Statistics", "🫁 TB Statistics"])

    with tab_regions:
        st.subheader("City of Johannesburg: Regional Mapping")
        region_map = pd.DataFrame({
            "Region": ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"],
            "Hubs Covered": ["Diepsloot, Midrand", "Randburg, Rosebank", "Roodepoort, Florida", "Soweto, Dobsonville", "Alexandra, Sandton", "Inner City", "Orange Farm, Lenasia"]
        })
        st.table(region_map)

    with tab_hiv:
        st.subheader("HIV Positivity Rate by Region (%)")
        hiv_data = pd.DataFrame({"Positivity Rate": [5.9, 4.9, 7.1, 5.8, 5.2, 7.8, 6.2]}, 
                                index=["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"])
        st.bar_chart(hiv_data)
        st.table(hiv_data.T)

    with tab_tb:
        st.subheader("TB Treatment Success vs. Mortality (%)")
        tb_data = pd.DataFrame({
            "Success Rate": [89.4, 90.3, 87.5, 80.5, 87.0, 80.7, 81.5],
            "Death Rate": [5.3, 3.7, 4.3, 7.8, 5.8, 4.0, 7.1]
        }, index=["Reg A", "Reg B", "Reg C", "Reg D", "Reg E", "Reg F", "Reg G"])
        st.bar_chart(tb_data)
        st.table(tb_data.T)

elif page == "📝 Register Account":
    st.title("📝 Entity Registration Portal")
    if not wallet_addr:
        st.warning("Please connect your MetaMask wallet in the sidebar first to register.")
    else:
        with st.form("reg_form"):
            st.text_input("Entity Name", placeholder="e.g. Soweto Regional Hospital")
            role = st.selectbox("Role to Register", ["Hospital", "Supplier"])
            if st.form_submit_button("Submit for Admin Review"):
                record_on_chain(ADMIN_ADDR)
                st.success("Registration submitted on the blockchain.")

elif page == "📊 Revenue Tracking":
    st.title("📊 Financial Officer: System Revenue")
    st.metric("Total System Revenue", "R124,500")

elif page == "📤 Send Invoice":
    st.title("📤 Supplier: Generate Invoice")
    with st.form("inv_form"):
        hosp = st.selectbox("Target Hospital", ["Soweto Clinic", "Region F Hub"])
        amt = st.number_input("Amount (ZAR)", min_value=0)
        if st.form_submit_button("Submit to Financial Officer"):
            record_on_chain(FIN_OFFICER_ADDR)

elif page == "📑 Invoice Verification":
    st.title("📑 Financial Officer: Verify Invoices")
    st.table(pd.DataFrame({"ID": ["INV-001"], "From": ["MediCore"], "Amt": ["R12,000"], "Status": ["Pending"]}))
    if st.button("Approve & Push to CEO"):
        record_on_chain(CEO_ADDR)

elif page == "💰 Financial Oversight":
    st.title("💰 CEO: Final Authorization")
    st.info("Verified Invoices awaiting final settlement.")
    if st.button("Finalize Blockchain Payment"):
        record_on_chain(ADMIN_ADDR)

elif page == "🛠️ Admin Approvals":
    st.title("🛠️ Admin: User Confirmation")
    target = st.text_input("Wallet Address to Verify")
    if st.button("Confirm Registration on Chain"):
        record_on_chain(target)

elif page == "🏥 Hospital Stock":
    st.title("🏥 Hospital: Stock Control")
    st.table(pd.DataFrame({"Medicine": ["ARVs", "Insulin"], "Current": [45, 12]}))
    st.button("Scan Out Medication")

elif page == "📦 Supplier Orders":
    st.title("📦 Supplier: Active Shipments")
    st.table(pd.DataFrame({"Order": ["#TX-99"], "Status": ["AUTHORIZED"]}))

elif page == "💳 Subscriptions":
    st.title("💳 Supplier Subscriptions")
    st.metric("Annual Plan", "R28,400")
    st.button("Pay Subscription")

# --- FOOTER ---
st.markdown("---")
st.caption("Eco-Chain Solutions | Version 14.8 | Johannesburg, South Africa")
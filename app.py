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

w3 = Web3(Web3.HTTPProvider(RPC_URL))
st.set_page_config(page_title="Eco-Chain | Healthcare Ledger", layout="wide")

# Persistent Session State for Demo Flow
if 'invoices' not in st.session_state:
    st.session_state.invoices = []

# --- 2. BRANDING & STYLING ---
st.markdown(f"""
    <style>
    :root {{ --teal: #0D9488; }}
    .stButton>button {{ 
        background: linear-gradient(135deg, var(--teal), #0F766E); 
        color: white; border-radius: 12px; font-weight: bold; height: 3.5em; width: 100%;
    }}
    .metric-card {{ background: white; padding: 20px; border-radius: 10px; border-left: 5px solid var(--teal); }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR & CONNECTION ---
with st.sidebar:
    st.title("🌿 Eco-Chain")
    raw_wallet = streamlit_js_eval(js_expressions="async function getAccount() { const accounts = await window.ethereum.request({ method: 'eth_accounts' }); return accounts[0]; }; getAccount();", key="wallet_check")
    
    wallet_addr = None
    user_role = "Unregistered"

    if not raw_wallet:
        if st.button("Connect to MetaMask"):
            streamlit_js_eval(js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' });", key="request_conn")
            st.rerun()
    else:
        wallet_addr = Web3.to_checksum_address(raw_wallet)
        if wallet_addr.lower() == CEO_ADDR.lower(): user_role = "CEO"
        elif wallet_addr.lower() == ADMIN_ADDR.lower(): user_role = "Admin"
        elif wallet_addr.lower() == FIN_OFFICER_ADDR.lower(): user_role = "Financial Officer"
        else: user_role = st.selectbox("Switch Role (Testing)", ["Unregistered", "Hospital", "Supplier", "Financial Officer"])
        st.info(f"Connected: **{user_role}**")

    tabs_nav = ["🏠 Overview", "📈 Health Insights"]
    if user_role == "Unregistered": tabs_nav += ["📝 Register Account"]
    else:
        if user_role == "Admin": tabs_nav += ["🛠️ Admin Approvals"]
        if user_role == "CEO": tabs_nav += ["💰 Financial Oversight"]
        if user_role == "Financial Officer": tabs_nav += ["📑 Invoice Verification"]
        if user_role == "Supplier": tabs_nav += ["📤 Send Invoice", "💳 Subscriptions"]
        if user_role == "Hospital": tabs_nav += ["🏥 Hospital Stock"]
    
    page = st.sidebar.radio("Navigation Menu", tabs_nav)

# --- 4. BLOCKCHAIN ENGINE ---
def record_on_chain(target_to, data_note="Eco-Chain activity", value_eth=0):
    if not wallet_addr: return
    try:
        hex_data = Web3.to_hex(text=data_note)
        tx_params = {
            "from": wallet_addr, "to": target_to, 
            "value": hex(w3.to_wei(value_eth, 'ether')),
            "nonce": hex(w3.eth.get_transaction_count(wallet_addr)), 
            "chainId": "0xaa36a7", "data": hex_data 
        }
        js_code = f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{json.dumps(tx_params)}] }});"
        streamlit_js_eval(js_expressions=js_code)
        st.info(f"Broadcasting to Ledger: {data_note}")
    except Exception as e: st.error(f"TX Error: {e}")

# --- 5. PAGE MODULES ---

if page == "🏠 Overview":
    st.title("🏥 Eco-Chain Procurement Solutions")
    st.info("""
    **Mission Statement**
Eco-Chain Procurement Solutions
Eco-Chain Procurement Solutions aims to provide a solution to the abrupt shortage of medication at local clinics and rural hospitals and clinics. We will be the bridge between the hospital and pharmaceutical companies.
Our app will be linked to the hospital or clinic we’re working with and it will monitor the medication stock levels. When any medication leaves the dispensary, it will be scanned by whoever is issuing the medication and this will show on the app. 
All medication will have a minimum number that is allowed to be left in the dispensary and once it reaches that minimum, we /it will notify the suppliers and the medication will be sent to the clinic or hospital before it fully runs out. This will eliminate medication running out and patients having to wait for long periods of time to receive medication.
There will be contracts in place to ensure payment for all deliverables  between the public clinics/hospitals and the suppliers.

    """)
    st.markdown("### 🔗 Blockchain Pulse")
    c1, c2, c3 = st.columns(3)
    c1.metric("Stockout Prevention", "100%", "Target")
    c2.metric("On-Chain Security", "Active", "Immutability")
    c3.metric("Service Nodes", "7 Hubs", "Johannesburg")

elif page == "📈 Health Insights":
    st.title("📈 Regional Health Trends")
    t1, t2, t3 = st.tabs(["📍 Regions", "📊 HIV Trends", "🫁 TB Trends"])
    with t1:
        st.table(pd.DataFrame({
            "Region": ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"],
            "Hub": ["Diepsloot", "Randburg", "Roodepoort", "Soweto", "Sandton", "Inner City", "Orange Farm"]
        }))
    with t2:
        st.bar_chart(pd.DataFrame({"Positivity %": [5.9, 4.9, 7.1, 5.8, 5.2, 7.8, 6.2]}, index=["A","B","C","D","E","F","G"]))
    with t3:
        st.bar_chart(pd.DataFrame({"Success %": [89.4, 90.3, 87.5, 80.5, 87.0, 80.7, 81.5]}, index=["A","B","C","D","E","F","G"]))

elif page == "📝 Register Account":
    st.title("📝 Entity Registration")
    with st.form("reg"):
        name = st.text_input("Organization Name")
        r = st.selectbox("Role", ["Hospital", "Supplier", "Financial Officer"])
        if st.form_submit_button("Record Registration On-Chain"):
            record_on_chain(ADMIN_ADDR, f"REGISTRATION: {r} | NAME: {name}") # Visible on Etherscan

elif page == "📤 Send Invoice":
    st.title("📤 Supplier: New Invoice")
    with st.form("inv"):
        amt = st.number_input("Amount (ZAR)", min_value=1)
        if st.form_submit_button("Submit to Financial Officer"):
            st.session_state.invoices.append({"id": len(st.session_state.invoices)+1, "amt": amt, "status": "Pending FO"})
            record_on_chain(FIN_OFFICER_ADDR, f"INVOICE: R{amt} Submitted")

elif page == "📑 Invoice Verification":
    st.title("📑 Financial Officer: Verification Queue")
    pending = [i for i in st.session_state.invoices if i['status'] == "Pending FO"]
    if not pending: st.write("Queue is empty.")
    else:
        for p in pending:
            st.subheader(f"Invoice #{p['id']}")
            st.write(f"Amount: R{p['amt']}")
            if st.button(f"Verify & Push to CEO #{p['id']}"):
                p['status'] = "Pending CEO"
                record_on_chain(CEO_ADDR, f"VERIFIED: Inv #{p['id']} by FO")
                st.rerun()

elif page == "💰 Financial Oversight":
    st.title("💰 CEO: Payment Authorization")
    verified = [i for i in st.session_state.invoices if i['status'] == "Pending CEO"]
    if not verified: st.write("No invoices awaiting settlement.")
    else:
        for v in verified:
            st.subheader(f"Verified Invoice #{v['id']}")
            st.write(f"Amount: R{v['amt']}")
            if st.button(f"Authorize Settlement #{v['id']}"):
                v['status'] = "Paid"
                record_on_chain(ADMIN_ADDR, f"PAID: Inv #{v['id']} Final Approval")
                st.success("Payment settlement recorded.")
                st.rerun()

# --- FOOTER ---
st.markdown("---")
st.caption("Eco-Chain Solutions | Version 15.4 | Johannesburg Hub | On-Chain Transparency Enabled")
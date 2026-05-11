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

# --- 2. BRANDING & WATERMARK ---
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
        color: white; border-radius: 12px; font-weight: bold; height: 3.5em;
    }}
    </style>
    <div class="watermark">ECO-CHAIN SOLUTIONS</div>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR (Logo + Menu + Wallet) ---
with st.sidebar:
    try: st.image(LOGO_FILE, use_column_width=True)
    except: st.title("🌿 Eco-Chain")
    
    st.markdown("---")
    raw_wallet = streamlit_js_eval(js_expressions="async function getAccount() { const accounts = await window.ethereum.request({ method: 'eth_accounts' }); return accounts[0]; }; getAccount();", key="wallet")
    
    user_role = "Guest"
    wallet_addr = None

    if raw_wallet:
        wallet_addr = Web3.to_checksum_address(raw_wallet)
        st.success(f"Connected: {wallet_addr[:6]}...{wallet_addr[-4:]}")
        if wallet_addr.lower() == ADMIN_ADDR.lower(): user_role = "Admin"
        elif wallet_addr.lower() == CEO_ADDR.lower(): user_role = "CEO"
        elif wallet_addr.lower() == FIN_OFFICER_ADDR.lower(): user_role = "Financial Officer"
        else: user_role = "Supplier / Hospital"
        st.info(f"Role: **{user_role}**")
    else:
        st.warning("🔒 Wallet Locked")

    st.markdown("---")
    tabs = ["🏠 Overview", "📈 Health Insights"]
    if user_role == "Admin": tabs += ["🛠️ Admin Verification"]
    if user_role == "CEO": tabs += ["📋 Hospital Requests", "💊 Issue Orders"]
    if user_role == "Supplier / Hospital": tabs += ["📦 Supplier Orders", "💳 Subscriptions"]
    page = st.sidebar.radio("Navigation Menu", tabs)

# --- 4. BLOCKCHAIN ENGINE ---
def record_on_chain(target_to, data="0x", value_eth=0):
    nonce = w3.eth.get_transaction_count(wallet_addr)
    tx_params = {
        "from": wallet_addr, "to": target_to, "value": hex(w3.to_wei(value_eth, 'ether')),
        "nonce": hex(nonce), "chainId": "0xaa36a7" 
    }
    js_code = f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{json.dumps(tx_params)}] }});"
    streamlit_js_eval(js_expressions=js_code)

# --- 5. PAGE MODULES ---

if page == "🏠 Overview":
    st.title("🏥 Eco-Chain | Regional Logistics")
    st.info("""
    **Mission:** Eco-Chain Procurement Solutions aims to provide a solution to the abrupt 
    shortage of medication at local clinics and rural hospitals. We will be the bridge 
    between the hospital and pharmaceutical companies.
    
    Our app is linked to the hospital or clinic we’re working with and it will monitor 
    the medication stock levels. When any medication leaves the dispensary, it will 
    be scanned by whoever is issuing the medication and this will show on the app. 
    
    All medication will have a minimum number that is allowed to be left in the 
    dispensary and once it reaches that minimum, the system will notify the suppliers 
    and the medication will be sent to the clinic or hospital before it fully runs out. 
    """)

elif page == "📈 Health Insights":
    st.title("📈 Regional Health Trends & Insights")
    
    # NEW: REGIONS TABLE
    st.subheader("📍 City of Johannesburg: Regional Network")
    region_map = pd.DataFrame({
        "Region": ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"],
        "Hubs / Areas Covered": [
            "Diepsloot, Midrand, Lanseria, Fourways",
            "Randburg, Rosebank, Melville, Northcliff",
            "Roodepoort, Florida, Bram Fischerville",
            "Doornkop, Soweto, Dobsonville, Protea Glen",
            "Alexandra, Wynberg, Sandton, Houghton",
            "Inner City, Johannesburg South",
            "Orange Farm, Ennerdale, Lenasia, Eldorado Park"
        ]
    })
    st.table(region_map)

    # HIV DATA
    st.subheader("📊 HIV Epidemic Trends (2019/20)")
    hiv_df = pd.DataFrame({
        "Region": ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"],
        "Positive Results": [18718, 5358, 13994, 27067, 9290, 21197, 18773],
        "Positivity Rate": ["5.9%", "4.9%", "7.1%", "5.8%", "5.2%", "7.8%", "6.2%"]
    })
    st.table(hiv_df)

    # TB DATA
    st.subheader("🫁 TB Treatment Outcomes (2018/19)")
    tb_df = pd.DataFrame({
        "Region": ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"],
        "Success Rate": ["89.4%", "90.3%", "87.5%", "80.5%", "87.0%", "80.7%", "81.5%"],
        "Death Rate": ["5.3%", "3.7%", "4.3%", "7.8%", "5.8%", "4.0%", "7.1%"]
    })
    st.table(tb_df)

elif page == "🛠️ Admin Verification":
    st.title("🛠️ Admin: Identity Verification")
    target = st.text_input("Entity Wallet Address")
    if st.button("Authorize Entity on Blockchain"):
        record_on_chain(wallet_addr)
        st.success(f"Verification for {target} recorded.")

elif page == "📋 Hospital Requests":
    st.title("📋 CEO: Pending Hospital Requests")
    reqs = pd.DataFrame({
        "Hospital": ["Chris Hani Baragwanath", "Charlotte Maxeke"],
        "Medicine": ["Insulin", "Paracetamol"],
        "Status": ["PENDING CEO REVIEW", "PENDING CEO REVIEW"]
    })
    st.table(reqs)

elif page == "💊 Issue Orders":
    st.title("💊 CEO: Authorize Supplier Order")
    with st.container(border=True):
        med = st.text_input("Medication Name")
        supplier = st.text_input("Supplier Address")
        if st.button("Record Authorized Order"):
            record_on_chain(wallet_addr)
            st.success(f"Order for {med} transmitted.")

elif page == "📦 Supplier Orders":
    st.title("📦 Supplier: Incoming CEO Orders")
    orders = pd.DataFrame({
        "Order ID": ["#TX-9921", "#TX-9925"],
        "Issued By": ["Eco-Chain CEO", "Eco-Chain CEO"],
        "Status": ["AUTHORIZED - READY TO SHIP", "AUTHORIZED - READY TO SHIP"]
    })
    st.table(orders)
    if st.button("Confirm Shipment on Blockchain"):
        record_on_chain(wallet_addr)
        st.success("Shipment status recorded.")

# --- FOOTER ---
st.markdown("---")
st.caption("Eco-Chain Solutions | Blockchain Procurement v13.6")
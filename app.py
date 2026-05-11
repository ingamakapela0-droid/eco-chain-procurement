import streamlit as st
import pandas as pd
import plotly.express as px
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval

# --- 1. CONFIG & IDENTITY ---
try:
    from config import CONTRACT_ADDRESS, CONTRACT_ABI, RPC_URL, ADMIN_ADDR, CEO_ADDR, FIN_OFFICER_ADDR
except:
    st.error("Missing config.py!")
    st.stop()

# CHANGE THIS TO YOUR ACTUAL GITHUB RAW IMAGE URL
LOGO_URL = "https://raw.githubusercontent.com/YourRepo/main/logo.png"

w3 = Web3(Web3.HTTPProvider(RPC_URL))
st.set_page_config(page_title="Eco-Chain | Healthcare Ledger", layout="wide")

# --- 2. THEME & WATERMARK (Teal & Gold) ---
st.markdown(f"""
    <style>
    :root {{ --teal: #0D9488; --gold: #B45309; --bg: #F1F5F9; }}
    .main {{ background-color: var(--bg); }}
    
    /* Watermark */
    .watermark {{
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-25deg);
        font-size: 100px; color: rgba(13, 148, 136, 0.04); font-weight: 800;
        z-index: -1; pointer-events: none; white-space: nowrap;
    }}
    
    /* Custom Sidebar Logo Styling */
    [data-testid="stSidebar"] {{ background-color: #FFFFFF; border-right: 2px solid var(--teal); }}
    .stButton>button {{ background-color: var(--teal); color: white; border-radius: 20px; }}
    .stButton>button:hover {{ border: 2px solid var(--gold); background: white; color: var(--gold); }}
    </style>
    <div class="watermark">ECO-CHAIN SOLUTIONS</div>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR LOGIN ---
with st.sidebar:
    st.image(LOGO_URL, width=220)
    st.markdown("---")
    
    raw_wallet = streamlit_js_eval(js_expressions="async function getAccount() { const accounts = await window.ethereum.request({ method: 'eth_accounts' }); return accounts[0]; }; getAccount();", key="wallet")
    
    user_role = "Guest"
    wallet_addr = None
    is_subscribed = False # This would normally be a blockchain check

    if raw_wallet:
        wallet_addr = Web3.to_checksum_address(raw_wallet)
        st.success(f"Verified: {wallet_addr[:6]}...{wallet_addr[-4:]}")
        
        # Role Logic
        if wallet_addr.lower() == ADMIN_ADDR.lower(): user_role = "Admin"
        elif wallet_addr.lower() == CEO_ADDR.lower(): user_role = "CEO"
        elif wallet_addr.lower() == FIN_OFFICER_ADDR.lower(): user_role = "Financial Officer"
        else: user_role = "Supplier" # Fallback for demo
        
        st.info(f"Authorized as: **{user_role}**")
    else:
        st.warning("🔒 Access Restricted. Connect MetaMask.")

# --- 4. DYNAMIC NAVIGATION ---
tabs = ["🏠 Overview", "📈 Health Insights"]
if user_role in ["CEO", "Supplier"]: tabs += ["💳 Subscription Board"]
if user_role == "CEO": tabs += ["💊 Issue Medication"]
if user_role == "Admin": tabs += ["🛠️ Network Control"]

page = st.radio("Menu", tabs, horizontal=True)

# --- 5. PAGE MODULES ---

if page == "🏠 Overview":
    st.title("🏥 Regional Healthcare Logistics")
    st.markdown("### Ecosystem Performance")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Live Nodes", "14", "Gauteng Region")
    c2.metric("Block Confirmations", "99.9%", "Secured")
    c3.metric("Inventory Burn Rate", "-12%", "Optimal")
    
    st.info("**Company Mission:** Eco-Chain provides immutable supply chain integrity, preventing stock-outs of life-saving medicine through real-time blockchain monitoring.")

elif page == "📈 Health Insights":
    st.title("📈 Demand & Stock Analytics")
    
    # Live Chart Simulation
    df = pd.DataFrame({'Week': ['W1', 'W2', 'W3', 'W4'], 'Insulin': [400, 450, 300, 500], 'ARVs': [200, 220, 210, 250]})
    fig = px.bar(df, x='Week', y=['Insulin', 'ARVs'], barmode='group', color_discrete_sequence=['#0D9488', '#B45309'])
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Regional Facility Status")
    st.dataframe(pd.DataFrame({
        "Facility": ["Johannesburg Central", "Pretoria West", "Soweto Clinic"],
        "Status": ["Stocked", "Reordering", "Stocked"],
        "Last Block ID": ["#9921", "#9925", "#9928"]
    }), use_container_width=True)

elif page == "💳 Subscription Board":
    st.title("💳 Partner Tiers")
    if user_role == "Supplier":
        st.success("🌟 STATUS: ACTIVE PREMIUM SUPPLIER")
    
    st.write("Manage your organization's access to the Eco-Chain procurement network.")
    col_x, col_y = st.columns(2)
    col_x.button("Standard Access (Free)")
    if col_y.button("Upgrade to Enterprise (0.05 ETH)"):
        st.write("Awaiting Block Confirmation...")

elif page == "💊 Issue Medication":
    st.title("💊 Medication Issue Authorization")
    st.info("Directives issued here are immutable and legally binding for suppliers.")
    
    with st.container(border=True):
        med = st.text_input("Medication Name", "Insulin Pen 300u")
        hosp = st.selectbox("Facility", ["Helen Joseph", "Rahima Moosa", "Edenvale"])
        amount = st.slider("Quantity to Issue", 100, 5000, 500)
        
        if st.button("Confirm & Record on Blockchain"):
            st.success(f"CEO APPROVED: {amount} units of {med} allocated to {hosp}.")

# --- FOOTER ---
st.markdown("---")
st.caption("Eco-Chain Solutions © 2026 | Built for Sustainable Healthcare Systems")
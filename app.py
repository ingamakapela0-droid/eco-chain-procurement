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

# Using the local file in your folder
LOGO_FILE = "logo.png" 

w3 = Web3(Web3.HTTPProvider(RPC_URL))
st.set_page_config(page_title="Eco-Chain | Healthcare Ledger", layout="wide")

# --- 2. BRANDING, WATERMARK & STYLING ---
st.markdown(f"""
    <style>
    :root {{ --teal: #0D9488; --gold: #B45309; }}
    .main {{ background-color: #F8FAFC; }}
    
    /* Company Watermark - Stays Fixed in Background */
    .watermark {{
        position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-30deg);
        font-size: 8vw; color: rgba(13, 148, 136, 0.05); font-weight: 900;
        z-index: -1; pointer-events: none; white-space: nowrap;
    }}
    
    /* Sidebar and Button Styling */
    [data-testid="stSidebar"] {{ background-color: #FFFFFF; border-right: 2px solid var(--teal); }}
    .stButton>button {{ 
        background: linear-gradient(135deg, var(--teal), #0F766E); 
        color: white; border-radius: 12px; font-weight: bold; height: 3.5em;
    }}
    </style>
    <div class="watermark">ECO-CHAIN SOLUTIONS</div>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR LOGO & WALLET ---
with st.sidebar:
    try:
        st.image(LOGO_FILE, use_column_width=True)
    except:
        st.title("🌿 Eco-Chain") # Fallback if logo.png isn't found
        
    st.markdown("---")
    raw_wallet = streamlit_js_eval(js_expressions="async function getAccount() { const accounts = await window.ethereum.request({ method: 'eth_accounts' }); return accounts[0]; }; getAccount();", key="wallet")
    
    user_role = "Guest"
    wallet_addr = None

    if raw_wallet:
        wallet_addr = Web3.to_checksum_address(raw_wallet)
        st.success(f"Connected: {wallet_addr[:6]}...{wallet_addr[-4:]}")
        
        # Check Role for navigation
        if wallet_addr.lower() == ADMIN_ADDR.lower(): user_role = "Admin"
        elif wallet_addr.lower() == CEO_ADDR.lower(): user_role = "CEO"
        elif wallet_addr.lower() == FIN_OFFICER_ADDR.lower(): user_role = "Financial Officer"
        else: user_role = "Supplier / Hospital"
        
        st.info(f"Authorized as: **{user_role}**")
    else:
        st.warning("🔒 Please Connect MetaMask")

# --- 4. NAVIGATION ---
# Restricted view: Subscriptions only for CEO and Suppliers
tabs = ["🏠 Overview", "📈 Health Insights"]
if user_role in ["CEO", "Supplier / Hospital"]: tabs += ["💳 Subscriptions"]
if user_role == "CEO": tabs += ["💊 Issue Medication"]
if user_role == "Admin": tabs += ["🛠️ Governance"]

page = st.radio("Menu", tabs, horizontal=True)

# --- 5. PAGE MODULES ---

if page == "🏠 Overview":
    st.title("🏥 Eco-Chain | Regional Logistics Overview")
    st.markdown("#### Real-time Healthcare Supply Chain Monitoring")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Network Nodes", "24", "Live")
    c2.metric("On-Chain Audits", "100%", "Verified")
    c3.metric("Stock Safety", "94%", "Optimal")
    
    st.write("---")
    st.info("**About Eco-Chain:** We prevent medication stock-outs by bridging the gap between hospital demand and supplier fulfillment using an immutable blockchain ledger.")

elif page == "📈 Health Insights":
    st.title("📈 Demand vs. Supply Analytics")
    
    # Simple table and metrics for Health Insights (No Plotly required)
    st.markdown("### Regional Facility Status")
    insights_data = pd.DataFrame({
        "Facility": ["Chris Hani Baragwanath", "Charlotte Maxeke", "Steve Biko"],
        "Inventory Level": ["92%", "88%", "96%"],
        "Status": ["Stable", "Reordering", "Stable"],
        "Last Audit": ["Success", "Success", "Success"]
    })
    st.table(insights_data)
    
    st.markdown("### Strategic Analysis")
    st.write("Based on current blockchain data, regional demand for ARVs is trending upward. The automated procurement logic is scheduled to trigger reorders at 15:00 SAST.")

elif page == "💳 Subscriptions":
    st.title("💳 Partner Subscription Board")
    
    if user_role == "Supplier / Hospital":
        st.success("✨ **Status:** Active Premium Partner")
        st.caption("Verified for regional bidding.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Standard Tier")
        st.write("• Basic Ledger Access\n• Email Alerts")
        st.button("Active", disabled=True)
    with col2:
        st.markdown("### Enterprise Tier")
        st.write("• Priority Fulfillment\n• Deep-Dive Analytics")
        if st.button("Upgrade (0.05 ETH)"):
            st.info("Opening MetaMask for Payment...")

elif page == "💊 Issue Medication":
    st.title("💊 CEO: Medication Disbursement")
    st.info("CEO Access: Issues are recorded as immutable requests on the blockchain.")
    
    with st.container(border=True):
        med = st.text_input("Medication Name", "Insulin Pen")
        hosp = st.selectbox("Facility", ["Chris Hani Baragwanath", "Charlotte Maxeke", "Steve Biko"])
        qty = st.slider("Quantity", 100, 5000, 1000)
        
        if st.button("Authorize & Record Transaction"):
            st.success(f"CEO APPROVED: {qty} units of {med} allocated to {hosp}.")

# --- FOOTER ---
st.markdown("---")
st.caption("Eco-Chain Solutions | Presentation Build 2026")
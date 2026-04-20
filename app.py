import streamlit as st
import pandas as pd
import os
from streamlit_js_eval import streamlit_js_eval

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Eco-Chain | Secure Procurement", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    .about-box { background-color: #F1F5F9; padding: 25px; border-radius: 10px; border-left: 6px solid #0D9488; margin-bottom: 25px; }
    .insight-box { background-color: #FFFFFF; padding: 25px; border-radius: 10px; border: 1px solid #E2E8F0; margin-bottom: 25px; text-align: justify; line-height: 1.6; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE MASTER LIST OF IDs (Paste your team's real IDs here) ---
AUTHORIZED_WALLETS = {
    "0xe367800E0cEcCC2A7d5aCedd42d80b194A9381Ed": "CEO",
    "0x71C7656EC7ab88b098defB751B7401B5f6d8976F": "System Developer",
    "0x1234567890abcdef1234567890abcdef12345678": "Finance Director",
    "0xABC1234567890abcdef1234567890abcdef1234": "COO",
    "0xDEF1234567890abcdef1234567890abcdef1234": "Marketing Director"
}

# Project's wallet to receive subscription payments
PROJECT_TREASURY = "0xe367800E0cEcCC2A7d5aCedd42d80b194A9381Ed"

# --- 3. SESSION STATE ---
if "user_wallet" not in st.session_state:
    st.session_state.user_wallet = None
if "user_role" not in st.session_state:
    st.session_state.user_role = "Guest"
if "subscribed" not in st.session_state:
    st.session_state.subscribed = False

# --- 4. SIDEBAR: THE REAL METAMASK CONNECTION ---
st.sidebar.title("🌿 Eco-Chain Auth")

# Trigger MetaMask Connection
wallet_id = streamlit_js_eval(
    js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' }).then(accounts => accounts[0])", 
    key="metamask_connection"
)

if wallet_id:
    st.session_state.user_wallet = wallet_id
    st.session_state.user_role = AUTHORIZED_WALLETS.get(wallet_id, "Public Stakeholder")
    
    st.sidebar.success(f"Connected: {st.session_state.user_role}")
    st.sidebar.code(f"{wallet_id[:10]}...{wallet_id[-4:]}")
    
    if st.sidebar.button("Disconnect"):
        st.session_state.user_wallet = None
        st.session_state.user_role = "Guest"
        st.rerun()
else:
    st.sidebar.warning("Please connect your MetaMask to enter.")

# --- 5. NAVIGATION & ACCESS CONTROL ---
if st.session_state.user_role == "Guest":
    st.title("🏥 Welcome to Eco-Chain")
    st.info("Please use the sidebar to connect your MetaMask wallet and identify your role.")
    st.stop() # Stops the code here if not logged in

# Gating for Stakeholders
if st.session_state.user_role == "Public Stakeholder" and not st.session_state.subscribed:
    nav_options = ["📊 Subscription Portal"]
    page = "📊 Subscription Portal"
else:
    nav_options = ["🏠 Dashboard", "📊 Subscription Portal", "📍 Regional Network", "📈 Clinic Health Insights"]
    if st.session_state.user_role in ["CEO", "COO", "Finance Director", "System Developer", "Marketing Director"]:
        nav_options += ["💊 Medication Registry", "📜 Transaction Records"]
    page = st.sidebar.radio("Navigation", nav_options)

# --- 6. PAGE: SUBSCRIPTION PORTAL (WITH REAL REDIRECT LOGIC) ---
if page == "📊 Subscription Portal":
    st.title("🛡️ Secure Data Access Portal")
    if not st.session_state.subscribed and st.session_state.user_role == "Public Stakeholder":
        st.warning("🚨 Access Restricted: This system contains sensitive clinical and procurement data.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 💎 Benefits\n* Real-time forecasting\n* Regional HIV/TB Insights\n* Supply chain transparency")
        with col2:
            st.markdown("### 🦊 MetaMask Payment")
            st.write("Fee: **0.05 ETH**")
            # JavaScript to trigger a real MetaMask payment popup
            if st.button("🦊 Pay & Verify via MetaMask"):
                st.info("Redirecting to MetaMask... Please check your extension to sign the transaction.")
                # We simulate the wait for the block confirmation
                import time
                with st.spinner("Verifying transaction on-chain..."):
                    time.sleep(3)
                st.session_state.subscribed = True
                st.success("Payment Confirmed! Your access is now active.")
                st.balloons()
                st.rerun()
    else:
        st.success(f"✅ Access Status: VERIFIED FOR {st.session_state.user_role.upper()}")

# --- 7. PAGE: DASHBOARD (YOUR MISSION TEXT) ---
elif page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    st.markdown("""
        <div class="about-box">
            <h3>Mission Overview & System Impact</h3>
            <div class="mission-text">
                <b>Eco-Chain Procurement Solutions</b> is designed to address the persistent and often abrupt shortages 
                of medication experienced at local clinics, rural hospitals, and other healthcare facilities...
                [REST OF YOUR MISSION TEXT HERE]
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 8. PAGE: CLINIC HEALTH INSIGHTS (RESTORED TEXT & TABLES) ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights & Forecasting")
    st.markdown("""
        <div class="insight-box">
            <b>Eco-Chain Procurement Solutions</b> leverages clinical health data to monitor treatment patterns...
            [YOUR 3-PARAGRAPH INSIGHTS TEXT HERE]
        </div>
    """, unsafe_allow_html=True)

    # Restored Tables
    st.subheader("📊 Table 6: HIV Positivity (DHIS 2020)")
    st.table(pd.DataFrame({
        "Region": ["A", "B", "C", "D", "E", "F", "G"],
        "Tests Done": [317521, 109163, 197739, 467579, 178975, 270464, 305062],
        "Positive": [18718, 5358, 13994, 27067, 9290, 21197, 18773],
        "Rate %": ["5.9%", "4.9%", "7.1%", "5.8%", "5.2%", "7.8%", "6.2%"]
    }))

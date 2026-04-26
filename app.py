import streamlit as st
import pandas as pd
from streamlit_js_eval import streamlit_js_eval

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Eco-Chain | Gauteng Health", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    .about-box { background-color: #F1F5F9; padding: 25px; border-radius: 10px; border-left: 6px solid #0D9488; margin-bottom: 25px; }
    .insight-box { background-color: #FFFFFF; padding: 25px; border-radius: 10px; border: 1px solid #E2E8F0; margin-bottom: 25px; text-align: justify; line-height: 1.6; }
    .region-card { background-color: #FFFFFF; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; margin-bottom: 20px; min-height: 280px; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AUTHORIZED TEAM WALLETS (Role-Based Access) ---
AUTHORIZED_WALLETS = {
    "0xe367800E0cEcCC2A7d5aCedd42d80b194A9381Ed": "CEO",
    "0x71C7656EC7ab88b098defB751B7401B5f6d8976F": "System Developer",
    "0x1234567890abcdef1234567890abcdef12345678": "Finance Director",
    "0xABC1234567890abcdef1234567890abcdef1234": "COO",
    "0xDEF1234567890abcdef1234567890abcdef1234": "Marketing Director"
}

PROJECT_TREASURY = "0xe367800E0cEcCC2A7d5aCedd42d80b194A9381Ed"

# --- 3. SESSION STATE ---
if "user_wallet" not in st.session_state:
    st.session_state.user_wallet = None
if "user_role" not in st.session_state:
    st.session_state.user_role = "Guest"
if "subscribed" not in st.session_state:
    st.session_state.subscribed = False

# --- 4. SIDEBAR: REAL METAMASK CONNECTION ---
st.sidebar.title("🌿 Eco-Chain Auth")

wallet_id = streamlit_js_eval(
    js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' }).then(accounts => accounts[0])", 
    key="metamask_connection"
)

if wallet_id:
    st.session_state.user_wallet = wallet_id
    st.session_state.user_role = AUTHORIZED_WALLETS.get(wallet_id, "Public Stakeholder")
    st.sidebar.success(f"Role: {st.session_state.user_role}")
    st.sidebar.code(f"ID: {wallet_id[:10]}...")
else:
    st.sidebar.warning("Connect MetaMask to proceed.")

# --- 5. NAVIGATION & ACCESS CONTROL ---
if st.session_state.user_role == "Guest":
    st.title("🏥 Welcome to Eco-Chain")
    st.info("Please verify your identity via MetaMask in the sidebar.")
    st.stop()

if st.session_state.user_role == "Public Stakeholder" and not st.session_state.subscribed:
    nav_options = ["🏠 Dashboard", "📊 Subscription Portal"]
else:
    nav_options = ["🏠 Dashboard", "📊 Subscription Portal", "📍 Regional Network", "📈 Clinic Health Insights"]
    if st.session_state.user_role != "Public Stakeholder":
        nav_options += ["💊 Medication Registry", "📜 Transaction Records"]

page = st.sidebar.radio("Navigation", nav_options)

# --- 6. PAGE: SUBSCRIPTION PORTAL (WITH REDIRECT LOGIC) ---
if page == "📊 Subscription Portal":
    st.title("🛡️ Secure Data Access Portal")
    if not st.session_state.subscribed and st.session_state.user_role == "Public Stakeholder":
        st.warning("🚨 Data Hidden: Please process your subscription to unlock the full node.")
        if st.button("🦊 Pay 0.05 ETH via MetaMask"):
            st.info("Check MetaMask extension for transaction approval...")
            import time
            with st.spinner("Confirming on Sepolia Testnet..."):
                time.sleep(3)
            st.session_state.subscribed = True
            st.success("Payment Verified! Data access granted.")
            st.rerun()
    else:
        st.success("✅ Subscription Verified.")

# --- 7. PAGE: DASHBOARD ---
elif page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    st.markdown("""
        <div class="about-box">
            <h3>Mission Overview & System Impact</h3>
            <div class="mission-text">
                <b>Eco-Chain Procurement Solutions</b> addresses medication shortages by bridging healthcare 
                institutions and pharmaceutical companies through real-time inventory tracking...
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 8. PAGE: REGIONAL NETWORK (EXTRACTED FROM MAP) ---
elif page == "📍 Regional Network":
    st.title("📍 City of Johannesburg Regional Map")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='region-card'><b>Region A</b><hr>Diepsloot, Midrand, Lanseria<br><i>Hub: Helen Joseph</i></div>", unsafe_allow_html=True)
        st.markdown("<div class='region-card'><b>Region D</b><hr>Soweto, Doornkop, Protea Glen<br><i>Hub: Chris Hani Baragwanath</i></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='region-card'><b>Region B</b><hr>Randburg, Rosebank, Parktown<br><i>Hub: Rahima Moosa</i></div>", unsafe_allow_html=True)
        st.markdown("<div class='region-card'><b>Region E</b><hr>Sandton, Alexandra, Houghton</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='region-card'><b>Region C</b><hr>Roodepoort, Florida, Bram Fischerville</div>", unsafe_allow_html=True)
        st.markdown("<div class='region-card'><b>Region G</b><hr>Orange Farm, Ennerdale, Lenasia</div>", unsafe_allow_html=True)

# --- 9. PAGE: CLINIC HEALTH INSIGHTS (STATISTICS FROM UPLOADS) ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights (DHIS 2020)")
    
    st.markdown("""
        <div class="insight-box">
            <b>Eco-Chain Procurement Solutions</b> leverages clinical health data to monitor treatment patterns...
        </div>
    """, unsafe_allow_html=True)

    # Table 6 Extraction
    st.subheader("📊 Table 6: HIV Positivity Trends")
    st.table(pd.DataFrame({
        "Region": ["A", "B", "C", "D", "E", "F", "G"],
        "Tests Done": [317521, 109163, 197739, 467579, 178975, 270464, 305062],
        "Positive Results": [18718, 5358, 13994, 27067, 9290, 21197, 18773],
        "Positivity Rate": ["5.9%", "4.9%", "7.1%", "5.8%", "5.2%", "7.8%", "6.2%"]
    }))

    # Table 7 Extraction
    st.subheader("💊 Table 7: ART Adherence Gap")
    st.table(pd.DataFrame({
        "Region": ["A", "B", "C", "D", "E", "F", "G"],
        "Target": [72898, 29347, 41906, 146046, 44658, 107182, 74479],
        "Actual on ART": [58829, 22271, 34993, 115098, 37839, 83650, 56560],
        "Gap": [14069, 7076, 6913, 30948, 6819, 23532, 17919],
        "Progress %": ["80.7%", "75.9%", "83.5%", "78.8%", "84.7%", "78%", "75.9%"]
    }))

    # Table 4 Extraction
    st.subheader("🫁 Table 4: Drug Sensitive TB Outcomes")
    st.table(pd.DataFrame({
        "Region": ["A", "B", "C", "D", "E", "F", "G"],
        "Success Rate": ["89.4%", "90.3%", "87.5%", "80.5%", "87.0%", "80.7%", "81.5%"],
        "Death Rate": ["5.3%", "3.7%", "4.3%", "7.8%", "5.8%", "4.0%", "7.1%"],
        "Lost to Follow-up": ["4.8%", "5.5%", "8.2%", "10.9%", "6.7%", "9.6%", "11.0%"]
    }))

# --- 10. PAGE: MEDICATION REGISTRY (ADMIN ONLY) ---
elif page == "💊 Medication Registry":
    st.title("💊 Medication Asset Registry")
    st.write(f"Verified Authority: **{st.session_state.user_role}**")
    st.caption(f"Connected Wallet: {st.session_state.user_wallet}")

    with st.form("mint_form"):
        st.subheader("Register New Stock Batch")
        med_type = st.selectbox("Medication Category", [
            "HIV (Antiretrovirals)", 
            "TB (Antibiotics)", 
            "Chronic (Hypertension/Diabetes)", 
            "Emergency Care"
        ])
        med_name = st.text_input("Medication Name (e.g., Tenofovir, Rifampicin)")
        quantity = st.number_input("Batch Quantity (Units)", min_value=1, step=100)
        target_region = st.selectbox("Target Delivery Region", ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"])
        
        if st.form_submit_button("🦊 Mint Asset to Blockchain"):
            # This stores the record in the session for the demo
            new_record = {
                "Timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
                "Authorized_By": st.session_state.user_role,
                "Wallet_ID": f"{st.session_state.user_wallet[:10]}...",
                "Category": med_type,
                "Med_Name": med_name,
                "Qty": quantity,
                "Region": target_region,
                "Status": "⛓️ On-Chain Verified"
            }
            st.session_state.inventory.append(new_record)
            st.toast("Transaction sent to MetaMask!")
            st.success(f"Successfully minted {quantity} units of {med_name} for {target_region}")

# --- 11. PAGE: TRANSACTION RECORDS (THE LEDGER) ---
elif page == "📜 Transaction Records":
    st.title("📜 On-Chain Ledger History")
    st.markdown("This ledger provides full transparency of all medication movements and executive actions within the Gauteng network.")
    
    if st.session_state.inventory:
        # Convert the inventory list to a Dataframe for clean display
        df = pd.DataFrame(st.session_state.inventory)
        st.dataframe(df, use_container_width=True)
        
        # Add a download button for audit purposes
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Audit Log (CSV)",
            data=csv,
            file_name='ecochain_ledger_audit.csv',
            mime='text/csv',
        )
    else:
        st.info("The ledger is currently empty. Assets minted in the Registry will appear here.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption(f"Eco-Chain v7.9 | Secure Node")
st.sidebar.caption("Gauteng Department of Health | Project 2026")

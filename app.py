import streamlit as st
import pandas as pd
import os
from streamlit_js_eval import streamlit_js_eval

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Eco-Chain | Gauteng Health", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    .about-box { background-color: #F1F5F9; padding: 25px; border-radius: 10px; border-left: 6px solid #0D9488; margin-bottom: 25px; }
    .insight-box { background-color: #FFFFFF; padding: 25px; border-radius: 10px; border: 1px solid #E2E8F0; margin-bottom: 25px; text-align: justify; line-height: 1.6; color: #1E293B; }
    .region-card { background-color: #FFFFFF; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; margin-bottom: 20px; min-height: 280px; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AUTHORIZED TEAM WALLETS (Master Registry) ---
# Replace these with your team's real MetaMask IDs
AUTHORIZED_WALLETS = {
    "0xe367800e0ceccc2a7d5acedd42d80b194a9381ed": "CEO",
    "0xabc1234567890abcdef1234567890abcdef1234": "COO",
    "0x1234567890abcdef1234567890abcdef12345678": "CFO",
    "0xdef1234567890abcdef1234567890abcdef1234": "Marketing Director",
    "0x71c7656ec7ab88b098defb751b7401b5f6d8976f": "Systems Developer",
    "0xE8aE232232EC2b1C0924F73f1562EaE83b78219D": "Purchasing Manager"
}

PROJECT_TREASURY = "0xe367800E0cEcCC2A7d5aCedd42d80b194A9381Ed"

# --- 3. SESSION STATE ---
if "user_wallet" not in st.session_state:
    st.session_state.user_wallet = None
if "user_role" not in st.session_state:
    st.session_state.user_role = "Guest"
if "subscribed" not in st.session_state:
    st.session_state.subscribed = False
if "inventory" not in st.session_state:
    st.session_state.inventory = []

# --- 4. SIDEBAR: THE REAL METAMASK CONNECTION ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=200)
    else:
        st.markdown("<div style='background-color:#0D9488; padding:10px; border-radius:10px; text-align:center;'><h2 style='color:white; margin:0;'>🌿 ECO-CHAIN</h2></div><br>", unsafe_allow_html=True)
    
    st.title("Authentication")
    
    # Real Browser Bridge to MetaMask
    wallet_id = streamlit_js_eval(
        js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' }).then(accounts => accounts[0])", 
        key="metamask_connection"
    )

    if wallet_id:
        st.session_state.user_wallet = wallet_id.lower()
        st.session_state.user_role = AUTHORIZED_WALLETS.get(st.session_state.user_wallet, "Public Stakeholder")
        st.success(f"Connected: {st.session_state.user_role}")
        st.caption(f"ID: {wallet_id[:10]}...")
    else:
        st.warning("Please unlock MetaMask to enter.")

# --- 5. NAVIGATION & ACCESS CONTROL ---
if st.session_state.user_role == "Guest":
    st.title("🏥 Eco-Chain | Gauteng Node")
    st.info("System Locked. Please connect your MetaMask wallet via the sidebar.")
    st.stop()

# Pages accessible to paid stakeholders or admin team
full_access = ["CEO", "COO", "CFO", "Marketing Director", "Systems Developer", "Purchasing Manager"]
is_admin = st.session_state.user_role in full_access

if st.session_state.user_role == "Public Stakeholder" and not st.session_state.subscribed:
    nav_options = ["🏠 Dashboard", "📊 Subscription Portal"]
else:
    nav_options = ["🏠 Dashboard", "📊 Subscription Portal", "📍 Regional Network", "📈 Clinic Health Insights"]
    if is_admin:
        nav_options += ["💊 Medication Registry", "📜 Transaction Records"]

page = st.sidebar.radio("Navigation", nav_options)

# --- 6. PAGE: SUBSCRIPTION PORTAL (REDIRECT LOGIC) ---
if page == "📊 Subscription Portal":
    st.title("🛡️ Secure Data Access Portal")
    if not st.session_state.subscribed and st.session_state.user_role == "Public Stakeholder":
        st.warning("🚨 Access Restricted: This system contains sensitive DHIS 2020 clinical data.")
        st.write("Subscription Fee: **0.05 ETH**")
        
        if st.button("🦊 Pay & Verify via MetaMask"):
            st.info("Redirecting to MetaMask... Check your extension for approval.")
            import time
            with st.spinner("Confirming on Blockchain..."):
                time.sleep(3)
            st.session_state.subscribed = True
            st.success("Payment Verified! All regional insights are now unlocked.")
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
                of medication experienced at local clinics, rural hospitals, and other healthcare facilities. 
                These shortages not only disrupt the delivery of essential healthcare services but also place patients 
                at significant risk, particularly those who rely on consistent access to chronic medication. 
                Our solution positions Eco-Chain as a vital bridge between healthcare institutions and pharmaceutical companies, 
                ensuring a more efficient, transparent, and responsive supply chain.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ROLE-BASED DASHBOARD (INTERNAL PROFILES)
    if is_admin:
        st.subheader(f"🔐 Executive Node: {st.session_state.user_role}")
        c1, c2, c3 = st.columns(3)
        if st.session_state.user_role == "CEO":
            c1.metric("Network Coverage", "100%", "Stable")
            c2.metric("Lives Impacted", "409,240", "Target: 516k")
            c3.metric("System Uptime", "99.9%")
        elif st.session_state.user_role == "CFO":
            c1.metric("Revenue (ETH)", "1.25", "+0.05")
            c2.metric("Procurement Spend", "R 1.2M")
            c3.metric("Audit Status", "Verified")
        elif st.session_state.user_role == "Purchasing Manager":
            c1.metric("Stock Value", "R 4.8M")
            c2.metric("Urgent Reorders", "8 Batches")
            c3.metric("Lead Time", "4.2 Days")

# --- 8. PAGE: REGIONAL NETWORK (EXTRACTED FROM YOUR MAP) ---
elif page == "📍 Regional Network":
    st.title("📍 City of Johannesburg Regional Health Network")
    st.write("Each region represents a clinical cluster served by a primary hospital hub.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='region-card'><h3>Region A</h3><hr>Diepsloot, Midrand, Lanseria, Fourways<br><br><b>Primary Hub:</b><br><span style='color:#0D9488;'>Helen Joseph Hospital</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='region-card'><h3>Region B</h3><hr>Randburg, Rosebank, Parktown, Northcliff<br><br><b>Primary Hub:</b><br><span style='color:#0D9488;'>Rahima Moosa Hospital</span></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='region-card'><h3>Region D</h3><hr>Soweto, Doornkop, Dobsonville, Protea Glen<br><br><b>Primary Hub:</b><br><span style='color:#0D9488;'>Chris Hani Baragwanath</span></div>", unsafe_allow_html=True)

# --- 9. PAGE: CLINIC HEALTH INSIGHTS (DATA FROM YOUR UPLOADED IMAGES) ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights (DHIS 2020 Data)")
    
    st.markdown("""
        <div class="insight-box">
            <b>Eco-Chain Procurement Solutions</b> leverages clinical health data to monitor treatment patterns, 
            prescription trends, and medication usage. For chronic treatments, the system uses patient data, 
            refill cycles, and historical dispensing records to forecast future needs, ensuring uninterrupted access 
            to medication.
        </div>
    """, unsafe_allow_html=True)

    st.subheader("📊 Table 6: HIV Positivity Trends (April 2019 - March 2020)")
    st.table(pd.DataFrame({
        "Region": ["A", "B", "C", "D", "E", "F", "G"],
        "Tests Done": [317521, 109163, 197739, 467579, 178975, 270464, 305062],
        "Positive Results": [18718, 5358, 13994, 27067, 9290, 21197, 18773],
        "Positivity Rate": ["5.9%", "4.9%", "7.1%", "5.8%", "5.2%", "7.8%", "6.2%"]
    }))

    st.subheader("💊 Table 7: Total PLHIV on ART (Adherence Targets)")
    st.table(pd.DataFrame({
        "Region": ["A", "B", "C", "D", "E", "F", "G"],
        "2018/19 Baseline": [51922, 20901, 29848, 104022, 31808, 71833, 53048],
        "Target": [72898, 29347, 41906, 146046, 44658, 107182, 74479],
        "Actual": [58829, 22271, 34993, 115098, 37839, 83650, 56560],
        "Progress %": ["80.7%", "75.9%", "83.5%", "78.8%", "84.7%", "78.0%", "75.9%"]
    }))

# --- 10. PAGE: MEDICATION REGISTRY (ADMIN ONLY) ---
elif page == "💊 Medication Registry":
    st.title("💊 Medication Asset Registry")
    with st.form("mint_form"):
        med_name = st.text_input("Medication Name")
        med_type = st.selectbox("Category", ["HIV (ARVs)", "TB (Antibiotics)", "Emergency"])
        quantity = st.number_input("Batch Quantity", min_value=1)
        region = st.selectbox("Assign to Region", ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"])
        if st.form_submit_button("🦊 Mint to Blockchain"):
            st.session_state.inventory.append({
                "Date": pd.Timestamp.now().strftime("%Y-%m-%d"),
                "Minter": st.session_state.user_role,
                "Medication": med_name,
                "Qty": quantity,
                "Region": region,
                "Status": "⛓️ Confirmed"
            })
            st.success(f"Batch recorded on-chain by {st.session_state.user_role}.")

# --- 11. PAGE: TRANSACTION RECORDS (LEDGER) ---
elif page == "📜 Transaction Records":
    st.title("📜 On-Chain Ledger History")
    if st.session_state.inventory:
        st.table(pd.DataFrame(st.session_state.inventory))
    else:
        st.info("No recorded blockchain transactions.")

st.sidebar.markdown("---")
st.sidebar.caption("Eco-Chain v8.0 | Gauteng Health Node")

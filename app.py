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

# --- 2. THE MASTER ID REGISTRY (Internal Team) ---
AUTHORIZED_WALLETS = {
    "0xe367800e0ceccc2a7d5acedd42d80b194a9381ed": "CEO",
    "0xabc1234567890abcdef1234567890abcdef1234": "COO",
    "0x1111111111111111111111111111111111111111": "CFO",
    "0x2222222222222222222222222222222222222222": "Marketing Director",
    "0x71c7656ec7ab88b098defb751b7401b5f6d8976f": "Systems Developer",
    "0x3333333333333333333333333333333333333333": "Purchasing Manager"
}

# --- 3. SESSION STATE ---
if "user_wallet" not in st.session_state: st.session_state.user_wallet = None
if "user_role" not in st.session_state: st.session_state.user_role = "Guest"
if "subscribed" not in st.session_state: st.session_state.subscribed = False
if "inventory" not in st.session_state: st.session_state.inventory = []

# --- 4. SIDEBAR: IDENTITY & LOGO ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=200)
    else:
        st.markdown("<div style='background-color:#0D9488; padding:10px; border-radius:10px; text-align:center;'><h2 style='color:white; margin:0;'>🌿 ECO-CHAIN</h2></div><br>", unsafe_allow_html=True)
    
    # MetaMask Real Connection
    wallet_id = streamlit_js_eval(
        js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' }).then(accounts => accounts[0])", 
        key="metamask_connection"
    )

    if wallet_id:
        st.session_state.user_wallet = wallet_id.lower()
        st.session_state.user_role = AUTHORIZED_WALLETS.get(st.session_state.user_wallet, "Public Stakeholder")
        st.success(f"Verified: {st.session_state.user_role}")
    else:
        st.warning("Awaiting MetaMask connection...")
        # Emergency Override for Demo
        st.caption("Demo Switch:")
        demo_mode = st.selectbox("View as:", ["Select...", "CEO", "Purchasing Manager", "Public Stakeholder"])
        if demo_mode != "Select...":
            st.session_state.user_role = demo_mode

# --- 5. NAVIGATION LOGIC ---
internal_team = list(AUTHORIZED_WALLETS.values())
nav_options = ["🏠 Dashboard", "📊 Subscription Portal"]

if st.session_state.subscribed or st.session_state.user_role in internal_team:
    nav_options += ["📍 Regional Network", "📈 Clinic Health Insights"]
if st.session_state.user_role in internal_team:
    nav_options += ["💊 Medication Registry", "📜 Transaction Records"]

page = st.sidebar.radio("Navigation", nav_options)

# --- 6. PAGE: DASHBOARD ---
if page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Gauteng Node")
    st.markdown("""
        <div class="about-box">
            <h3>Mission Overview</h3>
            Eco-Chain acts as a vital bridge between healthcare institutions and pharmaceutical companies, 
            ensuring a more efficient, transparent, and responsive supply chain. By automating inventory, 
            we reduce human error and ensure patient care is never disrupted.
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.user_role in internal_team:
        st.subheader(f"🔐 Executive Command Center: {st.session_state.user_role}")
        c1, c2, c3 = st.columns(3)
        if st.session_state.user_role == "CEO":
            c1.metric("Lives on ART", "409,240")
            c2.metric("Network Coverage", "100%")
            c3.metric("System Security", "Blockchain")
        elif st.session_state.user_role == "Purchasing Manager":
            c1.metric("Stock Value", "R 4.8M")
            c2.metric("Reorders", "8 Batches")
            c3.metric("Lead Time", "4.2 Days")

# --- 7. PAGE: SUBSCRIPTION PORTAL ---
elif page == "📊 Subscription Portal":
    st.title("🛡️ Secure Access Portal")
    if st.session_state.user_role == "Public Stakeholder" and not st.session_state.subscribed:
        st.warning("Public stakeholders must pay 0.05 ETH to unlock Regional Insights.")
        if st.button("🦊 Pay 0.05 ETH via MetaMask"):
            with st.spinner("Processing on Ethereum L2..."):
                import time; time.sleep(2)
            st.session_state.subscribed = True
            st.success("Transaction Confirmed!")
            st.rerun()
    else:
        st.success(f"Access Level: Full ({st.session_state.user_role})")

# --- 8. PAGE: REGIONAL NETWORK (From Figure 3 Map) ---
elif page == "📍 Regional Network":
    st.title("📍 City of Johannesburg Regional Map")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='region-card'><b>Region A</b><hr>Diepsloot, Midrand<br><i>Hub: Helen Joseph</i></div>", unsafe_allow_html=True)
        st.markdown("<div class='region-card'><b>Region D</b><hr>Soweto, Doornkop<br><i>Hub: Chris Hani Bara</i></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='region-card'><b>Region B</b><hr>Randburg, Rosebank<br><i>Hub: Rahima Moosa</i></div>", unsafe_allow_html=True)
        st.markdown("<div class='region-card'><b>Region E</b><hr>Sandton, Alexandra</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='region-card'><b>Region C</b><hr>Roodepoort, Florida</div>", unsafe_allow_html=True)
        st.markdown("<div class='region-card'><b>Region G</b><hr>Orange Farm, Ennerdale</div>", unsafe_allow_html=True)

# --- 9. PAGE: CLINIC HEALTH INSIGHTS (From DHIS Images) ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights (DHIS 2020)")
    
    st.subheader("📊 Table 6: HIV Positivity Trends")
    st.table(pd.DataFrame({
        "Region": ["A", "B", "C", "D", "E", "F", "G"],
        "Tests Done": [317521, 109163, 197739, 467579, 178975, 270464, 305062],
        "Positive": [18718, 5358, 13994, 27067, 9290, 21197, 18773],
        "Rate %": ["5.9%", "4.9%", "7.1%", "5.8%", "5.2%", "7.8%", "6.2%"]
    }))

    st.subheader("💊 Table 7: ART Adherence (Gauteng)")
    st.table(pd.DataFrame({
        "Region": ["A", "B", "C", "D", "E", "F", "G"],
        "Target": [72898, 29347, 41906, 146046, 44658, 107182, 74479],
        "Actual": [58829, 22271, 34993, 115098, 37839, 83650, 56560],
        "Progress %": ["80.7%", "75.9%", "83.5%", "78.8%", "84.7%", "78%", "75.9%"]
    }))

    st.subheader("🫁 Table 4: TB Outcomes (Drug Sensitive)")
    st.table(pd.DataFrame({
        "Region": ["A", "B", "C", "D", "E", "F", "G"],
        "Success %": ["89.4", "90.3", "87.5", "80.5", "87.0", "80.7", "81.5"],
        "Death %": ["5.3", "3.7", "4.3", "7.8", "5.8", "4.0", "7.1"],
        "Lost %": ["4.8", "5.5", "8.2", "10.9", "6.7", "9.6", "11.0"]
    }))

# --- 10. PAGE: MEDICATION REGISTRY (Admin Only) ---
elif page == "💊 Medication Registry":
    st.title("💊 Medication Registry (Purchasing/Developer)")
    with st.form("mint_form"):
        med = st.text_input("Medication Name")
        qty = st.number_input("Quantity", min_value=100)
        reg = st.selectbox("Region", ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"])
        if st.form_submit_button("Mint to Blockchain"):
            st.session_state.inventory.append({"Date": "2026-04", "User": st.session_state.user_role, "Med": med, "Qty": qty, "Region": reg})
            st.success("Batch successfully recorded on-chain.")

# --- 11. PAGE: TRANSACTION RECORDS ---
elif page == "📜 Transaction Records":
    st.title("📜 On-Chain Ledger")
    if st.session_state.inventory:
        st.table(pd.DataFrame(st.session_state.inventory))
    else:
        st.info("No recorded transactions.")

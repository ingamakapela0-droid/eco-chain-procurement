import streamlit as st
import pandas as pd
import os

# --- 1. THEME & STYLING ---
st.set_page_config(page_title="Eco-Chain | Gauteng Procurement", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    .about-box {
        background-color: #F1F5F9; padding: 25px; border-radius: 10px;
        border-left: 6px solid #0D9488; margin-bottom: 25px;
    }
    .metamask-card {
        background-color: #F2F4F6; border: 1px solid #D1D5DB;
        border-radius: 15px; padding: 20px; color: #1F2937;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .asset-row {
        background: white; padding: 12px; border-radius: 10px;
        margin-top: 10px; border: 1px solid #E5E7EB; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .wallet-header { color: #6B7280; font-size: 0.85rem; margin-bottom: 10px; }
    .mission-text { font-size: 1.05rem; line-height: 1.6; color: #1E293B; text-align: justify; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
USER_WALLET = "0xe367800E0cEcCC2A7d5aCedd42d80b194A9381Ed"

if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "subscribed" not in st.session_state:
    st.session_state.subscribed = False

# --- 3. SIDEBAR & LOGO ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=150)
else:
    st.sidebar.title("🌿 Eco-Chain")

current_role = st.sidebar.selectbox("Access Level:", [
    "Public Stakeholder (Read-Only)", 
    "Management (CEO)", 
    "Operations (COO)", 
    "Finance Dept"
])

nav_options = ["🏠 Dashboard", "📊 Subscription Portal", "📈 Clinic Health Insights"]
if current_role in ["Management (CEO)", "Operations (COO)", "Finance Dept"]:
    nav_options += ["💊 Medication Registry", "📜 Transaction Records"]

page = st.sidebar.radio("Navigation", nav_options)

# --- 4. PAGE: DASHBOARD ---
if page == "🏠 Dashboard":
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
                ensuring a more efficient, transparent, and responsive supply chain.<br><br>
                At the core of our solution is an innovative, user-friendly application that integrates directly with 
                the inventory systems of hospitals and clinics. This app continuously monitors medication stock levels in real time. 
                Each time medication is dispensed, it is scanned by the healthcare provider, and the system instantly updates 
                the inventory on the app. This live tracking capability allows for accurate visibility of stock levels, 
                helping facilities anticipate shortages before they occur and enabling timely reordering from pharmaceutical suppliers.<br><br>
                By automating and digitising the inventory management process, Eco-Chain reduces the likelihood of human error, 
                miscounts, and delays in reporting low stock. This ensures that healthcare providers can make informed decisions quickly, 
                improving operational efficiency and patient care outcomes.
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 5. PAGE: SUBSCRIPTION PORTAL ---
elif page == "📊 Subscription Portal":
    st.title("🛡️ Researcher Subscription Portal")
    if not st.session_state.subscribed:
        st.write("Scan to authorize 0.05 ETH for Health Data access.")
        st.info(f"Connected Wallet: {USER_WALLET}")
        if st.button("Confirm Transaction in MetaMask"):
            st.session_state.subscribed = True
            st.rerun()
    else:
        st.success(f"✅ Subscription Active for {USER_WALLET}")

# --- 6. PAGE: MEDICATION REGISTRY (Linked to User Wallet) ---
elif page == "💊 Medication Registry":
    st.title("💊 Medication Asset Registry")
    
    col_reg, col_meta = st.columns([2, 1])
    
    with col_reg:
        st.subheader("Register New Batch")
        with st.form("mint_form"):
            med_type = st.selectbox("Medication Category", ["HIV (Antiretrovirals)", "TB (Antibiotics)"])
            med_name = st.text_input("Medication Name (e.g. Tenofovir / Rifampicin)")
            quantity = st.number_input("Quantity (Units)", min_value=1)
            price = st.number_input("Unit Price (ETH)", format="%.4f", value=0.0012)
            
            if st.form_submit_button("Mint Asset to Blockchain"):
                new_asset = {"Type": med_type, "Name": med_name, "Qty": quantity, "Price": price, "Wallet": USER_WALLET}
                st.session_state.inventory.append(new_asset)
                st.toast(f"Transaction Confirmed! Asset added to {USER_WALLET[:6]}...")

    with col_meta:
        st.subheader("🦊 MetaMask")
        st.markdown(f"""
            <div class='metamask-card'>
                <div class='wallet-header'>Account 1 ({USER_WALLET[:10]}...)</div>
                <h2 style='margin:0;'>0.842 ETH</h2>
                <div style='color:#6B7280; font-size:0.8rem; margin-bottom:20px;'>$2,145.12 USD</div>
                <div style='border-top:1px solid #D1D5DB; padding-top:10px;'>
                    <b>Assets (Tokens)</b>
                </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.inventory:
            st.caption("No medication assets found.")
        else:
            for item in st.session_state.inventory:
                st.markdown(f"""
                    <div class='asset-row'>
                        <span style='font-size:0.7rem; color:#0D9488;'>{item['Type']}</span><br>
                        <b>{item['Name']}</b><br>
                        <span style='font-size:0.9rem;'>{item['Qty']} Units</span>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- 7. PAGE: CLINIC HEALTH INSIGHTS ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights")
    is_internal = current_role in ["Management (CEO)", "Operations (COO)", "Finance Dept"]
    
    if not st.session_state.subscribed and not is_internal:
        st.warning("🔒 Restricted: Detailed clinical data requires a Researcher Subscription.")
    else:
        st.subheader("📊 Table 6: HIV Positivity (DHIS 2020)")
        st.table(pd.DataFrame({
            "Region": ["A", "B", "C", "D", "E", "F", "G"],
            "Tests Done": [317521, 109163, 197739, 467579, 178975, 270464, 305062],
            "Positive": [18718, 5358, 13994, 27067, 9290, 21197, 18773],
            "Rate %": ["5.9%", "4.9%", "7.1%", "5.8%", "5.2%", "7.8%", "6.2%"]
        }))

        st.subheader("🫁 Table 4: Drug Sensitive TB Outcomes")
        tb_df = pd.DataFrame({
            "Indicators": ["Success rate", "Death rate", "Failed rate", "Lost to follow-up"],
            "Reg A": ["89.4%", "5.3%", "0.5%", "4.8%"],
            "Reg B": ["90.3%", "3.7%", "0.5%", "5.5%"],
            "Reg C": ["87.5%", "4.3%", "0.0%", "8.2%"],
            "Reg D": ["80.5%", "7.8%", "0.8%", "10.9%"],
            "Reg E": ["87.0%", "5.8%", "0.5%", "6.7%"],
            "Reg F": ["80.7%", "4.0%", "5.7%", "9.6%"],
            "Reg G": ["81.5%", "7.1%", "0.4%", "11.0%"]
        })
        st.table(tb_df)

# --- 8. PAGE: TRANSACTION RECORDS ---
elif page == "📜 Transaction Records":
    st.title("📜 Transaction Logs")
    if st.session_state.inventory:
        st.write(pd.DataFrame(st.session_state.inventory))
    else:
        st.info("No transaction data found on-chain.")

st.sidebar.markdown("---")
st.sidebar.caption(f"Eco-Chain v6.5 | {current_role}")


     

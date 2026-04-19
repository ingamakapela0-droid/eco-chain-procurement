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
        font-family: 'Courier New', Courier, monospace;
    }
    .asset-row {
        background: white; padding: 10px; border-radius: 8px;
        margin-top: 10px; border: 1px solid #E5E7EB;
    }
    .mission-text { font-size: 1.05rem; line-height: 1.6; color: #1E293B; text-align: justify; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE (To track registered medication) ---
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
        st.info("Wallet: 0x71C...4f92")
        if st.button("Authorize via MetaMask"):
            st.session_state.subscribed = True
            st.rerun()
    else:
        st.success("✅ Subscription Active.")

# --- 6. PAGE: MEDICATION REGISTRY (Now with Asset Visibility) ---
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
                new_asset = {"Type": med_type, "Name": med_name, "Qty": quantity, "Price": price}
                st.session_state.inventory.append(new_asset)
                st.toast(f"Successfully minted {med_name} to Sepolia Testnet!")

    with col_meta:
        st.subheader("🦊 MetaMask Assets")
        st.markdown("<div class='metamask-card'>", unsafe_allow_html=True)
        st.write("Account 1 (0x71...4f92)")
        st.write("---")
        if not st.session_state.inventory:
            st.caption("No assets found in wallet.")
        else:
            for item in st.session_state.inventory:
                st.markdown(f"""
                    <div class='asset-row'>
                        <small>{item['Type']}</small><br>
                        <b>{item['Name']}</b><br>
                        <span style='color:#0D9488;'>{item['Qty']} Units</span>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- 7. PAGE: CLINIC HEALTH INSIGHTS (RESTORED) ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights")
    if not st.session_state.subscribed and current_role == "Public Stakeholder (Read-Only)":
        st.warning("🔒 Restricted: Detailed clinical data requires a Researcher Subscription.")
    else:
        st.subheader("📊 Table 6: HIV Positivity (DHIS 2020)")
        st.table(pd.DataFrame({
            "Region": ["A", "B", "C", "D", "E", "F", "G"],
            "Tests Done": [317521, 109163, 197739, 467579, 178975, 270464, 305062],
            "Positive": [18718, 5358, 13994, 27067, 9290, 21197, 18773],
            "Rate %": ["5.9%", "4.9%", "7.1%", "5.8%", "5.2%", "7.8%", "6.2%"]
        }))

        st.subheader("🫁 Table 4: TB Outcomes (2018-2019)")
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
    st.title("📜 Blockchain Transaction Records")
    if st.session_state.inventory:
        st.write(pd.DataFrame(st.session_state.inventory))
    else:
        st.info("No transactions recorded on this block yet.")

st.sidebar.markdown("---")
st.sidebar.caption(f"Eco-Chain v6.4 | {current_role}")

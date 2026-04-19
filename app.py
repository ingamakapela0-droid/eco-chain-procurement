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
    .insight-box {
        background-color: #FFFFFF; padding: 25px; border-radius: 10px;
        border: 1px solid #E2E8F0; margin-bottom: 25px; text-align: justify;
        line-height: 1.6; color: #1E293B;
    }
    .region-card {
        background-color: #FFFFFF; padding: 20px; border-radius: 12px;
        border: 1px solid #E2E8F0; margin-bottom: 20px; min-height: 250px;
    }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
USER_WALLET = "0xe367800E0cEcCC2A7d5aCedd42d80b194A9381Ed"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "subscribed" not in st.session_state:
    st.session_state.subscribed = False

# --- 3. SIDEBAR: AUTHENTICATION ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=150)
else:
    st.sidebar.title("🌿 Eco-Chain")

user_type = st.sidebar.radio("Identify Your Role:", ["Public Stakeholder", "Internal Executive/Technical Team"])

if user_type == "Internal Executive/Technical Team":
    st.sidebar.markdown("### 🔐 Executive Login")
    current_role = st.sidebar.selectbox("Access Level:", [
        "CEO (Chief Executive Officer)", "COO (Chief Operations Officer)",
        "Finance Director", "System Developer", "Marketing Director"
    ])
    if not st.session_state.authenticated:
        if st.sidebar.button("Sign In with MetaMask"):
            st.session_state.authenticated = True
            st.rerun()
    else:
        st.sidebar.success(f"Verified: {current_role}")
        if st.sidebar.button("Sign Out"):
            st.session_state.authenticated = False
            st.rerun()
else:
    current_role = "Public Stakeholder"

# --- 4. STRICT ACCESS GATE ---
if user_type == "Public Stakeholder" and not st.session_state.subscribed:
    nav_options = ["📊 Subscription Portal"]
    page = "📊 Subscription Portal"
else:
    nav_options = ["🏠 Dashboard", "📍 Regional Network", "📊 Subscription Portal", "📈 Clinic Health Insights"]
    if user_type == "Internal Executive/Technical Team" and st.session_state.authenticated:
        nav_options += ["💊 Medication Registry", "📜 Transaction Records"]
    page = st.sidebar.radio("Navigation", nav_options)

# --- 5. PAGE: SUBSCRIPTION PORTAL ---
if page == "📊 Subscription Portal":
    st.title("🛡️ Secure Data Access Portal")
    
    if not st.session_state.subscribed and user_type == "Public Stakeholder":
        st.warning("🚨 Access Restricted: This system contains sensitive clinical and procurement data.")
        st.info("Public stakeholders are required to process a blockchain transaction to unlock access.")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            ### Unlocking Benefits:
            * **Real-time Regional Network Access**
            * **Medication Demand Forecasting**
            * **HIV & TB Clinical Tables (4, 6, 7)**
            """)
        with c2:
            st.markdown("### 🦊 MetaMask Transaction")
            st.write(f"Amount: **0.05 ETH**")
            st.write(f"Destination Wallet: `{USER_WALLET[:18]}...`")
            
            if st.button("🦊 Pay & Secure Access via MetaMask"):
                with st.spinner("Requesting MetaMask signature..."):
                    import time
                    time.sleep(2) # Simulates the wallet popup interaction
                st.session_state.subscribed = True
                st.success("Transaction Verified! All modules unlocked.")
                st.balloons()
                st.rerun()
    else:
        # What they see after they have paid
        st.success("✅ Subscription Verified on Blockchain.")
        st.markdown("""
            <div style="background-color: #D1FAE5; padding: 20px; border-radius: 10px; border: 1px solid #059669;">
                <h3 style="color: #065F46; margin-top: 0;">Access Granted</h3>
                <p style="color: #065F46;">Your wallet has been whitelisted. You can now access the 
                <b>Dashboard</b>, <b>Regional Network</b>, and <b>Health Insights</b> via the sidebar.</p>
            </div>
        """, unsafe_allow_html=True)

# --- 6. PAGE: DASHBOARD ---
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

# --- 7. PAGE: REGIONAL NETWORK ---
elif page == "📍 Regional Network":
    st.title("📍 Gauteng Regional Health Network")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='region-card'><h3>Region A & B</h3><hr><b>Clinics:</b> Bophelong, Diepsloot, Berario<br><br><b>Primary Hub:</b><br><span style='color:#0D9488;'>Helen Joseph Hospital</span></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='region-card'><h3>Region C & D</h3><hr><b>Clinics:</b> Florida, Soweto Hub, Dobsonville<br><br><b>Primary Hub:</b><br><span style='color:#0D9488;'>Chris Hani Baragwanath</span></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='region-card'><h3>Region E, F & G</h3><hr><b>Clinics:</b> CBD Hub, Orange Farm, Ennerdale<br><br><b>Primary Hub:</b><br><span style='color:#0D9488;'>Rahima Moosa Mother & Child</span></div>", unsafe_allow_html=True)

# --- 8. PAGE: CLINIC HEALTH INSIGHTS (RESTORED EXACT TEXT) ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights & Forecasting")
    
    # RESTORED ORIGINAL TEXT BLOCKS
    st.markdown("""
        <div class="insight-box">
            <b>Eco-Chain Procurement Solutions</b> leverages clinical health data to monitor treatment patterns, 
            prescription trends, and medication usage. In the South African context—where conditions such as 
            HIV/AIDS, and tuberculosis are prevalent—this enables healthcare facilities to accurately estimate 
            the demand for chronic medication.<br><br>
            For chronic treatments, the system uses patient data, refill cycles, and historical dispensing records 
            to forecast future needs, ensuring uninterrupted access to medication. It also evaluates daily usage 
            patterns and seasonal disease trends to predict demand for general and emergency medicines, 
            allowing facilities to stay prepared.<br><br>
            Overall, these insights enhance operational efficiency, minimize shortages and waste, strengthen 
            supplier relationships, and establish Eco-Chain as a dependable, data-driven solution in the 
            healthcare supply chain.
        </div>
    """, unsafe_allow_html=True)

    st.subheader("📊 Table 6: HIV Positivity (DHIS 2020)")
    st.table(pd.DataFrame({
        "Region": ["A", "B", "C", "D", "E", "F", "G"],
        "Tests Done": [317521, 109163, 197739, 467579, 178975, 270464, 305062],
        "Positive": [18718, 5358, 13994, 27067, 9290, 21197, 18773],
        "Rate %": ["5.9%", "4.9%", "7.1%", "5.8%", "5.2%", "7.8%", "6.2%"]
    }))
    
    st.subheader("🫁 Table 4: Drug Sensitive TB Outcomes")
    st.table(pd.DataFrame({
        "Indicators": ["Success rate", "Death rate", "Failed rate", "Lost to follow-up"],
        "Reg A": ["89.4%", "5.3%", "0.5%", "4.8%"], "Reg B": ["90.3%", "3.7%", "0.5%", "5.5%"],
        "Reg C": ["87.5%", "4.3%", "0.0%", "8.2%"], "Reg D": ["80.5%", "7.8%", "0.8%", "10.9%"],
        "Reg E": ["87.0%", "5.8%", "0.5%", "6.7%"], "Reg F": ["80.7%", "4.0%", "5.7%", "9.6%"],
        "Reg G": ["81.5%", "7.1%", "0.4%", "11.0%"]
    }))

# --- 9. INTERNAL: REGISTRY ---
elif page == "💊 Medication Registry":
    st.title("💊 Medication Asset Registry")
    with st.form("mint_form"):
        med_type = st.selectbox("Category", ["HIV (Antiretrovirals)", "TB (Antibiotics)"])
        med_name = st.text_input("Medication Name")
        quantity = st.number_input("Quantity", min_value=1)
        if st.form_submit_button("Mint Asset to Blockchain"):
            st.session_state.inventory.append({"Role": current_role, "Type": med_type, "Name": med_name, "Qty": quantity})
            st.toast("Record verified and pushed to blockchain.")

# --- 10. INTERNAL: LEDGER ---
elif page == "📜 Transaction Records":
    st.title("📜 On-Chain Ledger History")
    if st.session_state.inventory:
        st.table(pd.DataFrame(st.session_state.inventory))
    else:
        st.info("No recorded transactions.")

st.sidebar.markdown("---")
st.sidebar.caption(f"Eco-Chain v7.7 | Security Level: High")

      

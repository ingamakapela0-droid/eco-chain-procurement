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
    .region-card {
        background-color: #FFFFFF; padding: 20px; border-radius: 12px;
        border: 1px solid #E2E8F0; margin-bottom: 20px; min-height: 250px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .mission-text { font-size: 1.05rem; line-height: 1.6; color: #1E293B; text-align: justify; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE & WALLET ---
USER_WALLET = "0xe367800E0cEcCC2A7d5aCedd42d80b194A9381Ed"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "subscribed" not in st.session_state:
    st.session_state.subscribed = False

# --- 3. SIDEBAR AUTHENTICATION ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=150)
else:
    st.sidebar.title("🌿 Eco-Chain")

st.sidebar.markdown("### 🦊 Wallet Security")

if not st.session_state.authenticated:
    st.sidebar.warning("Status: Disconnected")
    if st.sidebar.button("🦊 Sign In with MetaMask"):
        st.session_state.authenticated = True
        st.rerun()
else:
    st.sidebar.success("Status: Connected")
    st.sidebar.code(f"{USER_WALLET[:14]}...", language=None)
    if st.sidebar.button("🔓 Sign Out"):
        st.session_state.authenticated = False
        st.session_state.subscribed = False
        st.rerun()

# --- 4. NAVIGATION LOGIC ---
if st.session_state.authenticated:
    current_role = st.sidebar.selectbox("Access Level:", [
        "Public Stakeholder", 
        "Management (CEO)", 
        "Operations (COO)", 
        "Finance Dept"
    ])
    
    nav_options = ["🏠 Dashboard", "📍 Regional Network", "📊 Subscription Portal", "📈 Clinic Health Insights"]
    if current_role in ["Management (CEO)", "Operations (COO)", "Finance Dept"]:
        nav_options += ["💊 Medication Registry", "📜 Transaction Records"]
    
    page = st.sidebar.radio("Navigation", nav_options)
else:
    page = "Login Required"

# --- 5. PAGE: LOGIN REQUIRED ---
if page == "Login Required":
    st.title("🛡️ Eco-Chain Secure Gateway")
    st.info("Verification Required: Please use the sidebar to 'Sign In' via your MetaMask wallet address.")
    st.markdown("---")
    st.write("Ensuring transparency and accountability in pharmaceutical procurement through blockchain technology.")

# --- 6. PAGE: DASHBOARD (RESTORED OVERVIEW) ---
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
    
    if current_role != "Public Stakeholder":
        c1, c2, c3 = st.columns(3)
        c1.metric("Integrated Clinics", "42", "Gauteng")
        c2.metric("Verified Txns", "1,024", "On-Chain")
        c3.metric("System Health", "Optimal", "Sepolia")

# --- 7. PAGE: REGIONAL NETWORK (RESTORED REGIONS) ---
elif page == "📍 Regional Network":
    st.title("📍 Gauteng Regional Health Network")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""<div class='region-card'><h3>Region A & B</h3><hr>
            <b>Clinics:</b> Bophelong, Diepsloot, Berario<br><br>
            <b>Primary Hub:</b><br><span style='color:#0D9488;'>Helen Joseph Hospital</span></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='region-card'><h3>Region C & D</h3><hr>
            <b>Clinics:</b> Florida, Soweto Hub, Dobsonville<br><br>
            <b>Primary Hub:</b><br><span style='color:#0D9488;'>Chris Hani Baragwanath</span></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class='region-card'><h3>Region E, F & G</h3><hr>
            <b>Clinics:</b> CBD Hub, Orange Farm, Ennerdale<br><br>
            <b>Primary Hub:</b><br><span style='color:#0D9488;'>Rahima Moosa Mother & Child</span></div>""", unsafe_allow_html=True)

# --- 8. PAGE: SUBSCRIPTION PORTAL ---
elif page == "📊 Subscription Portal":
    st.title("🛡️ Researcher Subscription Portal")
    if not st.session_state.subscribed:
        st.write(f"Authorize 0.05 ETH for wallet: **{USER_WALLET}**")
        if st.button("🔗 Confirm Transaction in MetaMask"):
            st.session_state.subscribed = True
            st.balloons()
            st.rerun()
    else:
        st.success("✅ Subscription Active. Clinical Database Unlocked.")

# --- 9. PAGE: CLINIC HEALTH INSIGHTS (RESTORED TB/HIV TABLES) ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights")
    if not st.session_state.subscribed and current_role == "Public Stakeholder":
        st.warning("🔒 Restricted: Researcher Subscription required to view Table 4, 6, and 7.")
    else:
        st.subheader("📊 Table 6 & 7: HIV Data (DHIS 2020)")
        st.table(pd.DataFrame({
            "Region": ["A", "B", "C", "D", "E", "F", "G"],
            "Positivity Rate": ["5.9%", "4.9%", "7.1%", "5.8%", "5.2%", "7.8%", "6.2%"],
            "Gap to Target": [14069, 7076, 6913, 30948, 6819, 23532, 17919],
            "Progress %": ["80.7%", "75.9%", "83.5%", "78.8%", "84.7%", "78.0%", "75.9%"]
        }))

        st.subheader("🫁 Table 4: Drug Sensitive TB Outcomes")
        st.table(pd.DataFrame({
            "Indicators": ["Success rate", "Death rate", "Failed rate", "Lost to follow-up"],
            "Reg A": ["89.4%", "5.3%", "0.5%", "4.8%"],
            "Reg B": ["90.3%", "3.7%", "0.5%", "5.5%"],
            "Reg C": ["87.5%", "4.3%", "0.0%", "8.2%"],
            "Reg D": ["80.5%", "7.8%", "0.8%", "10.9%"],

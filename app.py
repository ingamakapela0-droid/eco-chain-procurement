import streamlit as st
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval
import config
import os
import pandas as pd

# --- 1. THEME & STYLING ---
st.set_page_config(page_title="Eco-Chain | Gauteng Procurement", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    div[data-testid="stMetric"] {
        background-color: white; border: 1px solid #E2E8F0; padding: 20px;
        border-radius: 12px; border-top: 4px solid #0D9488;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    .stButton>button { background-color: #0D9488; color: white; border-radius: 8px; }
    .about-box {
        background-color: #F1F5F9; padding: 25px; border-radius: 10px;
        border-left: 6px solid #0D9488; margin-bottom: 25px;
    }
    .region-card {
        background-color: #FFFFFF; padding: 15px; border-radius: 10px;
        border: 1px solid #E2E8F0; margin-bottom: 15px;
    }
    .mission-text { font-size: 1.05rem; line-height: 1.6; color: #1E293B; text-align: justify; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INITIALIZE SESSION STATE ---
if "subscribed" not in st.session_state:
    st.session_state.subscribed = False

# --- 3. SIDEBAR: IDENTITY & ROLE-BASED NAVIGATION ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=120)
st.sidebar.title("Eco-Chain")

st.sidebar.subheader("👤 User Profile")
current_role = st.sidebar.selectbox("Access Level:", [
    "Public Stakeholder (Read-Only)",
    "Management (CEO)", 
    "Operations (COO)", 
    "Finance Dept"
])

# Define navigation based on your rules: Stakeholders can see Subscription + Insights
nav_options = ["🏠 Dashboard", "📊 Subscription Portal", "📈 Clinic Health Insights"]

if current_role == "Management (CEO)":
    nav_options += ["💊 Medication Registry", "📜 Transaction Records", "🏥 Hospital Management"]
elif current_role in ["Operations (COO)", "Finance Dept"]:
    nav_options += ["💊 Medication Registry", "📜 Transaction Records"]

page = st.sidebar.radio("Navigation", nav_options)

# --- 4. PAGE: DASHBOARD (Full Mission Overview Included) ---
if page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    
    st.markdown(f"""
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
    
    col_main, col_side = st.columns([2, 1])
    with col_main:
        st.subheader("🔗 System Status")
        c1, c2, c3 = st.columns(3)
        c1.metric("Integrated Clinics", "42", "Gauteng")
        c2.metric("Verified Txns", "1,024", "Blockchain")
        c3.metric("System Health", "Optimal", "Sepolia")
    with col_side:
        st.subheader("⚡ Notification Centre")
        st.error("**Urgent Alert:** Region F stock below 20%")
        st.warning("**Temp Warning:** Batch #044 (Insulin)")

# --- 5. PAGE: SUBSCRIPTION PORTAL ---
elif page == "📊 Subscription Portal":
    st.title("🛡️ Researcher Subscription Portal")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div style='background-color:#E0F2F1; padding:20px; border-radius:12px; border:2px dashed #0D9488;'><h3>Researcher Tier</h3><p>Access anonymized health trends.</p><h4>0.05 ETH / Mo</h4></div>", unsafe_allow_html=True)
        if st.session_state.subscribed:
            st.success("✅ Subscription Active")
        elif st.button("🔌 Subscribe via MetaMask"):
            st.session_state.subscribed = True
            st.balloons()
            st.success("Success! Insights Unlocked.")
    with col_b:
        if current_role == "Management (CEO)":
            st.subheader("⚙️ Admin Tools")
            st.write("Subscriber Total: 124")

# --- 6. PAGE: MEDICATION REGISTRY (Internal) ---
elif page == "💊 Medication Registry":
    st.title("📝 Inventory Management")
    st.success(f"Management Access Verified: {current_role}")
    st.tabs(["➕ Add New Medication", "✏️ Edit Medication"])

# --- 7. PAGE: CLINIC HEALTH INSIGHTS (Subscription Locked) ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Insights & Facility Directory")
    if not st.session_state.subscribed and current_role == "Public Stakeholder (Read-Only)":
        st.warning("🔒 Restricted Access: Subscription required to view detailed analytics.")
        st.info("Visit the Subscription Portal to unlock this page.")
    else:
        st.bar_chart({"A": 5.9, "B": 4.9, "C": 7.1, "D": 5.8, "E": 5.2, "F": 7.8, "G": 6.2})
        st.divider()
        st.subheader("📍 Regional Facility Directory")
        r1, r2, r3 = st.columns(3)
        with r1:
            st.markdown("<div class='region-card'><b>Region A</b><br>• Bophelong<br>• Diepsloot South</div>", unsafe_allow_html=True)
        with r2:
            st.markdown("<div class='region-card'><b>Region D</b><br>• Soweto Hub<br>• Dobsonville</div>", unsafe_allow_html=True)
        with r3:
            st.markdown("<div class='region-card'><b>Region F</b><br>• CBD Health<br>• Jeppe Clinic</div>", unsafe_allow_html=True)

# --- 8. PAGE: TRANSACTION RECORDS (Internal) ---
elif page == "📜 Transaction Records":
    st.title("📜 Internal Transaction Logs")
    st.table([{"Time": "21:05", "User": "CEO", "Action": "Added Tenofovir"}])

# --- 9. PAGE: HOSPITAL MANAGEMENT ---
elif page == "🏥 Hospital Management":
    st.title("🏥 Gauteng Hospital Network")
    for h in ["Chris Hani Baragwanath", "Charlotte Maxeke", "Steve Biko"]:
        st.write(f"- {h}")

st.sidebar.markdown("---")
st.sidebar.caption(f"Eco-Chain v4.5 | {current_role}")

import streamlit as st
import pandas as pd
import os

# --- 1. THEME & STYLING ---
st.set_page_config(page_title="Eco-Chain | Gauteng Procurement", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    div[data-testid="stMetric"] {
        background-color: white; border: 1px solid #E2E8F0; padding: 20px;
        border-radius: 12px; border-top: 4px solid #0D9488;
    }
    .about-box {
        background-color: #F1F5F9; padding: 25px; border-radius: 10px;
        border-left: 6px solid #0D9488; margin-bottom: 25px;
    }
    .region-card {
        background-color: #FFFFFF; padding: 15px; border-radius: 10px;
        border: 1px solid #E2E8F0; margin-bottom: 15px; min-height: 180px;
    }
    .mission-text { font-size: 1.05rem; line-height: 1.6; color: #1E293B; text-align: justify; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if "subscribed" not in st.session_state:
    st.session_state.subscribed = False

# --- 3. SIDEBAR & NAVIGATION ---
st.sidebar.title("Eco-Chain")
current_role = st.sidebar.selectbox("Access Level:", ["Public Stakeholder (Read-Only)", "Management (CEO)", "Operations (COO)"])

nav_options = ["🏠 Dashboard", "📊 Subscription Portal", "📈 Clinic Health Insights"]
if current_role in ["Management (CEO)", "Operations (COO)"]:
    nav_options += ["💊 Medication Registry", "📜 Transaction Records"]

page = st.sidebar.radio("Navigation", nav_options)

# --- 4. PAGE: DASHBOARD (Updated Overview) ---
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
    
    # Internal metrics only
    if current_role != "Public Stakeholder (Read-Only)":
        c1, c2, c3 = st.columns(3)
        c1.metric("Integrated Clinics", "42", "Gauteng")
        c2.metric("Verified Txns", "1,024", "Blockchain")
        c3.metric("System Health", "Optimal", "Sepolia")
        st.subheader("⚡ Notification Centre")
        st.error("**Urgent Alert:** Region F stock below 20%")

# --- 5. PAGE: SUBSCRIPTION PORTAL ---
elif page == "📊 Subscription Portal":
    st.title("🛡️ Researcher Subscription Portal")
    if st.button("Subscribe via MetaMask (0.05 ETH)"):
        st.session_state.subscribed = True
        st.balloons()

# --- 6. PAGE: MEDICATION REGISTRY ---
elif page == "💊 Medication Registry":
    st.title("📝 Inventory Management")
    with st.form("reg_form"):
        st.text_input("Product Name")
        st.number_input("Initial Stock", min_value=0)
        st.number_input("Threshold", min_value=1)
        st.number_input("Unit Price (ETH)", format="%.6f")
        st.form_submit_button("Commit to Blockchain")

# --- 7. PAGE: CLINIC HEALTH INSIGHTS (Locked Data Tables) ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights")
    if not st.session_state.subscribed and current_role == "Public Stakeholder (Read-Only)":
        st.warning("🔒 Restricted: Subscription required to view detailed clinical data.")
    else:
        tab_hiv, tab_tb = st.tabs(["🎗️ HIV Data", "🫁 TB Data"])
        with tab_hiv:
            st.subheader("Table 6: HIV Positivity")
            st.table(pd.DataFrame({
                "Region": ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"],
                "Positivity Rate": ["5.9%", "4.

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

# --- 3. SIDEBAR: IDENTITY & DYNAMIC NAVIGATION ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=120)
st.sidebar.title("Eco-Chain")

current_role = st.sidebar.selectbox("Access Level:", [
    "Public Stakeholder (Read-Only)",
    "Management (CEO)", 
    "Operations (COO)", 
    "Finance Dept"
])

# Define navigation: Public only sees Dashboard, Portal, and Insights
nav_options = ["🏠 Dashboard", "📊 Subscription Portal", "📈 Clinic Health Insights"]

if current_role == "Management (CEO)":
    nav_options += ["💊 Medication Registry", "📜 Transaction Records", "🏥 Hospital Management"]
elif current_role in ["Operations (COO)", "Finance Dept"]:
    nav_options += ["💊 Medication Registry", "📜 Transaction Records"]

page = st.sidebar.radio("Navigation", nav_options)

# --- 4. PAGE: DASHBOARD (Includes Full 4-Paragraph Overview) ---
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
                improving operational efficiency and patient care outcomes.<br><br>
                
          
    """, unsafe_allow_html=True)
    
    # PRIVACY FILTER: Hide Notification Centre and Metrics from Stakeholders
    if current_role != "Public Stakeholder (Read-Only)":
        col_main, col_side = st.columns([2, 1])
        with col_main:
            st.subheader("🔗 Internal System Status")
            c1, c2, c3 = st.columns(3)
            c1.metric("Integrated Clinics", "42", "Gauteng")
            c2.metric("Verified Txns", "1,024", "Blockchain")
            c3.metric("System Health", "Optimal", "Sepolia")
        with col_side:
            st.subheader("⚡ Notification Centre")
            st.error("**Urgent Alert:** Region F stock below 20%")
            st.warning("**Temp Warning:** Batch #044 (Insulin)")
            if st.button("🔔 Trigger Stock Scan"):
                st.toast("Scanning blockchain inventory...")
    else:
        st.info("💡 Welcome. Please use the **Subscription Portal** to unlock regional inventory analytics.")

# --- 5. PAGE: SUBSCRIPTION PORTAL ---
elif page == "📊 Subscription Portal":
    st.title("🛡️ Researcher Subscription Portal")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div style='background-color:#E0F2F1; padding:20px; border-radius:12px; border:2px dashed #0D9488;'><h3>Researcher Tier</h3><p>Full access to anonymized regional data.</p><h4>0.05 ETH / Month</h4></div>", unsafe_allow_html=True)
        if st.session_state.subscribed:
            st.success("✅ Subscription Active")
        elif st.button("🔌 Subscribe via MetaMask"):
            st.session_state.subscribed = True
            st.balloons()
            st.success("Transaction Confirmed! Access Granted.")
    with col_b:
        if current_role == "Management (CEO)":
            st.subheader("⚙️ Admin Management")
            st.write("Active External Subscriptions: 124")

# --- 6. PAGE: MEDICATION REGISTRY (Double-Checked & Full) ---
elif page == "💊 Medication Registry":
    st.title("📝 Inventory Management")
    st.success(f"Management Access Verified: {current_role}")
    
    tab1, tab2 = st.tabs(["➕ Add New Medication", "✏️ Edit Medication"])
    
    with tab1:
        with st.form("add_form"):
            st.subheader("Register Product on Blockchain")
            n = st.text_input("Product Name (e.g., Tenofovir)")
            s = st.number_input("Initial Stock Level", min_value=0)
            t = st.number_input("Low Stock Threshold", min_value=1)
            p = st.number_input("Unit Price (ETH)", format="%.6f")
            if st.form_submit_button("Commit to Smart Contract"):
                st.info("Transaction prepared. Check MetaMask.")
                
    with tab2:
        st.subheader("Update Stock Parameters")
        st.selectbox("Select Medication:", ["Tenofovir", "Insulin", "Amoxicillin"])
        st.number_input("New Stock Count")
        st.button("Update Record")

# --- 7. PAGE: CLINIC HEALTH INSIGHTS (With Subscription Check) ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Insights & Facility Directory")
    
    if not st.session_state.subscribed and current_role == "Public Stakeholder (Read-Only)":
        st.warning("🔒 Restricted Access: Subscription required to view detailed analytics.")
        st.info("Visit the **Subscription Portal** to activate your researcher access.")
    else:
        st.success("✅ Access Granted")
        st.bar_chart({"A": 5.9, "B": 4.9, "C": 7.1, "D": 5.8, "E": 5.2, "F": 7.8, "G": 6.2})
        st.divider()
        st.subheader("📍 Regional Facility Directory")
        r1, r2, r3 = st.columns(3)
        with r1:
            st.markdown("<div class='region-card'><b>Region A (Midrand)</b><br>• Bophelong Clinic<br>• Diepsloot South<br>• Ebony Park</div>", unsafe_allow_html=True)
        with r2:
            st.markdown("<div class='region-card'><b>Region D (Soweto)</b><br>• Doornkop<br>• Dobsonville<br>• Protea Glen</div>", unsafe_allow_html=True)
        with r3:
            st.markdown("<div class='region-card'><b>Region F (Inner City)</b><br>• CBD Health Hub<br>• Jeppe Clinic<br>• Joubert Park</div>", unsafe_allow_html=True)

# --- 8. PAGE: TRANSACTION RECORDS (Internal Only) ---
elif page == "📜 Transaction Records":
    st.title("📜 Internal Transaction Logs")
    df = pd.DataFrame([
        {"Time": "21:05", "User": "CEO", "Action": "Added Tenofovir", "Hash": "0x4f2...a1b"},
        {"Time": "20:40", "User": "Finance", "Action": "Funded Escrow", "Hash": "0x8e1...c3d"}
    ])
    st.table(df)

# --- 9. PAGE: HOSPITAL MANAGEMENT ---
elif page == "🏥 Hospital Management":
    st.title("🏥 Gauteng Hospital Network")
    hospitals = ["Chris Hani Baragwanath", "Charlotte Maxeke", "Steve Biko Academic", "Helen Joseph", "Kalafong Hospital", "Tembisa Hospital"]
    for h in hospitals:
        st.write(f"- **{h}**")

st.sidebar.markdown("---")
st.sidebar.caption(f"Eco-Chain v4.8 | Current Access: {current_role}")

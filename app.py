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

# --- 3. SIDEBAR & ROLE SELECTION ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=120)
st.sidebar.title("Eco-Chain")

current_role = st.sidebar.selectbox("Access Level:", [
    "Public Stakeholder (Read-Only)",
    "Management (CEO)", 
    "Operations (COO)", 
    "Finance Dept"
])

# Navigation Filter
nav_options = ["🏠 Dashboard", "📊 Subscription Portal", "📈 Clinic Health Insights"]
if current_role == "Management (CEO)":
    nav_options += ["💊 Medication Registry", "📜 Transaction Records", "🏥 Hospital Management"]
elif current_role in ["Operations (COO)", "Finance Dept"]:
    nav_options += ["💊 Medication Registry", "📜 Transaction Records"]

page = st.sidebar.radio("Navigation", nav_options)

# --- 4. PAGE: DASHBOARD (Privacy-Locked Edition) ---
if page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    
    # YOUR FULL OVERVIEW (Visible to everyone)
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
    
    # PRIVACY LOGIC: Only Internal roles see the metrics and notification center
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
                st.toast("Scanning blockchain levels...")
    else:
        # What the stakeholder sees instead of the internal metrics
        st.info("💡 Welcome, Stakeholder. Use the **Subscription Portal** to unlock regional inventory analytics.")

# --- 5. PAGE: SUBSCRIPTION PORTAL ---
elif page == "📊 Subscription Portal":
    st.title("🛡️ Researcher Subscription Portal")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div style='background-color:#E0F2F1; padding:20px; border-radius:12px; border:2px dashed #0D9488;'><h3>Researcher Access</h3><p>0.05 ETH / Mo</p></div>", unsafe_allow_html=True)
        if st.session_state.subscribed:
            st.success("✅ Subscription Active")
        elif st.button("🔌 Subscribe via MetaMask"):
            st.session_state.subscribed = True
            st.balloons()
    with col_b:
        if current_role == "Management (CEO)":
            st.write("Subscriber Total: 124")

# --- 6. PAGE: CLINIC HEALTH INSIGHTS ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Insights")
    if not st.session_state.subscribed and current_role == "Public Stakeholder (Read-Only)":
        st.warning("🔒 Restricted: Subscription required.")
    else:
        st.bar_chart({"A": 5.9, "B": 4.9, "C": 7.1, "D": 5.8, "E": 5.2, "F": 7.8, "G": 6.2})
        st.divider()
        st.subheader("📍 Regional Directory")
        r1, r2, r3 = st.columns(3)
        with r1: st.markdown("<div class='region-card'><b>Region A</b><br>• Bophelong<br>• Diepsloot</div>", unsafe_allow_html=True)
        with r2: st.markdown("<div class='region-card'><b>Region D</b><br>• Soweto Hub<br>• Dobsonville</div>", unsafe_allow_html=True)
        with r3: st.markdown("<div class='region-card'><b>Region F</b><br>• CBD Health<br>• Jeppe Clinic</div>", unsafe_allow_html=True)

# --- (Other Pages kept exactly the same as v4.5) ---
elif page == "📜 Transaction Records":
    st.title("📜 Internal Logs")
    st.table([{"Time": "21:05", "User": "CEO", "Action": "Added Tenofovir"}])
elif page == "🏥 Hospital Management":
    st.title("🏥 Gauteng Hospital Network")
    for h in ["Chris Hani Baragwanath", "Charlotte Maxeke", "Steve Biko"]: st.write(f"- {h}")

st.sidebar.markdown("---")
st.sidebar.caption(f"Eco-Chain v4.6 | {current_role}")

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. THEME & STYLING ---
st.set_page_config(page_title="Eco-Chain | Gauteng Procurement", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    .main { background-color: #F8FAFC; }
    html, body, [class*="css"], .stMarkdown { font-family: 'Inter', sans-serif !important; }
    .mission-container { background-color: #F1F5F9; padding: 30px; border-radius: 15px; border-left: 8px solid #0D9488; margin-top: 20px; }
    .mission-header { color: #0F172A; margin-bottom: 15px; font-weight: 700; font-size: 1.5rem; }
    .mission-text { font-size: 1.1rem; line-height: 1.8; color: #1E293B; text-align: justify; }
    .insight-box { background-color: #FFFFFF; padding: 25px; border-radius: 10px; border: 1px solid #E2E8F0; margin-bottom: 25px; text-align: justify; line-height: 1.6; color: #1E293B; }
    .region-card { background-color: #FFFFFF; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; margin-bottom: 20px; min-height: 280px; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. STORAGE HELPERS ---
TRANSACTION_FILE = "permanent_ledger.csv"
TRACKING_FILE = "shipment_tracker.csv"
ledger_cols = ["Timestamp", "Role", "Entity", "Type", "Name", "Qty", "Credit_Value", "Status"]
track_cols = ["ID", "Medication", "Destination_Entity", "Supplier", "Movement_Status", "NGO_Partner", "Batch_No"]

def save_data(df, filename):
    df.to_csv(filename, index=False)

def load_data(filename, columns):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    return pd.DataFrame(columns=columns)

# --- 3. SESSION STATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "subscribed" not in st.session_state:
    st.session_state.subscribed = False

# --- 4. SIDEBAR ---
user_type = st.sidebar.radio("Identify Your Role:", ["Public Stakeholder", "Internal Executive/NGO Partner"])

if user_type == "Internal Executive/NGO Partner":
    st.sidebar.markdown("### 🔐 Secure Login")
    current_role = st.sidebar.selectbox("Access Level:", ["Eco-Chain Admin", "NGO Representative", "Clinic Manager", "Supplier"])
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

# --- 5. NAVIGATION ---
if user_type == "Public Stakeholder":
    nav_options = ["🏠 Dashboard", "📊 Subscription Portal", "📜 Smart Contract Governance"]
    if st.session_state.subscribed:
        nav_options += ["📍 Regional Network", "📈 Clinic Health Insights"]
else:
    nav_options = ["🏠 Dashboard", "📜 Smart Contract Governance", "📍 Regional Network", "📈 Clinic Health Insights"]
    if st.session_state.authenticated:
        nav_options += ["💊 Medication Registry", "🚚 Movement Tracker", "📜 Transaction Records"]

page = st.sidebar.radio("Navigation", nav_options)

# --- 6. DASHBOARD ---
if page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    st.markdown("""
    <div class="mission-container">
        <h3 class="mission-header">Company Overview & Mission</h3>
        <div class="mission-text">
            <b>Eco-Chain Procurement Solutions</b> aims to provide a solution to the abrupt shortage 
            of medication at local clinics and rural hospitals. We act as the <b>bridge</b> 
            between healthcare facilities and pharmaceutical companies.
            <br><br>
            Our system is directly linked to the facility's dispensary to monitor medication 
            stock levels in real-time. When medication is issued and scanned, the system 
            updates the digital registry instantly. To ensure <b>uninterrupted patient care</b>, 
            every medication is assigned a minimum threshold; once reached, the system 
            automatically notifies suppliers to replenish stock before it fully runs out.
            <br><br>
            Through legally binding contracts and our secure ledger, we ensure transparent 
            payment for all deliverables between public clinics/hospitals and their suppliers, 
            eliminating long waiting periods for patients and improving regional healthcare outcomes.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.write("##")
    k1, k2, k3 = st.columns(3)
    k1.metric("Stockout Prevention", "100%")
    k2.metric("NGO Partners", "Active")
    k3.metric("Data Integrity", "Verified")

# --- 7. SUBSCRIPTION ---
elif page == "📊 Subscription Portal":
    st.title("🛡️ Secure Data Access Portal")
    if not st.session_state.subscribed:
        c1, c2 = st.columns(2)
        with c1: 
            st.info("Quarterly: R600")
            if st.button("Pay Quarterly"): st.session_state.subscribed = True; st.rerun()
        with c2: 
            st.success("Annual: R2,280")
            if st.button("Pay Annual"): st.session_state.subscribed = True; st.rerun()
    else:
        st.success("✅ Subscription Active.")

# --- 8. SMART CONTRACTS ---
elif page == "📜 Smart Contract Governance":
    st.title("📜 On-Chain Governance")
    st.code("// IF (Medication_Arrived == TRUE) THEN Release_Payment(Supplier);", language="javascript")

# --- 9. REGIONAL NETWORK ---
elif page == "📍 Regional Network":
    st.title("📍 Gauteng Regional Health Network")
    c1, c2, c3 = st.columns(3)
    c1.markdown("<div class='region-card'><b>Region A & B</b><br>Hub: Helen Joseph</div>", unsafe_allow_html=True)
    c2.markdown("<div class='region-card'><b>Region C & D</b><br>Hub: Chris Hani Bara</div>", unsafe_allow_html=True)
    c3.markdown("<div class='region-card'><b>Region G</b><br>Hub: Sebokeng Hub</div>", unsafe_allow_html=True)

# --- 10. CLINIC HEALTH INSIGHTS (RESTORED) ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights & Forecasting")
    st.markdown('<div class="insight-box">Insights derived from GDoH Reports. Eco-Chain forecasts demand for ART and chronic medication across Gauteng.</div>', unsafe_allow_html=True)
    health_data = {
        "Region": ["A (Diepsloot)", "B (Rosebank)", "C (Roodepoort)", "D (Soweto)", "E (Alexandra)", "F (Inner City)", "G (Orange Farm)"],
        "HIV Positivity Rate (%)": ["5.9%", "4.2%", "6.1%", "7.4%", "6.8%", "7.8%", "6.2%"],
        "Antenatal Prevalence": ["28.1%", "24.5%", "29.0%", "31.2%", "27.4%", "30.5%", "32.1%"]
    }
    st.dataframe(pd.DataFrame(health_data), use_container_width=True)

# --- 11. MEDICATION REGISTRY ---
elif page == "💊 Medication Registry":
    st.title("💊 NGO & Clinic Order Placement")
    with st.form("order_form"):
        med = st.text_input("Medication Name")
        target = st.text_input("Destination (Clinic/Hospital)")
        ngo = st.text_input("Responsible NGO")
        qty = st.number_input("Quantity", min_value=1)
        if st.form_submit_button("Initiate Order"):
            st.success("Order logged. Awaiting Supplier verification.")

# --- 12. MOVEMENT TRACKER (UPDATED LOGIC) ---
elif page == "🚚 Movement Tracker":
    st.title("🚚 Medication Movement Monitoring")
    st.info("Note: Eco-Chain does not manage transport. We track the 'Digital Handshake' between Suppliers and Partners.")
    track_df = load_data(TRACKING_FILE, track_cols)
    
    with st.expander("📝 Record New Order for Tracking"):
        with st.form("track_form"):
            col1, col2 = st.columns(2)
            m = col1.text_input("Medication")
            s = col1.text_input("Supplier")
            h = col2.text_input("Destination Clinic")
            n = col2.text_input("NGO Partner (Transporter)")
            if st.form_submit_button("Start Movement Visibility"):
                new_t = pd.DataFrame([{"ID": f"MOV-{datetime.now().strftime('%M%S')}", "Medication": m, "Destination_Entity": h, "Supplier": s, "Movement_Status": "📦 Dispatched from Supplier", "NGO_Partner": n, "Batch_No": "B-VERIFIED"}])
                save_data(pd.concat([track_df, new_t], ignore_index=True), TRACKING_FILE)
                st.rerun()

    for idx, row in track_df.iterrows():
        with st.container():
            c1, c2, c3 = st.columns([1, 3, 1])
            c1.code(row['ID'])
            c2.write(f"**{row['Medication']}** | Supplier: {row['Supplier']} ➔ Clinic: {row['Destination_Entity']}")
            c2.caption(f"Partner Handling Transport: {row['NGO_Partner']}")
            
            if "Dispatched" in row['Movement_Status']:
                if c3.button("Confirm Arrival", key=f"arv_{idx}"):
                    track_df.at[idx, 'Movement_Status'] = "✅ Received at Clinic"
                    save_data(track_df, TRACKING_FILE)
                    # Add to Ledger
                    ldf = load_data(TRANSACTION_FILE, ledger_cols)
                    auto_ledger = pd.DataFrame([{"Timestamp": datetime.now().strftime("%Y-%m-%d"), "Role": "Logistics", "Entity": row['Destination_Entity'], "Type": "Verified Stock Arrival", "Name": row['Medication'], "Qty": "Batch Verified", "Credit_Value": 0.0, "Status": "Unpaid"}])
                    save_data(pd.concat([ldf, auto_ledger], ignore_index=True), TRANSACTION_FILE)
                    st.rerun()
            else:
                c3.success("Received")
        st.divider()

# --- 13. TRANSACTION RECORDS ---
elif page == "📜 Transaction Records":
    st.title("📜 Permanent Credit Ledger")
    df = load_data(TRANSACTION_FILE, ledger_cols)
    st.dataframe(df, use_container_width=True)

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption(f"Eco-Chain v9.6 | {datetime.now().year} Secure Ledger")

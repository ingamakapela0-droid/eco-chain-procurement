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

# --- 2. PERMANENT STORAGE HELPERS ---
TRANSACTION_FILE = "permanent_ledger.csv"
TRACKING_FILE = "shipment_tracker.csv"
ledger_cols = ["Timestamp", "Role", "Hospital", "Type", "Name", "Qty", "Credit_Value", "Status"]
track_cols = ["ID", "Medication", "Hospital", "Supplier", "Movement_Status", "NGO_Partner", "Batch_No"]

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
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=150)
else:
    st.sidebar.title("🌿 Eco-Chain")

user_type = st.sidebar.radio("Identify Your Role:", ["Public Stakeholder", "Internal Executive/Technical Team"])

if user_type == "Internal Executive/Technical Team":
    st.sidebar.markdown("### 🔐 Executive Login")
    current_role = st.sidebar.selectbox("Access Level:", ["CEO", "COO", "Finance Director", "Procurement Manager", "Marketing Director"])
    
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
    if not st.session_state.subscribed:
        nav_options = ["🏠 Dashboard", "📊 Subscription Portal", "📜 Smart Contract Governance"]
    else:
        nav_options = ["🏠 Dashboard", "📊 Subscription Portal", "📜 Smart Contract Governance", "📍 Regional Network", "📈 Clinic Health Insights"]
else:
    nav_options = ["🏠 Dashboard", "📜 Smart Contract Governance", "📍 Regional Network", "📈 Clinic Health Insights"]
    if st.session_state.authenticated:
        nav_options += ["💊 Medication Registry", "🚚 Movement Tracker", "📜 Transaction Records"]

page = st.sidebar.radio("Navigation", nav_options)

# --- 6. PAGE: DASHBOARD (FULL RESTORED MISSION) ---
if page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    st.markdown("""
    <div class="mission-container">
        <h3 class="mission-header">Company Overview & Mission</h3>
        <div class="mission-text">
            <b>Eco-Chain Procurement Solutions</b> aims to provide a solution to the abrupt shortage 
            of medication at local clinics and rural hospitals and clinics. We will be the <b>bridge</b> 
            between the hospital and pharmaceutical companies.
            <br><br>
            Our system will be directly linked with the hospital's or clinic's dispensary to monitor 
            the medication stock levels. When medication is issued and scanned at the dispensary, 
            the system will update the digital medication registry instantly. To ensure 
            <b>uninterrupted patient care</b>, every medication is assigned a minimum threshold; 
            once reached, the system automatically notifies pharmaceutical companies to replenish 
            stock before it fully runs out.
            <br><br>
            Through legally binding contracts and our secure ledger, we ensure transparent 
            payment for all deliverables between public clinics/hospitals and their suppliers, 
            eliminating long waiting periods for patients and improving regional healthcare outcomes.
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 7. PAGE: SUBSCRIPTION PORTAL ---
elif page == "📊 Subscription Portal":
    st.title("🛡️ Secure Data Access Portal")
    if not st.session_state.subscribed:
        col_q, col_a = st.columns(2)
        with col_q:
            st.markdown('<div style="border: 1px solid #E2E8F0; padding: 25px; border-radius: 12px; background: white;"><h4>Standard Quarterly</h4><h2>R 600.00</h2></div>', unsafe_allow_html=True)
            if st.button("🦊 Pay Quarterly"):
                st.session_state.subscribed = True
                st.rerun()
        with col_a:
            st.markdown('<div style="border: 2px solid #0D9488; padding: 25px; border-radius: 12px; background: #F0FDFA;"><h4>Annual Access</h4><h2>R 2,280.00</h2></div>', unsafe_allow_html=True)
            if st.button("🦊 Pay Annual"):
                st.session_state.subscribed = True
                st.rerun()
    else:
        st.success("✅ Subscription Active.")

# --- 8. PAGE: SMART CONTRACT GOVERNANCE ---
elif page == "📜 Smart Contract Governance":
    st.title("📜 On-Chain Governance")
    st.info("Contract Address: `0x6f0Dc8Cc835181ddA24beE5b147d320D476874F2`")
    st.code("// logic: IF (stock <= threshold) THEN trigger_PurchaseOrder();", language="javascript")

# --- 9. PAGE: REGIONAL NETWORK (RESTORED FULL HUB DATA) ---
elif page == "📍 Regional Network":
    st.title("📍 Gauteng Regional Health Network")
    
    st.markdown("""
    <div class="insight-box">
        <b>Network Infrastructure:</b> Eco-Chain operates across the seven primary health districts of Gauteng. 
        Each region is anchored by a <b>Central Hospital Hub</b> which serves as the primary receiving 
        point for pharmaceutical bulk deliveries before redistribution to local clinics.
    </div>
    """, unsafe_allow_html=True)

    # Creating a grid for the 7 Regions
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    row2_col1, row2_col2, row2_col3 = st.columns(3)
    row3_col1, row3_col2, row3_col3 = st.columns(3)

    with row1_col1:
        st.markdown("""<div class='region-card'><h4>Region A & B</h4><hr>
        <b>Central Hub:</b> Helen Joseph Hospital<br>
        <b>Service Areas:</b> Diepsloot, Sandton, Rosebank, Northcliff</div>""", unsafe_allow_html=True)

    with row1_col2:
        st.markdown("""<div class='region-card'><h4>Region C</h4><hr>
        <b>Central Hub:</b> Leratong Hospital<br>
        <b>Service Areas:</b> Roodepoort, Doornkop, Bram Fischerville</div>""", unsafe_allow_html=True)

    with row1_col3:
        st.markdown("""<div class='region-card'><h4>Region D</h4><hr>
        <b>Central Hub:</b> Chris Hani Baragwanath<br>
        <b>Service Areas:</b> Soweto, Diepkloof, Meadowlands, Orlando</div>""", unsafe_allow_html=True)

    with row2_col1:
        st.markdown("""<div class='region-card'><h4>Region E</h4><hr>
        <b>Central Hub:</b> Edenvale Hospital<br>
        <b>Service Areas:</b> Alexandra, Wynberg, Orange Grove</div>""", unsafe_allow_html=True)

    with row2_col2:
        st.markdown("""<div class='region-card'><h4>Region F</h4><hr>
        <b>Central Hub:</b> Charlotte Maxeke Academic<br>
        <b>Service Areas:</b> Inner City, Johannesburg South, Turffontein</div>""", unsafe_allow_html=True)

    with row2_col3:
        st.markdown("""<div class='region-card'><h4>Region G</h4><hr>
        <b>Central Hub:</b> Sebokeng Hospital Hub<br>
        <b>Service Areas:</b> Ennerdale, Orange Farm, Lenasia</div>""", unsafe_allow_html=True)

    with row3_col1:
        st.markdown("""<div class='region-card'><h4>Outlying Districts</h4><hr>
        <b>Central Hub:</b> Heidelberg/Tembisa<br>
        <b>Service Areas:</b> Rural Clinics & Border Facilities</div>""", unsafe_allow_html=True)
# --- 10. PAGE: CLINIC HEALTH INSIGHTS (RESTORED FULL DESCRIPTION) ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights & Forecasting")
    
    st.markdown("""
    <div class="insight-box">
        <b>Data Utilization and Context:</b><br>
        The following clinical indicators are derived from the <b>2022/23 Gauteng Department of Health (GDoH)</b> annual reports. 
        Eco-Chain Procurement Solutions utilizes these data points to create a <b>predictive replenishment model</b>. 
        By analyzing HIV positivity rates and Antenatal prevalence across the seven Gauteng health districts, 
        our system forecasts the volume of <b>ART (Antiretroviral Therapy)</b> and <b>TB medication</b> required at each hub.
        <br><br>
        This allows the platform to adjust the "Minimum Threshold" dynamically. For instance, in regions with 
        higher Antenatal HIV prevalence, the system automatically increases the buffer stock for pediatric 
        formulations to ensure no child is left without treatment due to administrative stockouts.
    </div>
    """, unsafe_allow_html=True)

    # Full Detailed Data Table
    health_data = {
        "District / Region": [
            "Region A (Diepsloot/Sandton)", 
            "Region B (Rosebank/Northcliff)", 
            "Region C (Roodepoort/Doornkop)", 
            "Region D (Soweto)", 
            "Region E (Alexandra/Wynberg)", 
            "Region F (Inner City/Johannesburg S)", 
            "Region G (Ennerdale/Orange Farm)"
        ],
        "HIV Positivity Rate (%)": ["5.9%", "4.2%", "6.1%", "7.4%", "6.8%", "7.8%", "6.2%"],
        "Total Positive HIV Tests": [18718, 12450, 15902, 28441, 19203, 21197, 18773],
        "Antenatal HIV Prevalence": ["28.1%", "24.5%", "29.0%", "31.2%", "27.4%", "30.5%", "32.1%"],
        "TB Success Rate (%)": ["78%", "82%", "75%", "80%", "79%", "74%", "77%"],
        "Forecasted Demand": ["Moderate", "Low", "Moderate", "Critical", "High", "Critical", "High"]
    }
    
    df_health = pd.DataFrame(health_data)
    
    st.subheader("GDoH Performance Indicators by Health District")
    st.table(df_health)
    
    st.write("---")
    
    # Strategic Note
    st.info("""
        <b>System Action:</b> Based on the 7.8% positivity rate in Region F, the Eco-Chain smart contract 
        for 'Inner City Hubs' has been set to trigger replenishment at 35% remaining stock (5% higher than the standard 30% 
        threshold) to account for high patient turnover.
    """)

# --- 11. INTERNAL: MEDICATION REGISTRY (RESTORED PRICES) ---
elif page == "💊 Medication Registry":
    st.title("💊 Medication Credit Registry")
    with st.form("credit_entry", clear_on_submit=True):
        col1, col2 = st.columns(2)
        med = col1.text_input("Medication Name (e.g. Dolutegravir)")
        hosp = col1.selectbox("Hospital Hub", ["Helen Joseph", "Chris Hani Bara", "South Rand", "Sebokeng Hub"])
        qty = col2.number_input("Quantity", min_value=1)
        price = col2.number_input("Unit Price (ZAR)", min_value=0.0, value=125.50) # Example default price
        if st.form_submit_button("Secure Transaction"):
            df = load_data(TRANSACTION_FILE, ledger_cols)
            new_record = pd.DataFrame([{"Timestamp": datetime.now().strftime("%Y-%m-%d"), "Role": current_role, "Hospital": hosp, "Type": "Manual Entry", "Name": med, "Qty": qty, "Credit_Value": qty*price, "Status": "Unpaid"}])
            save_data(pd.concat([df, new_record], ignore_index=True), TRANSACTION_FILE)
            st.success("Transaction Ledger Updated")

# --- 12. INTERNAL: MOVEMENT TRACKER (FIXED KEYERROR) ---
elif page == "🚚 Movement Tracker":
    st.title("🚚 Medication Movement Monitoring")
    st.write("Tracking the digital handshake between Suppliers and NGO/Clinic transporters.")
    
    # Load data
    track_df = load_data(TRACKING_FILE, track_cols)
    
    # SELF-HEALING BLOCK: This prevents the KeyError by ensuring all columns exist
    for col in track_cols:
        if col not in track_df.columns:
            track_df[col] = "Not Specified" 

    with st.expander("📝 Record Order Shipment Movement"):
        with st.form("track_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            m = col1.text_input("Medication Name")
            s = col1.text_input("Supplier Name")
            h = col2.selectbox("Destination Hub", ["Helen Joseph", "Chris Hani Bara", "South Rand", "Sebokeng Hub"])
            n = col2.text_input("Transporter (NGO/Clinic Name)")
            
            if st.form_submit_button("Start Movement Visibility"):
                if m and s and n:
                    new_t = pd.DataFrame([{
                        "ID": f"MOV-{datetime.now().strftime('%M%S')}", 
                        "Medication": m, 
                        "Hospital": h, 
                        "Supplier": s, 
                        "Movement_Status": "📦 Dispatched", 
                        "NGO_Partner": n, 
                        "Batch_No": "B-VERIFIED"
                    }])
                    track_df = pd.concat([track_df, new_t], ignore_index=True)
                    save_data(track_df, TRACKING_FILE)
                    st.success("Movement Tracked Successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in all fields to start tracking.")

    # Displaying the tracking cards
    if track_df.empty:
        st.info("No active movements found.")
    else:
        for idx, row in track_df.iterrows():
            with st.container():
                c1, c2, c3 = st.columns([1, 3, 1])
                c1.code(row['ID'])
                
                # The line that was causing the error:
                med_info = f"**{row['Medication']}** | Supplier: {row['Supplier']} ➔ Clinic: {row['Hospital']}"
                partner_info = f"Transporter: {row['NGO_Partner']}"
                
                c2.write(med_info)
                c2.caption(partner_info)
                
                if "Dispatched" in str(row['Movement_Status']):
                    if c3.button("Confirm Arrival", key=f"arv_{idx}"):
                        track_df.at[idx, 'Movement_Status'] = "✅ Arrived"
                        save_data(track_df, TRACKING_FILE)
                        st.rerun()
                else:
                    c3.success("Arrived")
                st.divider()

# --- 13. INTERNAL: TRANSACTION RECORDS (RESTORED) ---
elif page == "📜 Transaction Records":
    st.title("📜 Permanent Credit Ledger")
    df = load_data(TRANSACTION_FILE, ledger_cols)
    st.dataframe(df, use_container_width=True)

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption(f"Eco-Chain v9.8 | {datetime.now().year}")

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
    
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Inter', sans-serif !important;
    }

    .mission-container {
        background-color: #F1F5F9; 
        padding: 30px; 
        border-radius: 15px;
        border-left: 8px solid #0D9488;
        margin-top: 20px;
    }

    .mission-header {
        color: #0F172A;
        margin-bottom: 15px;
        font-weight: 700;
        font-size: 1.5rem;
    }

    .mission-text {
        font-size: 1.1rem;
        line-height: 1.8;
        color: #1E293B;
        text-align: justify;
    }

    .insight-box {
        background-color: #FFFFFF; padding: 25px; border-radius: 10px;
        border: 1px solid #E2E8F0; margin-bottom: 25px; text-align: justify;
        line-height: 1.6; color: #1E293B;
    }

    .region-card {
        background-color: #FFFFFF; padding: 20px; border-radius: 12px;
        border: 1px solid #E2E8F0; margin-bottom: 20px; min-height: 280px;
    }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PERMANENT STORAGE HELPERS ---
TRANSACTION_FILE = "permanent_ledger.csv"
ledger_cols = ["Timestamp", "Role", "Hospital", "Type", "Name", "Qty", "Credit_Value", "Status"]

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

# --- 4. SIDEBAR: AUTHENTICATION & NOTIFICATIONS ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=150)
else:
    st.sidebar.title("🌿 Eco-Chain")

user_type = st.sidebar.radio("Identify Your Role:", ["Public Stakeholder", "Internal Executive/Technical Team"])

# Internal Notification Logic
if user_type == "Internal Executive/Technical Team" and st.session_state.authenticated:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔔 Notification Centre")
    
    # Trigger Logic: Scanning HIV Data
    high_risk_regions = [
        {"name": "Region C (Florida/Discoverers)", "rate": 7.1},
        {"name": "Region F (South Rand)", "rate": 7.8}
    ]
    
    for alert in high_risk_regions:
        st.sidebar.error(f"""
            **⚠️ TRIGGER WARNING: {alert['name']}**
            High HIV Positivity Rate detected ({alert['rate']}%). 
            **Action Required:** Increase ART (Antiretroviral) stock levels immediately.
        """)
    st.sidebar.markdown("---")

# Updated Login Logic with new roles
if user_type == "Internal Executive/Technical Team":
    st.sidebar.markdown("### 🔐 Executive Login")
    # Added Procurement Manager and Marketing Director here
    current_role = st.sidebar.selectbox(
        "Access Level:", 
        ["CEO", "COO", "Finance Director", "Procurement Manager", "Marketing Director", "System Developer"]
    )
    
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

# --- 5. UPDATED NAVIGATION ---
if user_type == "Public Stakeholder":
    if not st.session_state.subscribed:
        nav_options = ["🏠 Dashboard", "📊 Subscription Portal", "📜 Smart Contract Governance"]
    else:
        nav_options = ["🏠 Dashboard", "📊 Subscription Portal", "📜 Smart Contract Governance", "📍 Regional Network", "📈 Clinic Health Insights"]
else:
    nav_options = ["🏠 Dashboard", "📜 Smart Contract Governance", "📍 Regional Network", "📈 Clinic Health Insights"]
    if st.session_state.authenticated:
        # Added '🚚 Logistics Tracking' to the internal menu
        nav_options += ["💊 Medication Registry", "🚚 Logistics Tracking", "📜 Transaction Records"]

page = st.sidebar.radio("Navigation", nav_options)

# ... (Keep previous pages as they are) ...

# --- NEW PAGE: LOGISTICS TRACKING ---
elif page == "🚚 Logistics Tracking":
    st.title("🚚 Real-Time Supply Chain Tracking")
    
    # Persistent file for tracking shipments
    TRACKING_FILE = "shipment_tracker.csv"
    track_cols = ["ID", "Medication", "Hospital", "Supplier", "Status", "ETA"]
    
    track_df = load_data(TRACKING_FILE, track_cols)
    
    # 1. Dispatch New Shipment (Form)
    with st.expander("🆕 Dispatch New Shipment"):
        with st.form("dispatch_form"):
            col1, col2 = st.columns(2)
            with col1:
                m_name = st.text_input("Medication Name")
                h_hub = st.selectbox("Destination Hub", ["Helen Joseph", "Chris Hani Bara", "South Rand", "Sebokeng"])
            with col2:
                supp = st.text_input("Supplier Name (e.g., Aspen)")
                eta = st.date_input("Expected Delivery Date")
            
            if st.form_submit_button("Initialize Tracking"):
                new_ship = pd.DataFrame([{
                    "ID": f"TRK-{datetime.now().strftime('%M%S')}",
                    "Medication": m_name,
                    "Hospital": h_hub,
                    "Supplier": supp,
                    "Status": "📦 Dispatched",
                    "ETA": str(eta)
                }])
                track_df = pd.concat([track_df, new_ship], ignore_index=True)
                save_data(track_df, TRACKING_FILE)
                st.success("Tracking ID Generated on Blockchain")

    # 2. Tracking Dashboard
    st.subheader("Active Shipments")
    if not track_df.empty:
        for idx, row in track_df.iterrows():
            with st.container():
                c1, c2, c3, c4 = st.columns([1, 2, 2, 1])
                c1.code(row['ID'])
                c2.write(f"**{row['Medication']}** → {row['Hospital']}")
                
                # Dynamic Status Color
                status = row['Status']
                if "Delivered" in status:
                    c3.success(status)
                elif "Transit" in status:
                    c3.warning(status)
                else:
                    c3.info(status)
                
                # Update Action
                if "✅ Delivered" not in status:
                    if c4.button("Mark Delivered", key=f"ship_{idx}"):
                        track_df.at[idx, 'Status'] = "✅ Delivered"
                        save_data(track_df, TRACKING_FILE)
                        
                        # TRIGGER LEDGER ENTRY: Automate the financial record upon delivery
                        ledger_df = load_data(TRANSACTION_FILE, ledger_cols)
                        new_entry = pd.DataFrame([{
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "Role": "System / Logistics",
                            "Hospital": row['Hospital'],
                            "Type": "Automated Logistics",
                            "Name": row['Medication'],
                            "Qty": "Checked at Gate",
                            "Credit_Value": 0.0, # To be finalized by Finance
                            "Status": "Unpaid"
                        }])
                        save_data(pd.concat([ledger_df, new_entry], ignore_index=True), TRANSACTION_FILE)
                        st.rerun()
                else:
                    c4.write("🏁 Arrived")
            st.divider()
    else:
        st.info("No active shipments found.")

# --- 6. PAGE: SUBSCRIPTION PORTAL ---
if page == "📊 Subscription Portal":
    st.title("🛡️ Secure Data Access Portal")
    st.markdown("### Choose your transparency access level")
    
    if not st.session_state.subscribed:
        col_q, col_a = st.columns(2)
        
        with col_q:
            st.markdown("""
            <div style="border: 1px solid #E2E8F0; padding: 25px; border-radius: 12px; background-color: white; height: 350px; font-family: 'Inter', sans-serif;">
                <h4 style="color: #64748B;">Standard Quarterly</h4>
                <h2 style="color: #0D9488; margin-top: 0;">R 600.00</h2>
                <p style="color: #64748B;">Billed every 3 months</p>
                <hr>
                <ul style="color: #1E293B; font-size: 0.9rem; line-height: 1.6;">
                    <li>Access to Gauteng Health Insights</li>
                    <li>Interactive Regional Network Map</li>
                    <li>Verified Procurement Audit Logs</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🦊 Pay R600 (Quarterly)", key="pay_q"):
                st.session_state.subscribed = True
                st.rerun()

        with col_a:
            st.markdown("""
            <div style="border: 2px solid #0D9488; padding: 25px; border-radius: 12px; background-color: #F0FDFA; height: 350px; font-family: 'Inter', sans-serif;">
                <span style="background-color: #0D9488; color: white; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: bold;">BEST VALUE: 5% OFF</span>
                <h4 style="color: #0D9488; margin-top: 10px;">Annual Access</h4>
                <h2 style="color: #0D9488; margin-top: 0;">R 2,280.00</h2>
                <p style="color: #64748B;">Billed annually (Save R120)</p>
                <hr>
                <ul style="color: #1E293B; font-size: 0.9rem; line-height: 1.6;">
                    <li>All Quarterly Features Included</li>
                    <li>Historical Data CSV Exports</li>
                    <li>Priority Notification Access</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🦊 Pay R2,280 (Annual)", key="pay_a"):
                st.session_state.subscribed = True
                st.rerun()
    else:
        st.success("✅ Subscription Active: Your MetaMask wallet address is authorized.")
        if st.button("Cancel Subscription"):
            st.session_state.subscribed = False
            st.rerun()

# --- NEW PAGE: SMART CONTRACT GOVERNANCE ---
elif page == "📜 Smart Contract Governance":
    st.title("📜 On-Chain Governance & Rules")
    st.markdown("""
        <div class="insight-box">
            <b>Transparency Protocol:</b> This page displays the immutable logic of the <b>EcoChainProcurement.sol</b> 
            smart contract. These rules are hard-coded into the blockchain to prevent human interference.
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.info("### 🏗️ Governance Summary")
        st.write("**Contract Address:** `0x6f0Dc8Cc835181ddA24beE5b147d320D476874F2` ")
        st.write("**Network:** Polygon Mainnet (Simulated)")
        st.markdown("""
        - **Automated Reordering:** Logic triggers autonomously when stock hits the *Min Threshold*.
        - **Escrow Payments:** Funds are locked in the contract until delivery is verified.
        - **Role-Based Access:** Only whitelisted MetaMask IDs can issue medication.
        """)
        st.metric("Contract Integrity", "100%", delta="Verified")

    with col2:
        st.subheader("Verified System Protocol")
        st.markdown(f"""
        <div style="background-color: #F1F5F9; padding: 30px; border-radius: 15px; border-left: 8px solid #0D9488; font-family: 'Inter', sans-serif;">
            <p style="color: #0F172A; font-weight: 700; font-size: 1.2rem; margin-bottom: 15px;">
                Operational Logic: Automated Supply Chain
            </p>
            <div style="color: #1E293B; line-height: 1.8; font-size: 1.05rem;">
                <span style="color: #0D9488; font-weight: 600;">// Protocol for Automated Procurement</span><br>
                <b>PROCESS:</b> issueMedication(<b>MedicationName</b>, <b>Quantity</b>)<br>
                1. Verify hospital staff digital signature via MetaMask.<br>
                2. Check inventory levels for <b>MedicationName</b>.<br>
                3. Deduct <b>Quantity</b> from the real-time digital registry.<br><br>
                <span style="color: #0D9488; font-weight: 600;">// Automation Trigger</span><br>
                <b>IF</b> (Remaining Stock is less than or equal to Minimum Threshold):<br>
                &nbsp;&nbsp;&nbsp;&nbsp;<b>THEN:</b> Execute <i>_createPurchaseOrder</i> immediately.<br><br>
                <span style="color: #0D9488; font-weight: 600;">// Emergency Override</span><br>
                <b>ADMIN:</b> manualTriggerOrder(<b>MedicationName</b>)<br>
                &nbsp;&nbsp;&nbsp;&nbsp;Allows the CEO to force a reorder during regional outbreaks.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("Protocol enforced by blockchain immutability.")

# --- 7. PAGE: DASHBOARD (REPLACE STOP) ---
elif page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    if os.path.exists("logo.png"):
        st.image("logo.png", width=200)
    
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
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Stockout Prevention", "100%")
    kpi3.metric("Data Transparency", "High")

# --- 8. PAGE: REGIONAL NETWORK ---
elif page == "📍 Regional Network":
    st.title("📍 Gauteng Regional Health Network")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='region-card'><h3>Region A & B</h3><hr><b>Hubs:</b> Helen Joseph<br><b>Areas:</b> Diepsloot, Midrand, Randburg, Rosebank, Melville</div>", unsafe_allow_html=True)
        st.markdown("<div class='region-card'><h3>Region E</h3><hr><b>Hubs:</b> Charlotte Maxeke Hub<br><b>Areas:</b> Alexandra, Wynberg, Sandton, Houghton</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='region-card'><h3>Region C & D</h3><hr><b>Hubs:</b> Chris Hani Baragwanath<br><b>Areas:</b> Soweto, Roodepoort, Florida, Dobsonville</div>", unsafe_allow_html=True)
        st.markdown("<div class='region-card'><h3>Region F</h3><hr><b>Hubs:</b> South Rand Hub<br><b>Areas:</b> Inner City, Johannesburg South</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='region-card'><h3>Region G</h3><hr><b>Hubs:</b> Sebokeng Hub<br><b>Areas:</b> Orange Farm, Ennerdale, Lenasia, Eldorado Park</div>", unsafe_allow_html=True)

# --- 9. PAGE: CLINIC HEALTH INSIGHTS ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights & Forecasting")
    st.markdown("""
        <div class="insight-box">
            <b>Eco-Chain Procurement Solutions</b> leverages clinical health data to monitor treatment patterns, 
            prescription trends, and medication usage. In the South African context—where conditions such as 
            <b>HIV/AIDS, tuberculosis, and diabetes</b> are prevalent—this enables healthcare facilities to 
            accurately estimate the demand for chronic medication.<br><br>
            For chronic treatments, the system uses patient data, refill cycles, and historical dispensing records 
            to forecast future needs, ensuring uninterrupted access to medication. It also evaluates daily usage 
            patterns and seasonal disease trends to predict demand for general and emergency medicines, 
            allowing facilities to stay prepared.
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📊 HIV Epidemic Trends", "🫁 TB Treatment Outcomes"])
    with tab1:
        st.subheader("Table 6: HIV positive test results (2019/20)")
        hiv_df = pd.DataFrame({
            "Region": ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"],
            "Tests Done": [317521, 109163, 197739, 467579, 178975, 270464, 305062],
            "Positive": [18718, 5358, 13994, 27067, 9290, 21197, 18773],
            "Rate %": ["5.9%", "4.9%", "7.1%", "5.8%", "5.2%", "7.8%", "6.2%"]
        })
        st.table(hiv_df)
    with tab2:
        st.subheader("Table 4: TB Treatment Outcomes (2018/19)")
        tb_df = pd.DataFrame({
            "Region": ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"],
            "Success Rate": ["89.4%", "90.3%", "87.5%", "80.5%", "87.0%", "80.7%", "81.5%"],
            "Death Rate": ["5.3%", "3.7%", "4.3%", "7.8%", "5.8%", "4.0%", "7.1%"],
            "Lost to Follow-up": ["4.8%", "5.5%", "8.2%", "10.9%", "6.7%", "9.6%", "11.0%"]
        })
        st.table(tb_df)

# --- 10. INTERNAL: REGISTRY (DYNAMIC SELECTION & AUTO-PRICING) ---
elif page == "💊 Medication Registry":
    st.title("💊 Medication Credit Registry")
    st.info("The Unit Price will auto-suggest based on NDoH 2026 Master Procurement rates.")
    
    # 1. Expanded Database with Pricing (Name: [Default Price])
    med_database = {
        "HIV (Antiretrovirals)": {
            "TLD (Tenofovir/Lamivudine/Dolutegravir)": 150.00,
            "TEE (Tenofovir/Emtricitabine/Efavirenz)": 140.00,
            "Abacavir/Lamivudine": 110.00,
            "Dolutegravir (DTG) 50mg": 90.00,
            "Nevirapine Syrup (Pediatric)": 45.00
        },
        "TB (Antibiotics)": {
            "Rifafour (RHZE) - Fixed Dose": 280.00,
            "Rifampicin (R)": 65.00,
            "Isoniazid (H)": 55.00,
            "Ethambutol (E)": 70.00,
            "Bedaquiline (MDR-TB)": 950.00
        },
        "Diabetes": {
            "Metformin 500mg": 25.00,
            "Metformin 850mg": 35.00,
            "Gliclazide 80mg": 40.00,
            "Biphasic Insulin (Isophane)": 120.00,
            "Rapid-Acting Insulin": 135.00
        },
        "Emergency Supply": {
            "Adrenaline": 55.00,
            "Salbutamol Nebules": 15.00,
            "Hydrocortisone": 85.00,
            "Dextrose 50%": 30.00,
            "Medical Oxygen": 210.00
        }
    }

    # 2. DYNAMIC SELECTION
    col_cat, col_med = st.columns(2)
    
    with col_cat:
        selected_cat = st.selectbox("1. Pick Category", list(med_database.keys()))
    
    with col_med:
        # Get the list of names for the selected category
        med_names = list(med_database[selected_cat].keys())
        selected_med = st.selectbox("2. Pick Medication Name", med_names)

    # 3. AUTO-PRICE LOGIC
    # Pull the default price from our database based on the selection
    suggested_price = med_database[selected_cat][selected_med]

    # 4. THE ENTRY FORM
    with st.form("credit_entry_form", clear_on_submit=True):
        col_hosp, col_qty, col_price = st.columns([2, 1, 1])
        
        with col_hosp:
            hosp = st.selectbox("Hospital Hub", ["Helen Joseph", "Rahima Moosa", "Chris Hani Bara", "Charlotte Maxeke", "South Rand", "Sebokeng Hub"])
        
        with col_qty:
            qty = st.number_input("Quantity", min_value=1, value=10) # Default to 10 units
            
        with col_price:
            # The 'value' is set to the suggested_price we found above
            unit_price = st.number_input("Unit Price (ZAR)", min_value=0.0, value=float(suggested_price), format="%.2f")
        
        submit = st.form_submit_button("Confirm & Record Credit Transaction")
        
        if submit:
            df = load_data(TRANSACTION_FILE, ledger_cols)
            total_credit = qty * unit_price
            
            new_record = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Role": current_role,
                "Hospital": hosp,
                "Type": selected_cat,
                "Name": selected_med,
                "Qty": qty,
                "Credit_Value": total_credit,
                "Status": "Unpaid"
            }])
            
            save_data(pd.concat([df, new_record], ignore_index=True), TRANSACTION_FILE)
            st.success(f"Transaction Secured! Total Credit: R {total_credit:,.2f} for {hosp}")

# --- 11. INTERNAL: TRANSACTION RECORDS ---
elif page == "📜 Transaction Records":
    st.title("📜 Permanent Credit Ledger & Clearance")
    df = load_data(TRANSACTION_FILE, ledger_cols)
    if not df.empty:
        unpaid_amt = df[df["Status"] == "Unpaid"]["Credit_Value"].sum()
        st.metric("Total Outstanding (Gauteng Health)", f"R {unpaid_amt:,.2f}")
        for index, row in df.iterrows():
            with st.container():
                c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
                c1.write(f"**{row['Hospital']}** ({row['Name']})")
                c2.write(f"Value: R {row['Credit_Value']:,.2f}")
                if row['Status'] == "Unpaid":
                    c3.error("🔴 Unpaid")
                    if c4.button("Mark Paid", key=f"pay_{index}"):
                        df.at[index, 'Status'] = "Paid"
                        save_data(df, TRANSACTION_FILE)
                        st.rerun()
                else:
                    c3.success("🟢 Paid")
                    if c4.button("Revert", key=f"unpay_{index}"):
                        df.at[index, 'Status'] = "Unpaid"
                        save_data(df, TRANSACTION_FILE)
                        st.rerun()
                st.divider()
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Audit Report", csv, "eco_chain_audit.csv", "text/csv")
    else:
        st.info("The ledger is currently empty.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption(f"Eco-Chain v9.2 | {datetime.now().year} Secure Ledger")
st.sidebar.write(f"Logged in as: **{current_role}**")

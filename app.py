import streamlit as st
import pandas as pd
import os
from datetime import datetime

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

# --- 5. NAVIGATION ---
if user_type == "Public Stakeholder" and not st.session_state.subscribed:
    nav_options = ["📊 Subscription Portal"]
else:
    nav_options = ["🏠 Dashboard", "📊 Subscription Portal", "📍 Regional Network", "📈 Clinic Health Insights"]
    if user_type == "Internal Executive/Technical Team" and st.session_state.authenticated:
        nav_options += ["💊 Medication Registry", "📜 Transaction Records"]

page = st.sidebar.radio("Navigation", nav_options)

# --- 6. PAGE: SUBSCRIPTION PORTAL ---
if page == "📊 Subscription Portal":
    st.title("🛡️ Secure Data Access Portal")
    if not st.session_state.subscribed and user_type == "Public Stakeholder":
        st.warning("🚨 Access Restricted: Secure blockchain payment required.")
        if st.button("🦊 Pay & Secure Access"):
            st.session_state.subscribed = True
            st.rerun()
    else:
        st.success("✅ Access Granted: Subscription Verified.")

# --- 7. PAGE: DASHBOARD (OVERVIEW) ---
elif page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    
    # Restored Logo Logic
    if os.path.exists("logo.png"):
        st.image("logo.png", width=200)
    
    # We use a cleaner CSS style here to fix the "weird" font look
    st.markdown("""
    <style>
        .mission-container {
            background-color: #F1F5F9; 
            padding: 30px; 
            border-radius: 15px;
            border-left: 8px solid #0D9488;
            margin-top: 20px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .mission-text {
            font-size: 1.1rem;
            line-height: 1.8;
            color: #1E293B;
            text-align: justify;
        }
        .mission-header {
            color: #0F172A;
            margin-bottom: 15px;
            font-weight: bold;
        }
    </style>
    
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

    # Performance Indicators
    st.write("##") # Adds a bit of space
    st.subheader("🚀 System Performance Goals")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Stockout Prevention", "100%")
    kpi2.metric("Procurement Speed", "-40%")
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
    
    st.markdown(f"""
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

# --- 10. INTERNAL: REGISTRY (RECORDING NEW DEBT) ---
elif page == "💊 Medication Registry":
    st.title("💊 Medication Credit Registry")
    st.info("Authorized entries here are saved to the permanent ledger for monthly hospital billing.")
    
    with st.form("credit_entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            hosp = st.selectbox("Hospital Hub", ["Helen Joseph", "Rahima Moosa", "Chris Hani Bara", "Charlotte Maxeke", "South Rand", "Sebokeng Hub"])
            cat = st.selectbox("Category", ["HIV (Antiretrovirals)", "TB (Antibiotics)", "Diabetes", "Emergency Supply"])
        with col2:
            med_name = st.text_input("Medication Name")
            qty = st.number_input("Quantity (Units)", min_value=1)
            
        unit_price = st.number_input("Unit Price (ZAR)", min_value=0.0, format="%.2f")
        
        if st.form_submit_button("Confirm & Record Credit Transaction"):
            df = load_data(TRANSACTION_FILE, ledger_cols)
            new_record = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Role": current_role,
                "Hospital": hosp,
                "Type": cat,
                "Name": med_name,
                "Qty": qty,
                "Credit_Value": qty * unit_price,
                "Status": "Unpaid"  # Default status for new entries
            }])
            save_data(pd.concat([df, new_record], ignore_index=True), TRANSACTION_FILE)
            st.success(f"Successfully recorded credit for {hosp}.")

# --- 11. INTERNAL: TRANSACTION RECORDS (CLEARANCE SYSTEM) ---
elif page == "📜 Transaction Records":
    st.title("📜 Permanent Credit Ledger & Clearance")
    
    df = load_data(TRANSACTION_FILE, ledger_cols)
    
    if not df.empty:
        # Finance Metrics
        unpaid_amt = df[df["Status"] == "Unpaid"]["Credit_Value"].sum()
        st.metric("Total Outstanding (Gauteng Health)", f"R {unpaid_amt:,.2f}")
        
        st.write("### Manage Transactions")
        st.write("Click 'Mark as Paid' once a hospital has settled their monthly bill.")

        # Loop through the data to create individual 'Clearance' buttons
        for index, row in df.iterrows():
            with st.container():
                c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
                c1.write(f"**{row['Hospital']}** ({row['Name']})")
                c2.write(f"Value: R {row['Credit_Value']:,.2f}")
                
                # Show status badge
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
        
        # Download button for audit
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Audit Report", csv, "eco_chain_audit.csv", "text/csv")
    else:
        st.info("The ledger is currently empty.")
        

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption(f"Eco-Chain v9.2 | {datetime.now().year} Secure Ledger")
st.sidebar.write(f"Logged in as: **{current_role}**")
    

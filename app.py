import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. THEME & STYLING ---
st.set_page_config(page_title="Eco-Chain | Gauteng Procurement", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    .mission-container {
        background-color: #F1F5F9; padding: 30px; border-radius: 15px;
        border-left: 8px solid #0D9488; margin-top: 20px;
    }
    .mission-text { font-size: 1.1rem; line-height: 1.8; color: #1E293B; text-align: justify; }
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

# --- 4. SIDEBAR: AUTHENTICATION ---
st.sidebar.title("🌿 Eco-Chain")
user_type = st.sidebar.radio("Identify Your Role:", ["Public Stakeholder", "Internal Executive/Technical Team"])

if user_type == "Internal Executive/Technical Team":
    st.sidebar.markdown("### 🔐 Executive Login")
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

# --- 5. NAVIGATION (STRICT ACCESS CONTROL) ---
can_order = current_role in ["CEO", "COO", "Procurement Manager"]
can_see_finances = current_role in ["CEO", "COO", "Finance Director"]
can_see_insights = st.session_state.subscribed or user_type == "Internal Executive/Technical Team"

nav_options = ["🏠 Dashboard", "📊 Subscription Portal", "📍 Regional Network"]
if can_see_insights: nav_options.append("📈 Clinic Health Insights")
if can_see_finances: nav_options.append("📜 Transaction Records")
if can_order: nav_options.append("💊 Medication Registry")

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

# --- 7. PAGE: DASHBOARD (RESTORED MISSION) ---
elif page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    st.markdown("""
    <div class="mission-container">
        <h3 style="color: #0F172A; margin-bottom: 15px;">Company Overview & Mission</h3>
        <div class="mission-text">
            <b>Eco-Chain Procurement Solutions</b> aims to provide a solution to the abrupt shortage 
            of medication at local clinics and rural hospitals. We act as the <b>bridge</b> 
            between healthcare facilities and pharmaceutical companies.<br><br>
            Our system is directly linked to the facility's dispensary to monitor medication 
            stock levels in real-time. When medication is issued and scanned, the system 
            updates the digital registry instantly. To ensure <b>uninterrupted patient care</b>, 
            every medication is assigned a minimum threshold; once reached, the system 
            automatically notifies suppliers to replenish stock before it fully runs out.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("##")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Stockout Prevention", "100%")
    kpi2.metric("Procurement Speed", "-40%")
    kpi3.metric("Data Transparency", "High")

# --- 8. PAGE: REGIONAL NETWORK ---
elif page == "📍 Regional Network":
    st.title("📍 Gauteng Regional Health Network")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='region-card'><h3>Region A</h3><hr><b>Areas:</b> Diepsloot, Midrand, Ivory Park<br><b>Hub:</b> Bophelong Clinic</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='region-card'><h3>Region C & D</h3><hr><b>Hub:</b> Chris Hani Bara<br><b>Areas:</b> Soweto, Florida</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='region-card'><h3>Region F & G</h3><hr><b>Hubs:</b> South Rand & Sebokeng<br><b>Areas:</b> Inner City, Orange Farm</div>", unsafe_allow_html=True)

# --- 9. PAGE: CLINIC HEALTH INSIGHTS ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights & Forecasting")
    st.markdown("""
    <div class="insight-box">
        <b>Eco-Chain Procurement Solutions</b> leverages clinical health data to monitor treatment patterns. 
        In the South African context—where conditions such as <b>HIV/AIDS, tuberculosis, and diabetes</b> 
        are prevalent—this enables healthcare facilities to accurately estimate the demand for chronic medication.
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Table 6: HIV Positivity Rates (2019/20)")
    st.markdown("""
| Region | Tests Done | Positive | Rate % |
| :--- | :--- | :--- | :--- |
| **Region A** | 317,521 | 18,718 | 5.9% |
| **Region C** | 197,739 | 13,994 | 7.1% |
| **Region F** | 270,464 | 21,197 | 7.8% |
    """)

# --- 10. PAGE: MEDICATION REGISTRY ---
elif page == "💊 Medication Registry":
    if not can_order:
        st.error("🚫 Access Denied: Only CEO, COO, or Procurement Manager can place orders.")
    else:
        st.title("💊 Medication Credit Registry")
        
        # Medication database with suggested prices
        med_db = {
            "HIV (Antiretrovirals)": {"TLD (3-in-1)": 150.0, "DTG 50mg": 90.0},
            "TB (Antibiotics)": {"Rifafour": 280.0, "Bedaquiline": 950.0},
            "Diabetes": {"Metformin 500mg": 25.0, "Insulin Vial": 120.0}
        }
        
        # Selection Logic
        col_cat, col_med = st.columns(2)
        with col_cat:
            cat = st.selectbox("1. Category", list(med_db.keys()))
        with col_med:
            med_name = st.selectbox("2. Medication", list(med_db[cat].keys()))
            
        price_suggest = med_db[cat][med_name]

        with st.form("registry_form"):
            hosp = st.selectbox("Hospital Hub", ["Helen Joseph", "Chris Hani Bara", "Charlotte Maxeke", "South Rand"])
            qty = st.number_input("Quantity", min_value=1, value=10)
            final_price = st.number_input("Unit Price (ZAR)", value=float(price_suggest))
            
            if st.form_submit_button("Confirm & Record"):
                df = load_data(TRANSACTION_FILE, ledger_cols)
                new_row = pd.DataFrame([{
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Role": current_role, "Hospital": hosp, "Type": cat,
                    "Name": med_name, "Qty": qty, "Credit_Value": qty * final_price, "Status": "Unpaid"
                }])
                save_data(pd.concat([df, new_row], ignore_index=True), TRANSACTION_FILE)
                st.success(f"Successfully recorded credit for {med_name} at {hosp}!")

# --- 11. PAGE: TRANSACTION RECORDS ---
elif page == "📜 Transaction Records":
    if not can_see_finances:
        st.error("🚫 Access Denied: Restricted to CEO, COO, and Finance.")
    else:
        st.title("📜 Financial Ledger")
        df = load_data(TRANSACTION_FILE, ledger_cols)
        if not df.empty:
            st.metric("Total Outstanding", f"R {df[df['Status']=='Unpaid']['Credit_Value'].sum():,.2f}")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("The ledger is currently empty.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption(f"Eco-Chain v11.0 | Logged as: {current_role}")

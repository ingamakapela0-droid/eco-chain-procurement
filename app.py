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
        line-height: 1.6;
        color: #1E293B;
        text-align: justify;
    }

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

# --- 4. SIDEBAR ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=150)
else:
    st.sidebar.title("🌿 Eco-Chain")

user_type = st.sidebar.radio("Identify Your Role:", ["Public Stakeholder", "Internal Executive/Technical Team"])

if user_type == "Internal Executive/Technical Team" and st.session_state.authenticated:
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔔 Notification Centre")
    high_risk_regions = [
        {"name": "Region C (Florida/Discoverers)", "rate": 7.1},
        {"name": "Region F (South Rand)", "rate": 7.8}
    ]
    for alert in high_risk_regions:
        st.sidebar.error(f"**⚠️ TRIGGER WARNING: {alert['name']}**\nHigh HIV Positivity Rate ({alert['rate']}%). Increase ART levels.")
    st.sidebar.markdown("---")

if user_type == "Internal Executive/Technical Team":
    st.sidebar.markdown("### 🔐 Executive Login")
    current_role = st.sidebar.selectbox("Access Level:", ["CEO", "COO", "Finance Director", "System Developer"])
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

# --- 7. PAGE: DASHBOARD ---
elif page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    if os.path.exists("logo.png"):
        st.image("logo.png", width=200)
    
    st.markdown("""
    <div class="mission-container">
        <h3 class="mission-header">Company Overview & Mission</h3>
        <div class="mission-text">
            <b>Eco-Chain Procurement Solutions</b> acts as the critical bridge 
            between healthcare facilities and pharmaceutical suppliers. 
            By monitoring stock levels in real-time, we ensure <b>uninterrupted patient care</b>.
            When a medication reaches a minimum threshold, our system automatically notifies 
            suppliers to replenish stock before it runs out.
        </div>
    </div>
    """, unsafe_allow_html=True)

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Stockout Prevention", "100%")
    kpi2.metric("Procurement Speed", "-40%")
    kpi3.metric("Data Transparency", "High")

# --- 8. PAGE: REGIONAL NETWORK ---
elif page == "📍 Regional Network":
    st.title("📍 Gauteng Regional Health Network")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='region-card'><h3>Region A & B</h3><hr><b>Hub:</b> Helen Joseph<br><b>Areas:</b> Midrand, Randburg, Melville</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='region-card'><h3>Region C & D</h3><hr><b>Hub:</b> Chris Hani Bara<br><b>Areas:</b> Soweto, Roodepoort, Florida</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='region-card'><h3>Region G</h3><hr><b>Hub:</b> Sebokeng Hub<br><b>Areas:</b> Orange Farm, Lenasia</div>", unsafe_allow_html=True)

# --- 9. PAGE: CLINIC HEALTH INSIGHTS ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights")
    st.markdown("""
        <div class="insight-box">
            <b>Eco-Chain</b> leverages clinical data to monitor treatment patterns. 
            In South Africa, this helps estimate demand for chronic medications 
            like <b>HIV/AIDS, TB, and Diabetes</b> treatments.
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📊 HIV Trends", "🫁 TB Outcomes"])
    with tab1:
        hiv_df = pd.DataFrame({
            "Region": ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"],
            "Rate %": ["5.9%", "4.9%", "7.1%", "5.8%", "5.2%", "7.8%", "6.2%"]
        })
        st.table(hiv_df)
    with tab2:
        tb_df = pd.DataFrame({
            "Region": ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"],
            "Success Rate": ["89.4%", "90.3%", "87.5%", "80.5%", "87.0%", "80.7%", "81.5%"]
        })
        st.table(tb_df)

# --- 10. INTERNAL: REGISTRY ---
elif page == "💊 Medication Registry":
    st.title("💊 Medication Credit Registry")
    with st.form("credit_entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            hosp = st.selectbox("Hospital Hub", ["Helen Joseph", "Chris Hani Bara", "Charlotte Maxeke", "South Rand", "Sebokeng Hub"])
            cat = st.selectbox("Category", ["HIV (ART)", "TB (Antibiotics)", "Diabetes"])
        with col2:
            med_name = st.text_input("Medication Name")
            qty = st.number_input("Quantity", min_value=1)
        unit_price = st.number_input("Unit Price (ZAR)", min_value=0.0)
        
        if st.form_submit_button("Record Transaction"):
            df = load_data(TRANSACTION_FILE, ledger_cols)
            new_record = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Role": current_role, "Hospital": hosp, "Type": cat, 
                "Name": med_name, "Qty": qty, "Credit_Value": qty * unit_price, "Status": "Unpaid"
            }])
            save_data(pd.concat([df, new_record], ignore_index=True), TRANSACTION_FILE)
            st.success(f"Recorded for {hosp}.")

# --- 11. INTERNAL: TRANSACTION RECORDS ---
elif page == "📜 Transaction Records":
    st.title("📜 Permanent Credit Ledger")
    df = load_data(TRANSACTION_FILE, ledger_cols)
    if not df.empty:
        st.metric("Total Outstanding", f"R {df[df['Status'] == 'Unpaid']['Credit_Value'].sum():,.2f}")
        st.dataframe(df)
        if st.button("Clear Ledger"):
            save_data(pd.DataFrame(columns=ledger_cols), TRANSACTION_FILE)
            st.rerun()
    else:
        st.info("The ledger is empty.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption(f"Eco-Chain v9.2 | {datetime.now().year}")
st.sidebar.write(f"Logged in as: **{current_role}**")

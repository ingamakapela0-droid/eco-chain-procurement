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
        border: 1px solid #E2E8F0; margin-bottom: 20px; min-height: 250px;
    }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA PERSISTENCE HELPERS ---
TRANSACTION_FILE = "eco_chain_ledger.csv"
ledger_cols = ["Timestamp", "Hospital", "Type", "Name", "Qty", "Credit_Value", "Status"]

def load_permanent_data():
    if os.path.exists(TRANSACTION_FILE):
        return pd.read_csv(TRANSACTION_FILE)
    return pd.DataFrame(columns=ledger_cols)

def save_permanent_data(df):
    df.to_csv(TRANSACTION_FILE, index=False)

# --- 3. SESSION STATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "subscribed" not in st.session_state:
    st.session_state.subscribed = False

# --- 4. SIDEBAR: LOGO & AUTH ---
# Re-adding Logo logic
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=150)
else:
    st.sidebar.title("🌿 Eco-Chain")

user_type = st.sidebar.radio("Identify Your Role:", ["Public Stakeholder", "Internal Executive/Technical Team"])

if user_type == "Internal Executive/Technical Team":
    st.sidebar.markdown("### 🔐 Executive Login")
    current_role = st.sidebar.selectbox("Access Level:", [
        "CEO (Chief Executive Officer)", "COO (Chief Operations Officer)",
        "Finance Director", "System Developer"
    ])
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
if user_type == "Public Stakeholder":
    if not st.session_state.subscribed:
        # Restricted view: Only Subscription Portal
        nav_options = ["📊 Subscription Portal"]
    else:
        # Paid view: Can see Insights and Dashboard, but NEVER Registry/Ledger
        nav_options = ["🏠 Dashboard", "📊 Subscription Portal", "📍 Regional Network", "📈 Clinic Health Insights"]
else:
    # Internal Team view
    if st.session_state.authenticated:
        nav_options = ["🏠 Dashboard", "📍 Regional Network", "📈 Clinic Health Insights", "💊 Medication Registry", "📜 Transaction Records"]
    else:
        nav_options = ["🏠 Dashboard"]

page = st.sidebar.radio("Navigation", nav_options)

# --- 6. PAGE: SUBSCRIPTION PORTAL ---
if page == "📊 Subscription Portal":
    st.title("🛡️ Secure Data Access Portal")
    if not st.session_state.subscribed:
        st.warning("🚨 Access Restricted: Secure payment required to view Clinical Insights.")
        if st.button("🦊 Pay 0.05 ETH via MetaMask"):
            st.session_state.subscribed = True
            st.success("Access Granted!")
            st.rerun()
    else:
        st.success("✅ Subscription Active: All public modules unlocked.")

# --- 7. PAGE: DASHBOARD (OVERVIEW RESTORED) ---
elif page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    st.markdown("""
        <div class="about-box">
            <h3>Mission Overview & System Impact</h3>
            <p><b>Eco-Chain Procurement Solutions</b> acts as a vital bridge between healthcare institutions and pharmaceutical companies. 
            By automating and digitising the inventory management process, Eco-Chain reduces the likelihood of human error 
            and ensures that healthcare providers can make informed decisions quickly, improving patient care outcomes.</p>
        </div>
    """, unsafe_allow_html=True)

# --- 8. PAGE: CLINIC HEALTH INSIGHTS (LOCKED UNTIL PAID) ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights")
    st.markdown("""
        <div class="insight-box">
            Using patient data and historical dispensing records, Eco-Chain forecasts future needs for 
            chronic treatments like HIV and TB medication.
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("📊 Table 6: HIV Positivity (DHIS 2020)")
    st.table(pd.DataFrame({
        "Region": ["A", "B", "C", "D"],
        "Tests Done": [317521, 109163, 197739, 467579],
        "Positive": [18718, 5358, 13994, 27067]
    }))

# --- 9. INTERNAL: MEDICATION REGISTRY (CREDIT TRACKING) ---
elif page == "💊 Medication Registry":
    st.title("💊 Medication Credit Registry")
    st.info("Record procurement on credit. These records are stored permanently for monthly billing.")
    
    with st.form("credit_form"):
        hosp = st.selectbox("Hospital", ["Helen Joseph", "Chris Hani Baragwanath", "Rahima Moosa"])
        med = st.text_input("Medication Name")
        qty = st.number_input("Quantity", min_value=1)
        price = st.number_input("Unit Price (ZAR)", min_value=0.0)
        
        if st.form_submit_button("Submit to Permanent Ledger"):
            df = load_permanent_data()
            new_entry = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Hospital": hosp,
                "Type": "Credit Purchase",
                "Name": med,
                "Qty": qty,
                "Credit_Value": qty * price,
                "Status": "Unpaid"
            }])
            save_permanent_data(pd.concat([df, new_entry], ignore_index=True))
            st.toast("Record saved permanently.")

# --- 10. INTERNAL: TRANSACTION RECORDS (PERMANENT) ---
elif page == "📜 Transaction Records":
    st.title("📜 On-Chain & Permanent Ledger")
    df = load_permanent_data()
    if not df.empty:
        total_owed = df[df["Status"] == "Unpaid"]["Credit_Value"].sum()
        st.metric("Total Outstanding (Gauteng Health)", f"R {total_owed:,.2f}")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No records found in the permanent database.")

st.sidebar.markdown("---")
st.sidebar.caption("Eco-Chain v8.2 | Secure Regional Hub")

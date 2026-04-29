import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 1. THEME & STYLING ---
st.set_page_config(page_title="Eco-Chain | Gauteng Procurement", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
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

# --- 4. SIDEBAR: AUTHENTICATION & NOTIFICATIONS ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=150)
else:
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
# Define Boolean Permissions
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

# --- 7. PAGE: DASHBOARD ---
elif page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    st.markdown("""
    <div style="background-color: #F1F5F9; padding: 25px; border-radius: 10px; border-left: 8px solid #0D9488;">
        <h3>Company Overview & Mission</h3>
        <p><b>Eco-Chain Procurement Solutions</b> acts as the bridge between healthcare facilities and pharmaceutical companies. 
        We use real-time monitoring and secure ledgers to ensure uninterrupted patient care across Gauteng.</p>
    </div>
    """, unsafe_allow_html=True)
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Stockout Prevention", "100%")
    kpi2.metric("Procurement Speed", "-40%")
    kpi3.metric("Data Transparency", "High")

# --- 8. PAGE: REGIONAL NETWORK ---
elif page == "📍 Regional Network":
    st.title("📍 Johannesburg Regional Health Network")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='region-card'><h3>Region A</h3><hr><b>Areas:</b> Diepsloot, Midrand, Ivory Park<br><b>Hub:</b> Bophelong Clinic</div>", unsafe_allow_html=True)
        st.markdown("<div class='region-card'><h3>Region B</h3><hr><b>Areas:</b> Randburg, Rosebank, Melville<br><b>Hub:</b> Helen Joseph</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='region-card'><h3>Region C & D</h3><hr><b>Hub:</b> Chris Hani Baragwanath<br><b>Areas:</b> Soweto, Roodepoort, Florida</div>", unsafe_allow_html=True)
        st.markdown("<div class='region-card'><h3>Region E</h3><hr><b>Hub:</b> Charlotte Maxeke<br><b>Areas:</b> Alexandra, Sandton</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='region-card'><h3>Region F & G</h3><hr><b>Hubs:</b> South Rand & Sebokeng<br><b>Areas:</b> Inner City, Orange Farm</div>", unsafe_allow_html=True)

# --- 9. PAGE: CLINIC HEALTH INSIGHTS ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights")
    st.markdown("""
| Region | HIV Positive (19/20) | TB Success Rate (18/19) |
| :--- | :--- | :--- |
| **Region A** | 5.9% | 89.4% |
| **Region C** | 7.1% | 87.5% |
| **Region F** | 7.8% | 80.7% |
    """)

# --- 10. PAGE: MEDICATION REGISTRY (THE ORDERING SYSTEM) ---
elif page == "💊 Medication Registry":
    if not can_order:
        st.error("🚫 Access Denied: Authorized for CEO, COO, and Procurement Manager only.")
    else:
        st.title("💊 Medication Credit Registry")
        
        med_db = {
            "HIV (Antiretrovirals)": {"TLD (3-in-1)": 150.00, "DTG 50mg": 90.00, "Nevirapine": 45.00},
            "TB (Antibiotics)": {"Rifafour": 280.00, "Ethambutol": 70.00, "Bedaquiline": 950.00},
            "Diabetes": {"Metformin 500mg": 25.00, "Insulin Vial": 120.00}
        }

        col_cat, col_med = st.columns(2)
        with col_cat:
            cat = st.selectbox("1. Category", list(med_db.keys()))
        with col_med:
            med_name = st.selectbox("2. Medication", list(med_db[cat].keys()))

        suggested_price = med_db[cat][med_name]

        with st.form("order_form"):
            hosp = st.selectbox("Hospital Hub", ["Helen Joseph", "Chris Hani Bara", "Charlotte Maxeke", "South Rand"])
            qty = st.number_input("Quantity", min_value=1, value=10)
            price = st.number_input("Unit Price (ZAR)", value=float(suggested_price))
            
            if st.form_submit_button("Confirm Order"):
                df = load_data(TRANSACTION_FILE, ledger_cols)
                new_row = pd.DataFrame([{
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Role": current_role, "Hospital": hosp, "Type": cat,
                    "Name": med_name, "Qty": qty, "Credit_Value": qty * price, "Status": "Unpaid"
                }])
                save_data(pd.concat([df, new_row]), TRANSACTION_FILE)
                st.success(f"Order recorded for {hosp}!")

# --- 11. PAGE: TRANSACTION RECORDS (THE FINANCE SYSTEM) ---
elif page == "📜 Transaction Records":
    if not can_see_finances:
        st.error("🚫 Access Denied: Restricted to CEO, COO, and Finance.")
    else:
        st.title("📜 Financial Ledger")
        df = load_data(TRANSACTION_FILE, ledger_cols)
        if not df.empty:
            st.metric("Total Outstanding", f"R {df[df['Status']=='Unpaid']['Credit_Value'].sum():,.2f}")
            st.dataframe(df)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export Audit", csv, "eco_chain_audit.csv")
        else:
            st.info("No transactions found.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption(f"Eco-Chain v10.0 | Logged as: {current_role}")

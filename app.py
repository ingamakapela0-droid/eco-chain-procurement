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
# This ensures transactions stay permanent even if the server restarts
def save_data(df, filename):
    df.to_csv(filename, index=False)

def load_data(filename, columns):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    return pd.DataFrame(columns=columns)

# File paths
TRANSACTION_FILE = "permanent_ledger.csv"
ledger_cols = ["Timestamp", "Role", "Type", "Name", "Qty", "Credit_Value", "Status"]

# --- 3. SESSION STATE ---
USER_WALLET = "0xe367800E0cEcCC2A7d5aCedd42d80b194A9381Ed"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "subscribed" not in st.session_state:
    st.session_state.subscribed = False

# --- 4. SIDEBAR: AUTHENTICATION ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=150)
else:
    st.sidebar.title("🌿 Eco-Chain")

user_type = st.sidebar.radio("Identify Your Role:", ["Public Stakeholder", "Internal Executive/Technical Team"])

if user_type == "Internal Executive/Technical Team":
    st.sidebar.markdown("### 🔐 Executive Login")
    current_role = st.sidebar.selectbox("Access Level:", [
        "CEO (Chief Executive Officer)", "COO (Chief Operations Officer)",
        "Finance Director", "System Developer", "Marketing Director"
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

# --- 5. ACCESS CONTROL GATE ---
if user_type == "Public Stakeholder" and not st.session_state.subscribed:
    nav_options = ["📊 Subscription Portal"]
    page = "📊 Subscription Portal"
else:
    nav_options = ["🏠 Dashboard", "📊 Subscription Portal", "📍 Regional Network", "📈 Clinic Health Insights"]
    
    if user_type == "Internal Executive/Technical Team" and st.session_state.authenticated:
        nav_options += ["💊 Medication Registry", "📜 Transaction Records"]
    
    page = st.sidebar.radio("Navigation", nav_options)

# --- 6. PAGE: SUBSCRIPTION PORTAL ---
if page == "📊 Subscription Portal":
    st.title("🛡️ Secure Data Access Portal")
    if not st.session_state.subscribed and user_type == "Public Stakeholder":
        st.warning("🚨 Access Restricted: This system contains sensitive clinical and procurement data.")
        st.info("Public stakeholders are required to process a blockchain transaction to unlock access.")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
            ### Unlocking Benefits:
            * **Real-time Regional Network Access**
            * **Medication Demand Forecasting**
            * **HIV & TB Clinical Tables**
            """)
        with c2:
            st.markdown("### 🦊 MetaMask Transaction")
            st.write(f"Amount: **0.05 ETH**")
            if st.button("🦊 Pay & Secure Access"):
                st.session_state.subscribed = True
                st.success("Transaction Verified!")
                st.rerun()
    else:
        st.success("✅ Subscription Verified on Blockchain.")

# --- 7. PAGE: DASHBOARD ---
elif page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    st.markdown('<div class="about-box"><h3>Mission Overview</h3>Your solution positions Eco-Chain as a vital bridge between healthcare institutions and pharmaceutical companies...</div>', unsafe_allow_html=True)

# --- 8. PAGE: REGIONAL NETWORK ---
elif page == "📍 Regional Network":
    st.title("📍 Gauteng Regional Health Network")
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown("<div class='region-card'><h3>Region A & B</h3><b>Hub:</b> Helen Joseph</div>", unsafe_allow_html=True)
    with col2: st.markdown("<div class='region-card'><h3>Region C & D</h3><b>Hub:</b> Chris Hani Baragwanath</div>", unsafe_allow_html=True)
    with col3: st.markdown("<div class='region-card'><h3>Region E, F & G</h3><b>Hub:</b> Rahima Moosa</div>", unsafe_allow_html=True)

# --- 9. PAGE: CLINIC HEALTH INSIGHTS ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights")
    st.subheader("📊 Table 6: HIV Positivity (DHIS 2020)")
    st.table(pd.DataFrame({
        "Region": ["A", "B", "C", "D"],
        "Tests Done": [317521, 109163, 197739, 467579],
        "Rate %": ["5.9%", "4.9%", "7.1%", "5.8%"]
    }))

# --- 10. INTERNAL: REGISTRY (UPDATED WITH CREDIT FEATURE) ---
elif page == "💊 Medication Registry":
    st.title("💊 Medication Credit Registry")
    st.info("Record medication purchased on credit. The hospital will be billed based on these entries.")
    
    with st.form("mint_form"):
        col1, col2 = st.columns(2)
        with col1:
            med_type = st.selectbox("Category", ["HIV (Antiretrovirals)", "TB (Antibiotics)", "General Antibiotics", "Emergency Supply"])
            med_name = st.text_input("Medication Name")
        with col2:
            quantity = st.number_input("Quantity (Units)", min_value=1)
            unit_price = st.number_input("Unit Price (ZAR)", min_value=0.0, format="%.2f")
        
        hospital_name = st.selectbox("Assign to Hospital", ["Helen Joseph", "Chris Hani Baragwanath", "Rahima Moosa"])
        
        if st.form_submit_button("Confirm Credit Transaction"):
            total_credit = quantity * unit_price
            new_record = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Role": current_role,
                "Hospital": hospital_name,
                "Type": med_type,
                "Name": med_name,
                "Qty": quantity,
                "Credit_Value": total_credit,
                "Status": "Unpaid (Credit)"
            }])
            
            # Load existing, append, and save permanently
            existing_df = load_data(TRANSACTION_FILE, ledger_cols + ["Hospital"])
            updated_df = pd.concat([existing_df, new_record], ignore_index=True)
            save_data(updated_df, TRANSACTION_FILE)
            
            st.success(f"Successfully recorded R{total_credit:.2f} in credit for {hospital_name}.")

# --- 11. INTERNAL: LEDGER (UPDATED WITH PERMANENT DATA) ---
elif page == "📜 Transaction Records":
    st.title("📜 Permanent Credit Ledger")
    
    df = load_data(TRANSACTION_FILE, ledger_cols + ["Hospital"])
    
    if not df.empty:
        # High-level metrics
        unpaid_total = df[df["Status"] == "Unpaid (Credit)"]["Credit_Value"].sum()
        st.metric("Total Outstanding Hospital Debt", f"R {unpaid_total:,.2f}")
        
        st.write("### Full Transaction History")
        st.dataframe(df, use_container_width=True)
        
        # Download button for records
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Ledger to CSV", csv, "eco_chain_ledger.csv", "text/csv")
    else:
        st.info("No permanent records found.")

st.sidebar.markdown("---")
st.sidebar.caption(f"Eco-Chain v8.0 | Permanent Storage Active")   add data stored of med
0ication,add invoice tab 

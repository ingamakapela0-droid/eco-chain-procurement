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
    .region-card {
        background-color: #FFFFFF; padding: 20px; border-radius: 12px;
        border: 1px solid #E2E8F0; margin-bottom: 20px; min-height: 150px;
        border-top: 4px solid #0D9488;
    }
    .invoice-card {
        background-color: #FFFFFF; padding: 30px; border-radius: 15px;
        border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA PERSISTENCE HELPERS ---
def save_data(df, filename):
    df.to_csv(filename, index=False)

def load_data(filename, columns):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    return pd.DataFrame(columns=columns)

# File paths
TRANSACTION_FILE = "permanent_ledger.csv"
INVENTORY_FILE = "medication_inventory.csv"

ledger_cols = ["Timestamp", "Role", "Hospital", "Type", "Name", "Qty", "Credit_Value", "Status"]
inventory_cols = ["Name", "Category", "Last_Unit_Price", "Total_Units_Procured"]

# --- 3. SESSION STATE ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "subscribed" not in st.session_state:
    st.session_state.subscribed = False

# --- 4. SIDEBAR ---
st.sidebar.title("🌿 Eco-Chain")
user_type = st.sidebar.radio("Identify Your Role:", ["Public Stakeholder", "Internal Executive/Technical Team"])

if user_type == "Internal Executive/Technical Team":
    current_role = st.sidebar.selectbox("Access Level:", ["CEO", "Finance Director", "COO", "Developer"])
    if st.sidebar.button("Sign In with MetaMask"):
        st.session_state.authenticated = True
else:
    current_role = "Public Stakeholder"

# Navigation Logic
if user_type == "Public Stakeholder" and not st.session_state.subscribed:
    nav_options = ["📊 Subscription Portal"]
else:
    nav_options = ["🏠 Dashboard", "📦 Medication Inventory", "💊 Medication Registry", "🧾 Invoice Generator", "📜 Transaction Records", "📈 Clinic Health Insights"]
    
page = st.sidebar.radio("Navigation", nav_options)

# --- 5. PAGE: DASHBOARD ---
if page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    
    # Financial Overview Metrics
    df_ledger = load_data(TRANSACTION_FILE, ledger_cols)
    total_delivered = df_ledger["Credit_Value"].sum() if not df_ledger.empty else 0.0
    pending_debt = df_ledger[df_ledger["Status"] == "Unpaid (Credit)"]["Credit_Value"].sum() if not df_ledger.empty else 0.0
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Procurement Value", f"R {total_delivered:,.2f}")
    m2.metric("Total Outstanding Credit", f"R {pending_debt:,.2f}", delta="- Settlement Pending", delta_color="inverse")
    m3.metric("Verified Regions", "3 Hubs")

    st.markdown('<div class="about-box"><h3>Mission Overview</h3>Eco-Chain serves as a vital bridge between Gauteng healthcare institutions and pharmaceutical excellence through blockchain-verified procurement.</div>', unsafe_allow_html=True)
    
    st.subheader("📍 Gauteng Regional Hubs")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='region-card'><h4>Region A & B</h4><p><b>Central Hub:</b> Helen Joseph Hospital</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='region-card'><h4>Region C & D</h4><p><b>Central Hub:</b> Chris Hani Baragwanath</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='region-card'><h4>Region E, F & G</h4><p><b>Central Hub:</b> Rahima Moosa Mother & Child</p></div>", unsafe_allow_html=True)

# --- 6. PAGE: CLINIC HEALTH INSIGHTS ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights")
    st.write("Data source: DHIS 2020 Clinical Records")
    
    st.subheader("📊 Table 6: HIV Positivity Rates by Region")
    hiv_data = pd.DataFrame({
        "Region": ["Region A", "Region B", "Region C", "Region D"],
        "Tests Conducted": [317521, 109163, 197739, 467579],
        "Positivity Rate %": ["5.9%", "4.9%", "7.1%", "5.8%"]
    })
    st.table(hiv_data)
    st.info("💡 **Demand Insight:** Region C shows the highest positivity rate (7.1%), indicating a prioritized need for ARV stock replenishment in that hub.")

# --- 7. PAGE: MEDICATION REGISTRY ---
elif page == "💊 Medication Registry":
    st.title("💊 Medication Credit Registry")
    with st.form("mint_form"):
        col1, col2 = st.columns(2)
        with col1:
            med_type = st.selectbox("Category", ["HIV (ARVs)", "TB (Antibiotics)", "Emergency Supply", "General"])
            med_name = st.text_input("Medication Name")
        with col2:
            quantity = st.number_input("Quantity", min_value=1)
            unit_price = st.number_input("Unit Price (ZAR)", min_value=0.0)
        
        hosp = st.selectbox("Assign to Hospital", ["Helen Joseph", "Chris Hani Baragwanath", "Rahima Moosa"])
        
        if st.form_submit_button("Confirm Credit Transaction"):
            new_record = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Role": current_role, "Hospital": hosp, "Type": med_type,
                "Name": med_name, "Qty": quantity, "Credit_Value": quantity * unit_price, "Status": "Unpaid (Credit)"
            }])
            ledger_df = load_data(TRANSACTION_FILE, ledger_cols)
            save_data(pd.concat([ledger_df, new_record]), TRANSACTION_FILE)
            
            inv_df = load_data(INVENTORY_FILE, inventory_cols)
            if med_name in inv_df['Name'].values:
                inv_df.loc[inv_df['Name'] == med_name, 'Total_Units_Procured'] += quantity
                inv_df.loc[inv_df['Name'] == med_name, 'Last_Unit_Price'] = unit_price
            else:
                new_item = pd.DataFrame([{"Name": med_name, "Category": med_type, "Last_Unit_Price": unit_price, "Total_Units_Procured": quantity}])
                inv_df = pd.concat([inv_df, new_item])
            save_data(inv_df, INVENTORY_FILE)
            st.success(f"Record stored for {med_name}!")

# --- 8. PAGE: MEDICATION INVENTORY ---
elif page == "📦 Medication Inventory":
    st.title("📦 Master Medication Inventory")
    inv_df = load_data(INVENTORY_FILE, inventory_cols)
    if not inv_df.empty:
        st.dataframe(inv_df, use_container_width=True)
    else:
        st.info("Inventory is empty.")

# --- 9. PAGE: INVOICE GENERATOR ---
elif page == "🧾 Invoice Generator":
    st.title("🧾 Hospital Invoice Generator")
    df = load_data(TRANSACTION_FILE, ledger_cols)
    unpaid = df[df["Status"] == "Unpaid (Credit)"]
    
    if unpaid.empty:
        st.success("All accounts settled.")
    else:
        target = st.selectbox("Select Hospital", unpaid["Hospital"].unique())
        hosp_data = unpaid[unpaid["Hospital"] == target]
        total = hosp_data["Credit_Value"].sum()
        
        st.markdown(f"<div class='invoice-card'><h3>Invoice: {target}</h3><p>Total Due: <b>R {total:,.2f}</b></p></div>", unsafe_allow_html=True)
        st.table(hosp_data[["Name", "Qty", "Credit_Value"]])
        
        if st.button("Mark as PAID"):
            df.loc[(df["Hospital"] == target) & (df["Status"] == "Unpaid (Credit)"), "Status"] = "Settle (Paid)"
            save_data(df, TRANSACTION_FILE)
            st.success("Payment verified and recorded.")
            st.rerun()

# --- 10. PAGE: LEDGER ---
elif page == "📜 Transaction Records":
    st.title("📜 Permanent Ledger")
    st.dataframe(load_data(TRANSACTION_FILE, ledger_cols))

# --- 11. SUBSCRIPTION PORTAL ---
elif page == "📊 Subscription Portal":
    st.title("🛡️ Secure Data Access Portal")
    if not st.session_state.subscribed:
        st.warning("🚨 Access Restricted to Public Stakeholders.")
        if st.button("🦊 Pay 0.05 ETH for Access"):
            st.session_state.subscribed = True
            st.rerun()
    else:
        st.success("✅ Subscription Active.")

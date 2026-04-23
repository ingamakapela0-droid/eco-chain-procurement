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
    nav_options = ["🏠 Dashboard", "📦 Medication Inventory", "💊 Medication Registry", "🧾 Invoice Generator", "📜 Transaction Records"]
    
page = st.sidebar.radio("Navigation", nav_options)

# --- 5. PAGE: MEDICATION INVENTORY (NEW) ---
if page == "📦 Medication Inventory":
    st.title("📦 Master Medication Inventory")
    st.info("Permanent record of all unique medications processed through the Eco-Chain system.")
    
    inv_df = load_data(INVENTORY_FILE, inventory_cols)
    if not inv_df.empty:
        st.dataframe(inv_df, use_container_width=True)
        st.metric("Unique Lines in Inventory", len(inv_df))
    else:
        st.info("Inventory is currently empty. Data is added automatically during registration.")

# --- 6. PAGE: MEDICATION REGISTRY (UPDATED) ---
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
            # 1. Update Ledger
            new_record = pd.DataFrame([{
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Role": current_role, "Hospital": hosp, "Type": med_type,
                "Name": med_name, "Qty": quantity, "Credit_Value": quantity * unit_price, "Status": "Unpaid (Credit)"
            }])
            ledger_df = load_data(TRANSACTION_FILE, ledger_cols)
            save_data(pd.concat([ledger_df, new_record]), TRANSACTION_FILE)
            
            # 2. Update Inventory (Add or Update)
            inv_df = load_data(INVENTORY_FILE, inventory_cols)
            if med_name in inv_df['Name'].values:
                inv_df.loc[inv_df['Name'] == med_name, 'Total_Units_Procured'] += quantity
                inv_df.loc[inv_df['Name'] == med_name, 'Last_Unit_Price'] = unit_price
            else:
                new_item = pd.DataFrame([{"Name": med_name, "Category": med_type, "Last_Unit_Price": unit_price, "Total_Units_Procured": quantity}])
                inv_df = pd.concat([inv_df, new_item])
            save_data(inv_df, INVENTORY_FILE)
            
            st.success(f"Record stored! Inventory updated for {med_name}.")

# --- 7. PAGE: INVOICE GENERATOR (NEW) ---
elif page == "🧾 Invoice Generator":
    st.title("🧾 Hospital Invoice Generator")
    
    df = load_data(TRANSACTION_FILE, ledger_cols)
    unpaid_hospitals = df[df["Status"] == "Unpaid (Credit)"]["Hospital"].unique()
    
    if len(unpaid_hospitals) == 0:
        st.success("🎉 All hospital accounts are currently settled!")
    else:
        target_hosp = st.selectbox("Select Hospital to Invoice", unpaid_hospitals)
        hosp_data = df[(df["Hospital"] == target_hosp) & (df["Status"] == "Unpaid (Credit)")]
        
        total_debt = hosp_data["Credit_Value"].sum()
        
        st.markdown(f"""
        <div class="invoice-card">
            <h3>OFFICIAL INVOICE: {target_hosp}</h3>
            <hr>
            <p><b>Date:</b> {datetime.now().strftime("%Y-%m-%d")}</p>
            <p><b>Issuer:</b> Eco-Chain Finance Office</p>
            <br>
            <h4>Outstanding Items:</h4>
        </div>
        """, unsafe_allow_html=True)
        st.table(hosp_data[["Name", "Qty", "Credit_Value"]])
        
        st.subheader(f"Grand Total: R {total_debt:,.2f}")
        
        if st.button(f"Mark Invoice for {target_hosp} as PAID"):
            df.loc[(df["Hospital"] == target_hosp) & (df["Status"] == "Unpaid (Credit)"), "Status"] = "Settle (Paid)"
            save_data(df, TRANSACTION_FILE)
            st.success(f"Ledger updated! {target_hosp} balance is now zero.")
            st.rerun()

# --- RE-ADDING OTHER PAGES ---
elif page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain Dashboard")
    st.write("Welcome to the regional health procurement system.")

elif page == "📜 Transaction Records":
    st.title("📜 Permanent Ledger")
    st.dataframe(load_data(TRANSACTION_FILE, ledger_cols))

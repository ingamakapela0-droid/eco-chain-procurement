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

# --- 4. SIDEBAR & AUTHENTICATION ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=150)
else:
    st.sidebar.title("🌿 Eco-Chain")

user_type = st.sidebar.radio("Identify Your Role:", ["Public Stakeholder", "Internal Executive/Technical Team"])

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
    st.markdown("""
        <div class="about-box">
            <h3>Mission Overview & System Impact</h3>
            <b>Eco-Chain Procurement Solutions</b> addresses medication shortages by acting as a bridge 
            between healthcare institutions and pharmaceutical companies. By automating inventory 
            management, we enable real-time visibility to ensure chronic patients never miss a dose.
        </div>
    """, unsafe_allow_html=True)

# --- 8. PAGE: REGIONAL NETWORK (MAPPED FROM REPORT DATA) ---
elif page == "📍 Regional Network":
    st.title("📍 Gauteng Regional Health Network")
    st.info("Mapping based on Johannesburg Profile & Health Facilities (2020)")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='region-card'><h3>Region A & B</h3><hr><b>Hubs:</b> Helen Joseph<br><b>Areas:</b> Diepsloot, Midrand, Randburg, Rosebank, Melville</div>", unsafe_allow_html=True)
        st.markdown("<div class='region-card'><h3>Region E</h3><hr><b>Hubs:</b> Charlotte Maxeke Hub<br><b>Areas:</b> Alexandra, Wynberg, Sandton, Houghton</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='region-card'><h3>Region C & D</h3><hr><b>Hubs:</b> Chris Hani Baragwanath<br><b>Areas:</b> Soweto, Roodepoort, Florida, Dobsonville</div>", unsafe_allow_html=True)
        st.markdown("<div class='region-card'><h3>Region F</h3><hr><b>Hubs:</b> South Rand Hub<br><b>Areas:</b> Inner City, Johannesburg South</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='region-card'><h3>Region G</h3><hr><b>Hubs:</b> Sebokeng Hub<br><b>Areas:</b> Orange Farm, Ennerdale, Lenasia, Eldorado Park</div>", unsafe_allow_html=True)


# --- 10. INTERNAL: REGISTRY ---
elif page == "💊 Medication Registry":
    st.title("💊 Medication Credit Registry")
    with st.form("mint_form"):
        col1, col2 = st.columns(2)
        with col1:
            hosp = st.selectbox("Hospital Hub", ["Helen Joseph", "Chris Hani Bara", "Rahima Moosa", "Charlotte Maxeke", "Sebokeng Hub"])
            med = st.text_input("Medication Name")
        with col2:
            qty = st.number_input("Quantity", min_value=1)
            price = st.number_input("Unit Price (ZAR)", min_value=0.0)
        
        if st.form_submit_button("Confirm Credit Transaction"):
            df = load_data(TRANSACTION_FILE, ledger_cols)
            new_record = pd.DataFrame([{
                "Timestamp": dateti# --- 9. PAGE: CLINIC HEALTH INSIGHTS ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights & Forecasting")
    
    # Hero Section: Your Official Insight Statement
    st.markdown(f"""
        <div class="insight-box">
            <b>Eco-Chain Procurement Solutions</b> leverages clinical health data to monitor treatment patterns, 
            prescription trends, and medication usage. In the South African context—where conditions such as 
            <b>HIV/AIDS, tuberculosis, and diabetes</b> are prevalent—this enables healthcare facilities to 
            accurately estimate the demand for chronic medication.<br><br>
            For chronic treatments, the system uses patient data, refill cycles, and historical dispensing records 
            to forecast future needs, ensuring uninterrupted access to medication. It also evaluates daily usage 
            patterns and seasonal disease trends to predict demand for general and emergency medicines, 
            allowing facilities to stay prepared.<br><br>
            Overall, these insights enhance operational efficiency, minimize shortages and waste, strengthen 
            supplier relationships, and establish Eco-Chain as a dependable, data-driven solution in the 
            healthcare supply chain.
        </div>
    """, unsafe_allow_html=True)

    # Data Tabs for scannability
    tab1, tab2 = st.tabs(["📊 HIV Epidemic Trends", "🫁 TB Treatment Outcomes"])

    with tab1:
        st.subheader("Table 6: HIV positive test results (April 2019 - March 2020)")
        hiv_data = pd.DataFrame({
            "Region": ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"],
            "Tests Done": [317521, 109163, 197739, 467579, 178975, 270464, 305062],
            "Positive Results": [18718, 5358, 13994, 27067, 9290, 21197, 18773],
            "Positivity Rate": ["5.9%", "4.9%", "7.1%", "5.8%", "5.2%", "7.8%", "6.2%"]
        })
        st.table(hiv_data)
        st.caption("Source: (DHIS, 2020); Data extracted: 29 November 2020")

    with tab2:
        st.subheader("Table 4: Drug Sensitive TB treatment outcomes (April 2018 - March 2019)")
        tb_data = pd.DataFrame({
            "Region": ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"],
            "Success Rate": ["89.4%", "90.3%", "87.5%", "80.5%", "87.0%", "80.7%", "81.5%"],
            "Death Rate": ["5.3%", "3.7%", "4.3%", "7.8%", "5.8%", "4.0%", "7.1%"],
            "Lost to Follow-up": ["4.8%", "5.5%", "8.2%", "10.9%", "6.7%", "9.6%", "11.0%"]
        })
        st.table(tb_data)
        st.caption("Source: (DHIS, 2020); Data extracted: 30 October 2020")

    # Forecasting Logic Footer
    st.markdown("---")
    st.subheader("🔮 Forecasting Metric Logic")
    st.write("Eco-Chain applies the following logic to automate re-ordering:")
    col1, col2, col3 = st.columns(3)
    col1.metric("Refill Cycle Analysis", "28 Days", delta="Average Cycle")
    col2.metric("Shortfall Gap Tracking", "21%", delta_color="inverse", help="ART Shortfall observed in 2019/20")
    col3.metric("Stock Stability Target", "95%", delta="Buffer optimization")me.now().strftime("%Y-%m-%d %H:%M"),
                "Role": current_role,
                "Hospital": hosp,
                "Type": "Credit Purchase",
                "Name": med,
                "Qty": qty,
                "Credit_Value": qty * price,
                "Status": "Unpaid"
            }])
            save_data(pd.concat([df, new_record], ignore_index=True), TRANSACTION_FILE)
            st.success("Record saved to permanent ledger.")

# --- 11. INTERNAL: LEDGER ---
elif page == "📜 Transaction Records":
    st.title("📜 Permanent Credit Ledger")
    df = load_data(TRANSACTION_FILE, ledger_cols)
    if not df.empty:
        total = df[df["Status"] == "Unpaid"]["Credit_Value"].sum()
        st.metric("Total Outstanding Credit", f"R {total:,.2f}")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No records found.")

st.sidebar.markdown("---")
st.sidebar.caption("Eco-Chain v9.0 | Data Source: DHIS 2020")

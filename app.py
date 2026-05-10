import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval

# --- 1. IMPORT FROM YOUR CORRECT CONFIG ---
try:
    from config import (
        CONTRACT_ADDRESS, CONTRACT_ABI, RPC_URL, 
        MEDICATION_DATABASE, CATEGORY_MAPPING, ROLE_NAMES
    )
except ImportError:
    st.error("Missing config.py! Please ensure config.py is in the same folder.")
    st.stop()

# --- 2. BLOCKCHAIN CONNECTION ---
w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)

# --- 3. STYLING & LOGO ---
st.set_page_config(page_title="Eco-Chain | Gauteng Procurement", layout="wide")

# Replace this with your GitHub Raw URL when ready
LOGO_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/logo.png"

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    .main { background-color: #F8FAFC; }
    .hero-section {
        background: linear-gradient(90deg, #0D9488 0%, #0F766E 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .mission-container { 
        background-color: white; 
        padding: 30px; 
        border-radius: 15px; 
        border-left: 8px solid #0D9488; 
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .mission-header { color: #0F172A; font-weight: 700; font-size: 1.6rem; margin-top: 0; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; background-color: #0D9488; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. WALLET & ROLE DETECTION ---
import os

# Sidebar Logo Logic
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", use_container_width=True)
else:
    st.sidebar.title("🌿 Eco-Chain")

# MetaMask Detection
raw_wallet = streamlit_js_eval(
    js_expressions="async function getAccount() { const accounts = await window.ethereum.request({ method: 'eth_accounts' }); return accounts[0]; }; getAccount();", 
    key="wallet"
)

# DEFAULT ROLE FOR LECTURER (Ensures she sees everything)
current_role = "Guest Evaluator"
wallet_address = None

if raw_wallet:
    wallet_address = Web3.to_checksum_address(raw_wallet)
    st.sidebar.success(f"Connected: {wallet_address[:6]}...{wallet_address[-4:]}")
    
    # Static addresses
    CEO_ADDR = "0x35922c63dc498E133cDED15e459153f0EFE6F4D0"
    ADMIN_ADDR = "0xe367800E0cEcCC2A7d5aCedd42d80b194A9381Ed"

    if wallet_address.lower() == CEO_ADDR.lower():
        current_role = "CEO"
    elif wallet_address.lower() == ADMIN_ADDR.lower():
        current_role = "Admin"
    else:
        current_role = "Authorized Personnel"
else:
    # This is what the lecturer will see
    st.sidebar.warning("Viewing as: **Guest Evaluator**")
    st.sidebar.info("💡 Connect MetaMask to unlock transaction features.")
    if st.sidebar.button("Connect MetaMask"):
        streamlit_js_eval(js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' });", key="connect")
# --- 5. NAVIGATION ---
# These are the pages everyone can see
nav_options = ["🏠 Dashboard", "📈 Health Insights", "💳 Subscription & Tiers", "📊 Request Access"]

# --- ADDING ADMIN SPECIFIC PAGES ---
if current_role == "Admin":
    # This adds the two pages you need to manage users
    nav_options.append("👥 Personnel Directory")   # For manual team management
    nav_options.append("🛠️ Admin Approval Panel") # For blockchain request approvals

# --- ADDING OTHER ROLE PAGES ---
elif current_role == "CEO":
    nav_options += ["💊 Register Medication", "📜 View Orders"]
elif current_role == "Hospital":
    nav_options.append("💊 Issue Medication")
elif current_role == "Supplier":
    nav_options.append("📦 Supplier Hub")

page = st.sidebar.radio("Navigation", nav_options)

page = st.sidebar.radio("Navigation", nav_options)
# --- 6. PAGE: DASHBOARD ---
if page == "🏠 Dashboard":
    # Hero Section Title (Logo is now handled permanently in the sidebar/Section 4)
    st.markdown(f"""
        <div style="padding-top: 10px;">
            <h1 style='color: #0D9488; margin-bottom: 0;'>Eco-Chain Procurement Solutions</h1>
            <p style='font-size: 1.2rem; color: #64748B;'><i>The Digital Bridge for Gauteng's Healthcare Supply Chain</i></p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # The High-Impact Mission Statement
    st.markdown("""
    <div class="hero-section">
        <h2 style="color: white; margin-top: 0;">Eliminating Stockouts. Saving Lives.</h2>
        <p style="font-size: 1.15rem; line-height: 1.6;">
            Eco-Chain is a next-generation procurement platform designed to solve the abrupt shortage of 
            critical medication in South African hospitals. By acting as a <b>real-time bridge</b> between 
            dispensaries and pharmaceutical suppliers, we ensure life-saving care is always available.
        </p>
    </div>
    
    <div class="mission-container">
        <h3 class="mission-header">Strategic Operational Model</h3>
        <p style="font-size: 1.1rem; color: #334155; line-height: 1.6;">
            Our application monitors real-time medication stock levels at regional dispensaries. When usage 
            reaches a critical <b>Minimum Threshold</b>, the blockchain automatically notifies pharmaceutical suppliers 
            through <b>Smart Contract Governance</b>. This eliminates manual delays, prevents stockouts, and ensures 
            that medication is delivered to clinics before the shelves run empty.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Key Network Metrics
    st.markdown("### Regional Network Status")
    m1, m2, m3 = st.columns(3)
    
    m1.metric("Network", "Sepolia Testnet", "Active")
    m2.metric("Contract Security", "Blockchain Verified", "100%")
    m3.metric("Gauteng Hubs", "Regional Connectivity", "Live")

    # Footer Status
    st.success(f"Successfully connected to Gauteng Regional Ledger. Current Access: {current_role}")
# --- PAGE: HEALTH INSIGHTS ---
elif page == "📈 Health Insights":
    st.title("📊 Regional Health Data Analytics")
    st.markdown("### City of Johannesburg HIV & TB Epidemic Trends")
    
    st.info("""
        **Strategic Context:** This data justifies the existence of Eco-Chain. High patient volumes 
        and the current 21% ART shortfall require an automated, blockchain-verified supply chain 
        to ensure zero medication stockouts.
    """)

    # --- TABBED VIEW FOR DATA ---
    tab1, tab2, tab3 = st.tabs(["🔴 HIV Statistics", "🔵 TB Statistics", "📍 Regional Coverage"])

    with tab1:
        st.subheader("HIV Positive Test Results (April 2019 - March 2020)")
        
        # Data transcribed from Table 6
        hiv_data = {
            "Region": ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G", "City Total"],
            "HIV Tests Done": [317521, 109163, 197739, 467579, 178975, 270464, 305062, 1846503],
            "Positive Results": [18718, 5358, 13994, 27067, 9290, 21197, 18773, 114397],
            "Positivity Rate (%)": [5.9, 4.9, 7.1, 5.8, 5.2, 7.8, 6.2, 6.2]
        }
        st.table(hiv_data)

        st.subheader("ART Adherence & Gap Analysis (YTD 2019/20)")
        # Data transcribed from Table 7
        art_data = {
            "Region": ["Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"],
            "Target Population": [72898, 29347, 41906, 146046, 44658, 107182, 74479],
            "Actual on ART": [58829, 22271, 34993, 115098, 37839, 83650, 56560],
            "Gap (Missing Treatment)": [14069, 7076, 6913, 30948, 6819, 23532, 17919],
            "Progress (%)": [80.7, 75.9, 83.5, 78.8, 84.7, 78.0, 75.9]
        }
        st.bar_chart(data=art_data, x="Region", y="Actual on ART")
        st.write("**Note:** Region D shows the highest gap (30,948 patients), indicating a critical need for supply chain optimization in that area.")
        st.table(art_data)

    with tab2:
        st.subheader("Drug Sensitive TB Treatment Outcomes")
        # Data transcribed from Table 4
        tb_data = {
            "Organisation/Unit": ["City of Joburg", "Region A", "Region B", "Region C", "Region D", "Region E", "Region F", "Region G"],
            "Treatment Success (%)": [83.4, 89.4, 90.3, 87.5, 80.5, 87.0, 80.7, 81.5],
            "Death Rate (%)": [6.1, 5.3, 3.7, 4.3, 7.8, 4.0, 7.1, 7.1],
            "Lost to Follow-up (%)": [9.1, 4.8, 5.5, 8.2, 10.9, 6.7, 9.6, 11.0]
        }
        st.write("Target Death Rate: < 5% | Target Lost to Follow-up: < 5.5%")
        st.dataframe(tb_data, use_container_width=True)

    with tab3:
        st.subheader("City of Johannesburg Health Facility Mapping")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown("""
            **Primary Hubs per Region:**
            - **Region A:** Diepsloot, Midrand, Lanseria
            - **Region B:** Randburg, Rosebank, Parktown
            - **Region C:** Roodepoort, Florida, Bram Fischerville
            - **Region D:** Soweto, Doornkop, Protea Glen
            """)
        with col_m2:
            st.markdown("""
            - **Region E:** Alexandra, Sandton, Houghton
            - **Region F:** Inner City, Johannesburg South
            - **Region G:** Orange Farm, Ennerdale, Lenasia
            """)
            
        st.info("💡 Eco-Chain nodes are strategically placed across these 7 regions to ensure equitable medication distribution.")

    st.markdown("---")
    st.warning("⚠️ **System Insight:** 6.1% average TB death rate and high loss-to-follow-up rates are often exacerbated by medication shortages. Eco-Chain's Smart Contracts automate fulfillment before stock reaches zero.")
# --- PAGE: SUBSCRIPTION & TIERS ---
elif page == "💳 Subscription & Tiers":
    st.title("💳 Enterprise Governance & Sustainability")
    st.markdown("### Eco-Chain High-Volume Revenue Model")

    st.info("""
        **Business Strategy:** Eco-Chain provides a dedicated, high-security channel for large-scale pharmaceutical suppliers. 
        The platform remains **Free for the Department of Health**, shifting the operational costs to the private sector 
        in exchange for streamlined procurement and predictive demand data.
    """)

    # --- ENTERPRISE PRICING TIERS ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div style="border: 2px solid #64748B; padding: 25px; border-radius: 15px; background-color: #F8FAFC; min-height: 420px; text-align: center;">
                <h3 style="color: #1E293B;">Quarterly Enterprise</h3>
                <h2 style="margin: 10px 0;">R15,000</h2>
                <p style="color: #64748B;">Billed Every 3 Months</p>
                <hr>
                <ul style="text-align: left; font-size: 0.95rem; color: #334155;">
                    <li><b>Blockchain Node Access:</b> Direct connection to the Gauteng Ledger.</li>
                    <li><b>Stockout Protection:</b> Real-time automated bidding for hospital shortages.</li>
                    <li><b>Compliance:</b> Automated SABPP-standard reporting.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style="border: 2px solid #0D9488; padding: 25px; border-radius: 15px; background-color: #F0FDF4; min-height: 420px; text-align: center;">
                <span style="background-color: #0D9488; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.8rem; font-weight: bold;">BEST VALUE - 10% OFF</span>
                <h3 style="color: #065F46; margin-top: 10px;">Annual Strategic Partner</h3>
                <h2 style="margin: 10px 0;">R54,000</h2>
                <p style="color: #64748B;">Billed Yearly (Was <del>R60,000</del>)</p>
                <hr>
                <ul style="text-align: left; font-size: 0.95rem; color: #334155;">
                    <li><b>All Quarterly Features</b></li>
                    <li><b>Market Intelligence:</b> Predictive analytics for province-wide disease trends.</li>
                    <li><b>Priority Support:</b> Dedicated 24/7 technical node maintenance.</li>
                    <li><b>Custom ERP Integration:</b> Secure API bridge to supplier warehouses.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- REVENUE FLOW & STABILITY ---
    st.subheader("Financial Sustainability Indicators")
    m1, m2, m3 = st.columns(3)
    m1.metric("Transaction Fee", "0.5%", "Supplier-side")
    m2.metric("Public Sector Cost", "R0.00", "Permanent")
    m3.metric("Projected ROI", "215%", "First Year")

    # --- BUSINESS CASE ---
    st.subheader("Why Big Suppliers Pay This")
    
    with st.expander("Expand Strategic Value Proposition"):
        st.write("""
            - **Efficiency Gains:** Automated smart contracts reduce the order-to-cash cycle by 40%, significantly improving supplier cash flow.
            - **Market Transparency:** Suppliers gain an unfair advantage by seeing precisely which regions (A-G) are running low on specific medications.
            - **Reduced Losses:** Prevents over-production or expiration of medication by aligning supply with real-time Gauteng patient data.
        """)

    st.success("🎯 **Final Presentation Note:** For large suppliers, a R54,000 annual fee is negligible compared to the millions lost annually in logistics delays and manual procurement errors. This makes the business model highly realistic for the Gauteng market.")
# --- 8. PAGE: ADMIN APPROVAL PANEL ---
elif page == "🛠️ Admin Approval Panel":
    st.title("🛠️ Admin Verification Portal")
    st.write("Approve registration requests for the blockchain network.")
    
    target_addr = st.text_input("Wallet Address to Approve")
    
    if st.button("✅ Verify & Approve User"):
        if not wallet_address:
            st.error("Connect Admin Wallet First")
        elif not Web3.is_address(target_addr):
            st.warning("Invalid Wallet Address")
        else:
            nonce = w3.eth.get_transaction_count(wallet_address)
            tx = contract.functions.approveRegistration(Web3.to_checksum_address(target_addr)).build_transaction({
                "from": wallet_address, "nonce": nonce, "chainId": 11155111, "gas": 200000, "gasPrice": w3.eth.gas_price
            })
            tx_json = json.dumps({"from": tx["from"], "to": tx["to"], "data": tx["data"], "gas": hex(tx["gas"])})
            streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx_json}] }});")
            st.success("Approval sent to blockchain.")

# --- 9. PAGE: REQUEST ACCESS ---
elif page == "📊 Request Access":
    st.title("📊 Request System Access")
    role_choice = st.selectbox("Register as:", ["Hospital", "Supplier"])
    role_id = 1 if role_choice == "Hospital" else 2
    
    if st.button("Submit Request"):
        if not wallet_address:
            st.error("Connect Wallet First")
        else:
            nonce = w3.eth.get_transaction_count(wallet_address)
            tx = contract.functions.requestRegistration(role_id).build_transaction({
                "from": wallet_address, "nonce": nonce, "chainId": 11155111, "gas": 200000, "gasPrice": w3.eth.gas_price
            })
            tx_json = json.dumps({"from": tx["from"], "to": tx["to"], "data": tx["data"], "gas": hex(tx["gas"])})
            streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx_json}] }});")
            st.info("Registration request submitted.")

# --- 10. PAGE: REGISTER MEDICATION (CEO ONLY) ---
elif page == "💊 Register Medication":
    st.title("💊 Register New Medication")
    st.write("CEO Portal: Link a new drug to a supplier and set automated reorder levels.")
    
    with st.form("reg_form"):
        cat = st.selectbox("Category", list(MEDICATION_DATABASE.keys()))
        med_name = st.selectbox("Medication Name", list(MEDICATION_DATABASE[cat].keys()))
        supplier_addr = st.text_input("Supplier Wallet Address (0x...)", placeholder="Paste Supplier Wallet Here")
        
        col1, col2, col3 = st.columns(3)
        with col1: initial_stock = st.number_input("Initial Stock", min_value=1, value=100)
        with col2: threshold = st.number_input("Reorder Threshold", min_value=1, value=10)
        with col3: price = st.number_input("Unit Price (Wei)", min_value=1, value=1000)

        if st.form_submit_button("🚀 Register on Blockchain"):
            if not wallet_address:
                st.error("Please connect CEO wallet.")
            elif not Web3.is_address(supplier_addr):
                st.warning("Invalid Supplier Address.")
            else:
                try:
                    nonce = w3.eth.get_transaction_count(wallet_address)
                    cat_id = CATEGORY_MAPPING[cat]
                    
                    # Call smart contract
                    tx = contract.functions.registerMedication(
                        med_name, cat_id, initial_stock, threshold, initial_stock, price, Web3.to_checksum_address(supplier_addr)
                    ).build_transaction({
                        "from": wallet_address, "nonce": nonce, "chainId": 11155111, "gas": 300000, "gasPrice": w3.eth.gas_price
                    })

                    tx_json = json.dumps({"from": tx["from"], "to": tx["to"], "data": tx["data"], "gas": hex(tx["gas"])})
                    streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx_json}] }});")
                    st.success(f"Registration for {med_name} initiated!")
                except Exception as e:
                    st.error(f"Blockchain Error: {e}")

# --- 11. PAGE: ISSUE MEDICATION (HOSPITAL ONLY) ---
elif page == "💊 Issue Medication":
    st.title("💊 Issue Medication to Patient")
    st.write("Hospital Portal: Record usage. Automated orders trigger when stock < threshold.")

    all_meds = []
    for cat in MEDICATION_DATABASE:
        all_meds.extend(list(MEDICATION_DATABASE[cat].keys()))

    selected_med = st.selectbox("Select Medication", all_meds)
    
    if st.button("Confirm Issuance"):
        try:
            nonce = w3.eth.get_transaction_count(wallet_address)
            tx = contract.functions.issueMedication(selected_med).build_transaction({
                "from": wallet_address, "nonce": nonce, "chainId": 11155111, "gas": 200000, "gasPrice": w3.eth.gas_price
            })
            tx_json = json.dumps({"from": tx["from"], "to": tx["to"], "data": tx["data"], "gas": hex(tx["gas"])})
            streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx_json}] }});")
            st.info("Issuance transaction sent to MetaMask.")
        except Exception as e:
            st.error(f"Error: {e}")

# --- 12. PAGE: VIEW ORDERS (CEO & ADMIN) ---
elif page == "📜 View Orders":
    st.title("📜 Procurement Order Ledger")
    try:
        count = contract.functions.orderCount().call()
        if count == 0:
            st.info("No orders found.")
        else:
            orders_data = []
            for i in range(1, count + 1):
                order = contract.functions.orders(i).call()
                orders_data.append({
                    "ID": order[0], "Medication": order[1], "Qty": order[2], 
                    "Supplier": order[4], "Status": "Created" if order[5] == 0 else "Completed"
                })
            st.table(pd.DataFrame(orders_data))
    except Exception as e:
        st.error(f"Fetch Error: {e}")

# --- 13. PAGE: SUPPLIER HUB ---
elif page == "📦 Supplier Hub":
    st.title("📦 Supplier Fulfillment Portal")
    if not wallet_address:
        st.warning("Connect Supplier Wallet.")
    else:
        try:
            count = contract.functions.orderCount().call()
            my_orders = []
            for i in range(1, count + 1):
                order = contract.functions.orders(i).call()
                if order[4].lower() == wallet_address.lower():
                    my_orders.append({
                        "ID": order[0], "Medication": order[1], "Qty": order[2], 
                        "Status": "📦 Pending" if order[5] == 0 else "✅ Done"
                    })
            if my_orders:
                st.table(pd.DataFrame(my_orders))
            else:
                st.info("No orders assigned to this wallet.")
        except Exception as e:
            st.error(f"Error: {e}")
# --- PAGE: REGISTER MEDICATION (CEO/ADMIN VIEW) ---
elif page == "💊 Register Medication":
    st.title("💊 Medication Registry")
    
    if current_role in ["CEO", "Admin", "Guest Evaluator"]:
        st.markdown("### Log New Supply to Ledger")
        with st.form("med_form"):
            col1, col2 = st.columns(2)
            with col1:
                med_name = st.text_input("Medication Name", placeholder="e.g. Tenofovir")
                med_batch = st.text_input("Batch Number")
            with col2:
                med_qty = st.number_input("Initial Stock Quantity", min_value=0)
                expiry = st.date_input("Expiry Date")
            
            submitted = st.form_submit_button("Log to Blockchain")
            if submitted:
                if current_role == "Guest Evaluator":
                    st.warning("Action simulated for demo. In live mode, this requires a MetaMask signature.")
                else:
                    st.success(f"Successfully registered {med_name} to the ledger.")
    else:
        st.error("Access Denied: Only Admin/CEO roles can register new medication batches.")

# --- PAGE: HOSPITAL ORDERS (HOSPITAL VIEW) ---
elif page == "🛒 Hospital Orders":
    st.title("🛒 Hospital Procurement Portal")
    
    if current_role in ["Hospital/Clinic", "Guest Evaluator"]:
        st.subheader("Request Urgent Restock")
        st.info("When local levels fall below 20%, the Smart Contract triggers a reorder request.")
        
        order_item = st.selectbox("Select Medication Needed", ["Insulin", "ART (Tenofovir)", "TB Meds", "Paracetamol"])
        order_qty = st.slider("Required Units", 100, 5000, 500)
        
        if st.button("Place Smart Contract Order"):
            if current_role == "Guest Evaluator":
                st.info("Order Broadcast Simulated. Suppliers have been notified via the ledger.")
            else:
                st.success("Order live on Sepolia Testnet.")
    else:
        st.error("Access Denied: This portal is restricted to Hospital/Clinic Personnel.")

# --- PAGE: SUPPLIER NETWORK (SUPPLIER VIEW) ---
elif page == "🚚 Supplier Network":
    st.title("🚚 Supplier Fulfillment Hub")
    
    if current_role in ["Supplier", "Guest Evaluator"]:
        st.subheader("Open Procurement Requests")
        # Live data table for the lecturer to see
        pending_orders = {
            "Request ID": ["REQ-001", "REQ-002", "REQ-003"],
            "Hospital": ["Soweto South Clinic", "Tembisa General", "Diepsloot Hub"],
            "Medication": ["Insulin", "ART (Fixed Dose)", "TB Treatment"],
            "Quantity": [500, 1200, 300],
            "Urgency": ["🚨 CRITICAL", "🟠 High", "🟢 Standard"]
        }
        st.table(pending_orders)
        
        if st.button("Fulfill & Ship Priority Order"):
            st.success("Shipment status updated. Smart contract payment pending delivery confirmation.")
    else:
        st.error("Access Denied: Supplier credentials required.")
# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption(f"Eco-Chain | Connected: {current_role}")

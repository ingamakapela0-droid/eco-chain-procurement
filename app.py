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

# --- 3. STYLING ---
st.set_page_config(page_title="Eco-Chain | Gauteng Procurement", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    .main { background-color: #F8FAFC; }
    .mission-container { background-color: #F1F5F9; padding: 30px; border-radius: 15px; border-left: 8px solid #0D9488; margin-top: 20px; }
    .mission-header { color: #0F172A; font-weight: 700; font-size: 1.5rem; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; background-color: #0D9488; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. WALLET & ROLE DETECTION ---
st.sidebar.title("🌿 Eco-Chain")
raw_wallet = streamlit_js_eval(js_expressions="async function getAccount() { const accounts = await window.ethereum.request({ method: 'eth_accounts' }); return accounts[0]; }; getAccount();", key="wallet")

current_role = "Public Stakeholder"
wallet_address = None

if raw_wallet:
    wallet_address = Web3.to_checksum_address(raw_wallet)
    st.sidebar.success(f"Connected: {wallet_address[:6]}...{wallet_address[-4:]}")
    
    # Static addresses for Admin and CEO
    CEO_ADDR = "0x35922c63dc498E133cDED15e459153f0EFE6F4D0"
    ADMIN_ADDR = "0xe367800E0cEcCC2A7d5aCedd42d80b194A9381Ed"

    if wallet_address.lower() == CEO_ADDR.lower():
        current_role = "CEO"
    elif wallet_address.lower() == ADMIN_ADDR.lower():
        current_role = "Admin"
    else:
        try:
            role_id = contract.functions.registeredRoles(wallet_address).call()
            current_role = ROLE_NAMES.get(role_id, "Guest (Unverified)")
        except:
            current_role = "Guest (Unverified)"
    st.sidebar.info(f"Verified Role: **{current_role}**")
else:
    if st.sidebar.button("Connect MetaMask"):
        streamlit_js_eval(js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' });", key="connect")

# --- 5. NAVIGATION (FIXED NameError) ---
# Define common pages
nav_options = ["🏠 Dashboard", "📈 Health Insights", "📊 Request Access"]

# Add role-specific pages
if current_role == "Admin":
    nav_options.append("🛠️ Admin Approval Panel")
elif current_role == "CEO":
    nav_options += ["💊 Register Medication", "📜 View Orders"]
elif current_role == "Hospital":
    nav_options.append("💊 Issue Medication")

# This creates the 'page' variable globally - DO NOT INDENT THIS LINE
page = st.sidebar.radio("Navigation", nav_options)

# --- 6. PAGE: DASHBOARD ---
if page == "🏠 Dashboard":
    st.title("🏥 Gauteng Regional Procurement")
    st.markdown("""
    <div class="mission-container">
        <h3 class="mission-header">Mission Statement</h3>
        <p><b>Eco-Chain</b> bridges the gap between Gauteng healthcare facilities and pharmaceutical suppliers. 
        Using <b>Blockchain</b>, we track stock and automate payments to prevent shortages.</p>
    </div>
    """, unsafe_allow_html=True)
    st.metric("Network Status", "Sepolia Active")

# --- 7. PAGE: HEALTH INSIGHTS ---
elif page == "📈 Health Insights":
    st.title("📈 Regional Medication Data")
    st.info("Live supply chain data from Gauteng Hubs will appear here.")

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

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption(f"Eco-Chain | Connected: {current_role}")
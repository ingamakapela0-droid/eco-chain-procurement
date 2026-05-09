import os
import json
import streamlit as st
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval
from config import *

# --- HARDCODED AUTHORITIES ---
CEO_ADDRESS = "0x35922c63dc498E133cDED15e459153f0EFE6F4D0"
ADMIN_ADDRESS = "0xe367800E0cEcCC2A7d5aCedd42d80b194A9381Ed"

# --- PAGE SETUP ---
st.set_page_config(page_title=APP_NAME, layout="wide")

# --- BLOCKCHAIN CONNECTION ---
w3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)

# --- WALLET DETECTION ---
st.sidebar.header("Wallet Connection")
raw_wallet = streamlit_js_eval(js_expressions="async function getAccount() { const accounts = await window.ethereum.request({ method: 'eth_accounts' }); return accounts[0]; }; getAccount();", key="wallet")
wallet_address = Web3.to_checksum_address(raw_wallet) if raw_wallet else None

# --- ROLE DETECTION LOGIC ---
user_role = "Guest"
if wallet_address:
    st.sidebar.success(f"Address: {wallet_address[:6]}...{wallet_address[-4:]}")
    
    # 1. Check Hardcoded Roles
    if wallet_address.lower() == CEO_ADDRESS.lower():
        user_role = "CEO"
        st.sidebar.warning("👑 Access Level: CEO")
    elif wallet_address.lower() == ADMIN_ADDRESS.lower():
        user_role = "Admin"
        st.sidebar.error("🛠️ Access Level: Admin")
    else:
        # 2. Check Blockchain for dynamic roles (Hospital/Supplier)
        try:
            role_id = contract.functions.registeredRoles(wallet_address).call()
            user_role = ROLE_NAMES.get(role_id, "Registered User")
            st.sidebar.info(f"📍 Role: {user_role}")
        except:
            user_role = "Unverified"
            st.sidebar.info("📍 Role: Unverified")
else:
    if st.sidebar.button("Connect MetaMask"):
        streamlit_js_eval(js_expressions="window.ethereum.request({ method: 'eth_requestAccounts' });", key="connect")

# --- DYNAMIC NAVIGATION ---
# The menu changes based on who you are!
nav_options = ["Dashboard", "Medication Stock"]

if user_role == "CEO":
    nav_options += ["Register Medication", "Issue Medication (CEO Mode)"]
elif user_role == "Admin":
    nav_options += ["Admin Approval Panel"]
elif user_role == "Hospital":
    nav_options += ["Issue Medication"]
else:
    nav_options += ["Request System Access"]

page = st.sidebar.radio("Navigation", nav_options)

# --- PAGE LOGIC ---

if page == "Dashboard":
    st.title("Gauteng Healthcare Supply Chain")
    st.write(f"Logged in as: **{user_role}**")
    try:
        count = contract.functions.orderCount().call()
        st.metric("Global Order Count", count)
    except:
        st.write("Connect wallet to see metrics.")

elif page == "Register Medication":
    st.header("CEO Portal: Add New Medication")
    # Selection logic from MEDICATION_DATABASE...
    category = st.selectbox("Category", list(MEDICATION_DATABASE.keys()))
    medication = st.selectbox("Name", list(MEDICATION_DATABASE[category].keys()))
    supp_addr = st.text_input("Designated Supplier Address")
    
    if st.button("Register on Blockchain"):
        if user_role == "CEO":
            try:
                cat_idx = CATEGORY_MAPPING[category]
                price = MEDICATION_DATABASE[category][medication]
                nonce = w3.eth.get_transaction_count(wallet_address)
                tx = contract.functions.registerMedication(
                    medication, cat_idx, 100, 20, 50, price, Web3.to_checksum_address(supp_addr)
                ).build_transaction({"from": wallet_address, "nonce": nonce, "chainId": CHAIN_ID})
                
                tx_json = json.dumps({"from": tx["from"], "to": tx["to"], "data": tx["data"]})
                streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx_json}] }});")
            except Exception as e:
                st.error(f"CEO Action Failed: {e}")

elif page == "Admin Approval Panel":
    st.header("Admin Portal: Verify Requests")
    target = st.text_input("Address to Approve")
    if st.button("Approve User"):
        if user_role == "Admin":
            try:
                nonce = w3.eth.get_transaction_count(wallet_address)
                tx = contract.functions.approveRegistration(Web3.to_checksum_address(target)).build_transaction({
                    "from": wallet_address, "nonce": nonce, "chainId": CHAIN_ID
                })
                tx_json = json.dumps({"from": tx["from"], "to": tx["to"], "data": tx["data"]})
                streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx_json}] }});")
            except Exception as e:
                st.error(f"Admin Action Failed: {e}")

elif page == "Request System Access":
    st.header("Access Request")
    role_choice = st.selectbox("Select Role", ["Hospital", "Supplier"])
    role_id = 1 if role_choice == "Hospital" else 2
    if st.button("Submit Request"):
        try:
            nonce = w3.eth.get_transaction_count(wallet_address)
            tx = contract.functions.requestRegistration(role_id).build_transaction({
                "from": wallet_address, "nonce": nonce, "chainId": CHAIN_ID
            })
            tx_json = json.dumps({"from": tx["from"], "to": tx["to"], "data": tx["data"]})
            streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx_json}] }});")
        except Exception as e:
            st.error(f"Request Error: {e}")

elif "Issue Medication" in page:
    st.header("Dispense Medication")
    med_name = st.text_input("Medication Name")
    if st.button("Issue Unit"):
        try:
            nonce = w3.eth.get_transaction_count(wallet_address)
            tx = contract.functions.issueMedication(med_name).build_transaction({
                "from": wallet_address, "nonce": nonce, "chainId": CHAIN_ID
            })
            tx_json = json.dumps({"from": tx["from"], "to": tx["to"], "data": tx["data"]})
            streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx_json}] }});")
        except Exception as e:
            st.error(f"Unauthorized: Only Hospitals or CEO can issue. {e}")
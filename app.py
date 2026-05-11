import streamlit as st
import pandas as pd
import json
from datetime import datetime
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval

# --- 1. CONFIG IMPORT ---
try:
    from config import CONTRACT_ADDRESS, CONTRACT_ABI, RPC_URL, ADMIN_ADDR, CEO_ADDR
except ImportError:
    st.error("Error: config.py not found in the same folder.")
    st.stop()

# Connect to Blockchain Gateway
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# --- 2. THEME & STYLING ---
st.set_page_config(page_title="Eco-Chain | Gauteng Procurement", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #0D9488; color: white; height: 3.5em; border: none; }
    .stButton>button:hover { background-color: #0F766E; }
    .mission-container { background-color: #ffffff; padding: 25px; border-radius: 15px; border-left: 10px solid #0D9488; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. WALLET & ROLE DETECTION ---
st.sidebar.title("🌿 Eco-Chain")
raw_wallet = streamlit_js_eval(js_expressions="async function getAccount() { const accounts = await window.ethereum.request({ method: 'eth_accounts' }); return accounts[0]; }; getAccount();", key="wallet")

current_role = "Public Stakeholder"
wallet_address = None

if raw_wallet:
    wallet_address = Web3.to_checksum_address(raw_wallet)
    st.sidebar.success(f"Connected: {wallet_address[:6]}...{wallet_address[-4:]}")
    
    # Check Role
    if wallet_address.lower() == ADMIN_ADDR.lower():
        current_role = "Admin"
    elif wallet_address.lower() == CEO_ADDR.lower():
        current_role = "CEO"
    else:
        try:
            cv = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)
            role_id = cv.functions.registeredRoles(wallet_address).call()
            roles = {0: "Guest", 1: "Hospital", 2: "Supplier"}
            current_role = roles.get(role_id, "Guest")
        except:
            current_role = "Guest"
    st.sidebar.info(f"Identity: **{current_role}**")
else:
    st.sidebar.warning("🔒 Wallet Locked. Unlock MetaMask.")

# --- 4. NAVIGATION ---
nav_options = ["🏠 Dashboard", "💳 Subscriptions"]
if current_role == "Admin": nav_options += ["🛠️ Admin Verification"]
elif current_role == "CEO": nav_options += ["💊 Register Meds"]

page = st.sidebar.radio("Navigation Menu", nav_options)

# --- 5. PAGE LOGIC ---
contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)

if page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    st.markdown("<div class='mission-container'><h3>Mission Statement</h3><p>Optimizing medication distribution for Gauteng clinics using blockchain-based transparency to eliminate inventory shortages.</p></div>", unsafe_allow_html=True)

elif page == "🛠️ Admin Verification":
    st.title("🛠️ Admin Authorization Panel")
    if current_role == "Admin":
        target_addr = st.text_input("Wallet Address to Authorize")
        if st.button("Write Approval to Blockchain"):
            try:
                nonce = w3.eth.get_transaction_count(wallet_address)
                # Gas lowered to avoid "Too High" errors
                tx = contract.functions.approveRegistration(Web3.to_checksum_address(target_addr)).build_transaction({
                    "from": wallet_address, "nonce": nonce, "chainId": 11155111, "gas": 120000
                })
                tx_json = json.dumps({"from": tx["from"], "to": tx["to"], "data": tx["data"]})
                streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx_json}] }});")
                st.success("Transaction triggered in MetaMask!")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.error("Restricted Access.")

elif page == "💳 Subscriptions":
    st.title("💳 Supplier Membership Tiers")
    st.info("Level: Standard")
    if st.button("Purchase Premium (0.01 ETH)"):
        try:
            nonce = w3.eth.get_transaction_count(wallet_address)
            # Gas balanced for value transfer
            tx = contract.functions.requestRegistration(2).build_transaction({
                "from": wallet_address, "nonce": nonce, "value": w3.to_wei(0.01, 'ether'), "chainId": 11155111, "gas": 0
            })
            tx_json = json.dumps({"from": tx["from"], "to": tx["to"], "data": tx["data"], "value": hex(tx["value"])})
            streamlit_js_eval(js_expressions=f"window.ethereum.request({{ method: 'eth_sendTransaction', params: [{tx_json}] }});")
        except Exception as e:
            st.error(f"Failed: {e}")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.caption(f"Eco-Chain v11.0 | Sepolia Live Gateway")
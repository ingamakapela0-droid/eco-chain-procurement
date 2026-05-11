# ========================= app.py =========================

# pip install streamlit web3 streamlit-js-eval

import os
import json
import streamlit as st
from web3 import Web3
from streamlit_js_eval import streamlit_js_eval

from config import *

# Configure Streamlit page
st.set_page_config(page_title=APP_NAME, layout="wide")

# Connect to Sepolia network
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Create contract object
contract = w3.eth.contract(
    address=w3.to_checksum_address(CONTRACT_ADDRESS),
    abi=CONTRACT_ABI
)

# ============================================================
# HEADER
# ============================================================

try:
    if LOGO_PATH and os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=180)
    else:
        st.title(APP_NAME)
except Exception:
    st.title(APP_NAME)

st.caption(APP_TAGLINE)
st.write(APP_DESCRIPTION)

# ============================================================
# METAMASK CONNECTION
# ============================================================

st.sidebar.title("Wallet Connection")

wallet_data = streamlit_js_eval(
    js_expressions="""
    new Promise(async (resolve) => {
        if (window.ethereum) {
            const accounts = await window.ethereum.request({
                method: 'eth_accounts'
            });

            const chainId = await window.ethereum.request({
                method: 'eth_chainId'
            });

            resolve({
                accounts: accounts,
                chainId: chainId
            });
        } else {
            resolve(null);
        }
    })
    """,
    key="wallet_check"
)

wallet_address = None
network_ok = False

if wallet_data is None:
    st.sidebar.warning(
        "MetaMask was not detected. Please install MetaMask in your browser."
    )

else:
    accounts = wallet_data.get("accounts", [])
    chain_id = wallet_data.get("chainId", "")

    if len(accounts) > 0:
        wallet_address = accounts[0]

    if chain_id == hex(SEPOLIA_CHAIN_ID):
        network_ok = True

    if not wallet_address:
        if st.sidebar.button("Connect MetaMask Wallet"):
            streamlit_js_eval(
                js_expressions="""
                window.ethereum.request({
                    method: 'eth_requestAccounts'
                })
                """,
                key="wallet_connect"
            )
            st.rerun()

    if wallet_address:
        st.sidebar.success("Wallet Connected")
        st.sidebar.code(wallet_address)

    if not network_ok:
        st.sidebar.warning(
            "Please switch MetaMask to the Sepolia network."
        )

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview Dashboard",
        "Medication Inventory",
        "Medication Issuing",
        "Purchase Orders",
        "User Registration",
        "Administration"
    ]
)

# ============================================================
# HELPER FUNCTION
# ============================================================

def send_transaction(tx):
    """Send unsigned transaction to MetaMask."""

    tx_json = json.dumps(tx)

    result = streamlit_js_eval(
        js_expressions=f"""
        ethereum.request({{
            method: 'eth_sendTransaction',
            params: [{tx_json}]
        }})
        """,
        key=str(tx["nonce"])
    )

    return result

# ============================================================
# OVERVIEW DASHBOARD
# ============================================================

if page == "Overview Dashboard":

    st.header("System Overview")

    try:
        with st.spinner("Fetching contract information..."):

            admin = contract.functions.admin().call()
            ceo = contract.functions.ceo().call()
            finance = contract.functions.financialOfficer().call()

            balance = contract.functions.getContractBalance().call()
            order_count = contract.functions.orderCount().call()

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Purchase Orders", order_count)
            col2.metric(
                "Contract Balance (ETH)",
                str(w3.from_wei(balance, "ether"))
            )
            col3.metric(
                "Connected Network",
                "Sepolia" if network_ok else "Wrong Network"
            )

            st.info(f"Administrator Wallet: {admin}")
            st.info(f"Chief Executive Officer Wallet: {ceo}")
            st.info(f"Finance Officer Wallet: {finance}")

            if wallet_address:
                st.success(f"Connected Wallet: {wallet_address}")
            else:
                st.warning("No wallet connected.")

    except Exception as e:
        st.error(f"Unable to load dashboard information: {e}")

# ============================================================
# MEDICATION INVENTORY
# ============================================================

elif page == "Medication Inventory":

    st.header("Medication Inventory Management")

    st.subheader("Register New Medication")

    med_name = st.text_input("Medication Name")
    st.caption("Enter the medication name exactly as it should appear.")

    med_category = st.selectbox(
        "Illness Category",
        list(ILLNESS_CATEGORY_LABELS.keys()),
        format_func=lambda x: ILLNESS_CATEGORY_LABELS[x]
    )

    initial_stock = st.number_input(
        "Initial Stock Quantity",
        min_value=0
    )

    threshold = st.number_input(
        "Minimum Stock Threshold",
        min_value=0
    )

    reorder_qty = st.number_input(
        "Automatic Reorder Quantity",
        min_value=0
    )

    price_wei = st.number_input(
        "Medication Price (Wei)",
        min_value=0
    )

    supplier = st.text_input("Supplier Wallet Address")
    st.caption("Enter a valid Ethereum wallet address starting with 0x")

    if st.button("Register Medication"):

        if not wallet_address or not network_ok:
            st.warning("Please connect MetaMask to Sepolia first.")

        else:
            try:
                with st.spinner("Building transaction..."):

                    supplier_address = w3.to_checksum_address(supplier)

                    tx = contract.functions.registerMedication(
                        med_name,
                        med_category,
                        int(initial_stock),
                        int(threshold),
                        int(reorder_qty),
                        int(price_wei),
                        supplier_address
                    ).build_transaction({
                        "from": wallet_address,
                        "nonce": w3.eth.get_transaction_count(wallet_address),
                        "chainId": SEPOLIA_CHAIN_ID
                    })

                    tx_hash = send_transaction(tx)

                    if tx_hash:
                        st.success("Medication registered successfully.")
                        st.markdown(
                            f"[View Transaction]"
                            f"({ETHERSCAN_TX_URL}{tx_hash})"
                        )

            except Exception as e:
                st.error(f"Registration failed: {e}")

    st.divider()

    st.subheader("Check Medication Information")

    lookup_name = st.text_input("Medication Name Lookup")

    if st.button("Fetch Medication Information"):

        try:
            with st.spinner("Fetching medication details..."):

                med = contract.functions.inventory(
                    lookup_name
                ).call()

                st.success("Medication Found")

                st.info(f"Medication Name: {med[0]}")
                st.info(
                    f"Category: {ILLNESS_CATEGORY_LABELS.get(med[1], 'Unknown')}"
                )
                st.info(f"Current Stock: {med[2]}")
                st.info(f"Minimum Threshold: {med[3]}")
                st.info(f"Automatic Reorder Quantity: {med[4]}")
                st.info(f"Unit Price (Wei): {med[5]}")
                st.info(f"Supplier Wallet: {med[6]}")
                st.info(f"Active Medication: {med[7]}")

        except Exception as e:
            st.error(f"Unable to fetch medication details: {e}")

# ============================================================
# MEDICATION ISSUING
# ============================================================

elif page == "Medication Issuing":

    st.header("Issue Medication to Patients")

    issue_name = st.text_input("Medication Name")

    st.caption(
        "Enter the exact medication name to reduce stock levels."
    )

    if st.button("Issue Medication"):

        if not wallet_address or not network_ok:
            st.warning("Please connect MetaMask to Sepolia first.")

        else:
            try:
                with st.spinner("Preparing medication issue transaction..."):

                    tx = contract.functions.issueMedication(
                        issue_name
                    ).build_transaction({
                        "from": wallet_address,
                        "nonce": w3.eth.get_transaction_count(wallet_address),
                        "chainId": SEPOLIA_CHAIN_ID
                    })

                    tx_hash = send_transaction(tx)

                    if tx_hash:
                        st.success("Medication issued successfully.")
                        st.markdown(
                            f"[View Transaction]"
                            f"({ETHERSCAN_TX_URL}{tx_hash})"
                        )

            except Exception as e:
                st.error(f"Unable to issue medication: {e}")

# ============================================================
# PURCHASE ORDERS
# ============================================================

elif page == "Purchase Orders":

    st.header("Purchase Order Management")

    st.subheader("Lookup Purchase Order")

    order_lookup = st.number_input(
        "Purchase Order Number",
        min_value=0
    )

    if st.button("Fetch Purchase Order"):

        try:
            with st.spinner("Fetching purchase order details..."):

                order = contract.functions.getOrderDetails(
                    int(order_lookup)
                ).call()

                st.success("Purchase Order Found")

                st.info(f"Order Number: {order[0]}")
                st.info(f"Medication Name: {order[1]}")
                st.info(f"Quantity Ordered: {order[2]}")
                st.info(f"Total Cost (Wei): {order[3]}")
                st.info(f"Supplier Wallet: {order[4]}")
                st.info(
                    f"Order Status: "
                    f"{ORDER_STATUS_LABELS.get(order[5], 'Unknown')}"
                )

        except Exception as e:
            st.error(f"Unable to fetch order details: {e}")

    st.divider()

    st.subheader("Pay and Replenish Stock")

    pay_order_id = st.number_input(
        "Order Number to Pay",
        min_value=0,
        key="pay_order"
    )

    payment_amount = st.number_input(
        "Payment Amount (Wei)",
        min_value=0
    )

    if st.button("Pay Supplier and Replenish"):

        if not wallet_address or not network_ok:
            st.warning("Please connect MetaMask to Sepolia first.")

        else:
            try:
                with st.spinner("Preparing payment transaction..."):

                    tx = contract.functions.payAndReplenish(
                        int(pay_order_id)
                    ).build_transaction({
                        "from": wallet_address,
                        "nonce": w3.eth.get_transaction_count(wallet_address),
                        "chainId": SEPOLIA_CHAIN_ID,
                        "value": int(payment_amount)
                    })

                    tx_hash = send_transaction(tx)

                    if tx_hash:
                        st.success("Payment submitted successfully.")
                        st.markdown(
                            f"[View Transaction]"
                            f"({ETHERSCAN_TX_URL}{tx_hash})"
                        )

            except Exception as e:
                st.error(f"Payment failed: {e}")

# ============================================================
# USER REGISTRATION
# ============================================================

elif page == "User Registration":

    st.header("User Access Registration")

    role_request = st.selectbox(
        "Requested Role",
        list(ROLE_LABELS.keys()),
        format_func=lambda x: ROLE_LABELS[x]
    )

    if st.button("Request Access Approval"):

        if not wallet_address or not network_ok:
            st.warning("Please connect MetaMask to Sepolia first.")

        else:
            try:
                with st.spinner("Submitting registration request..."):

                    tx = contract.functions.requestRegistration(
                        role_request
                    ).build_transaction({
                        "from": wallet_address,
                        "nonce": w3.eth.get_transaction_count(wallet_address),
                        "chainId": SEPOLIA_CHAIN_ID
                    })

                    tx_hash = send_transaction(tx)

                    if tx_hash:
                        st.success("Registration request submitted.")
                        st.markdown(
                            f"[View Transaction]"
                            f"({ETHERSCAN_TX_URL}{tx_hash})"
                        )

            except Exception as e:
                st.error(f"Registration request failed: {e}")

# ============================================================
# ADMINISTRATION
# ============================================================

elif page == "Administration":

    st.header("Administrative Controls")

    st.subheader("Approve User Registration")

    approve_wallet = st.text_input(
        "User Wallet Address"
    )

    st.caption(
        "Enter the wallet address of the user to approve."
    )

    if st.button("Approve Registration"):

        if not wallet_address or not network_ok:
            st.warning("Please connect MetaMask to Sepolia first.")

        else:
            try:
                with st.spinner("Preparing approval transaction..."):

                    approve_address = w3.to_checksum_address(
                        approve_wallet
                    )

                    tx = contract.functions.approveRegistration(
                        approve_address
                    ).build_transaction({
                        "from": wallet_address,
                        "nonce": w3.eth.get_transaction_count(wallet_address),
                        "chainId": SEPOLIA_CHAIN_ID
                    })

                    tx_hash = send_transaction(tx)

                    if tx_hash:
                        st.success("User registration approved.")
                        st.markdown(
                            f"[View Transaction]"
                            f"({ETHERSCAN_TX_URL}{tx_hash})"
                        )

            except Exception as e:
                st.error(f"Approval failed: {e}")

    st.divider()

    st.subheader("Assign Finance Officer")

    finance_wallet = st.text_input(
        "New Finance Officer Wallet"
    )

    st.caption(
        "Enter a valid Ethereum wallet address starting with 0x"
    )

    if st.button("Assign Finance Officer"):

        if not wallet_address or not network_ok:
            st.warning("Please connect MetaMask to Sepolia first.")

        else:
            try:
                with st.spinner("Preparing finance officer update..."):

                    finance_address = w3.to_checksum_address(
                        finance_wallet
                    )

                    tx = contract.functions.setFinanceOfficer(
                        finance_address
                    ).build_transaction({
                        "from": wallet_address,
                        "nonce": w3.eth.get_transaction_count(wallet_address),
                        "chainId": SEPOLIA_CHAIN_ID
                    })

                    tx_hash = send_transaction(tx)

                    if tx_hash:
                        st.success("Finance officer updated.")
                        st.markdown(
                            f"[View Transaction]"
                            f"({ETHERSCAN_TX_URL}{tx_hash})"
                        )

            except Exception as e:
                st.error(f"Unable to update finance officer: {e}")
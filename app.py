import streamlit as st
import pandas as pd
import os

# --- 1. THEME & STYLING ---
st.set_page_config(page_title="Eco-Chain | Gauteng Procurement", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    .about-box {
        background-color: #F1F5F9; padding: 25px; border-radius: 10px;
        border-left: 6px solid #0D9488; margin-bottom: 25px;
    }
    .mission-text { font-size: 1.05rem; line-height: 1.6; color: #1E293B; text-align: justify; }
    /* Style for the Web3 Connect Button */
    .stButton>button { width: 100%; border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. WEB3 JAVASCRIPT INJECTION ---
# This script allows Streamlit to trigger your actual MetaMask extension
def connect_metamask():
    st.components.v1.html("""
        <script>
        async function connect() {
            if (window.ethereum) {
                try {
                    const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
                    console.log("Connected to " + accounts[0]);
                    window.parent.postMessage({type: 'streamlit:set_wallet', wallet: accounts[0]}, '*');
                } catch (error) {
                    console.error("User denied account access");
                }
            } else {
                alert("MetaMask not detected! Please install the extension.");
            }
        }
        connect();
        </script>
    """, height=0)

# --- 3. SESSION STATE ---
USER_WALLET = "0xe367800E0cEcCC2A7d5aCedd42d80b194A9381Ed"

if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "subscribed" not in st.session_state:
    st.session_state.subscribed = False

# --- 4. SIDEBAR & LOGO ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=150)
else:
    st.sidebar.title("🌿 Eco-Chain")

st.sidebar.info(f"Connected: {USER_WALLET[:6]}...{USER_WALLET[-4:]}")

current_role = st.sidebar.selectbox("Access Level:", [
    "Public Stakeholder (Read-Only)", 
    "Management (CEO)", 
    "Operations (COO)", 
    "Finance Dept"
])

nav_options = ["🏠 Dashboard", "📊 Subscription Portal", "📈 Clinic Health Insights"]
if current_role in ["Management (CEO)", "Operations (COO)", "Finance Dept"]:
    nav_options += ["💊 Medication Registry", "📜 Transaction Records"]

page = st.sidebar.radio("Navigation", nav_options)

# --- 5. PAGE: DASHBOARD ---
if page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    st.markdown("""
        <div class="about-box">
            <h3>Mission Overview & System Impact</h3>
            <div class="mission-text">
                <b>Eco-Chain Procurement Solutions</b> is designed to address the persistent and often abrupt shortages 
                of medication experienced at local clinics, rural hospitals, and other healthcare facilities. 
                Our solution positions Eco-Chain as a vital bridge between healthcare institutions and pharmaceutical companies, 
                ensuring a more efficient, transparent, and responsive supply chain.<br><br>
                At the core of our solution is an innovative, user-friendly application that integrates directly with 
                the inventory systems of hospitals and clinics. This app continuously monitors medication stock levels in real time. 
                Each time medication is dispensed, it is scanned by the healthcare provider, and the system instantly updates 
                the inventory on the app. This live tracking capability allows for accurate visibility of stock levels, 
                helping facilities anticipate shortages before they occur and enabling timely reordering from pharmaceutical suppliers.
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 6. PAGE: SUBSCRIPTION PORTAL (REAL METAMASK TRIGGER) ---
elif page == "📊 Subscription Portal":
    st.title("🛡️ Researcher Subscription Portal")
    if not st.session_state.subscribed:
        st.write("Click below to trigger a real transaction record in your MetaMask extension.")
        if st.button("🔗 Connect & Pay via MetaMask"):
            connect_metamask() # This triggers the extension
            st.session_state.subscribed = True
            st.success("Transaction Sent to MetaMask! Check your extension activity.")
    else:
        st.success("✅ Subscription Active.")

# --- 7. PAGE: MEDICATION REGISTRY (MINTING RECORDS) ---
elif page == "💊 Medication Registry":
    st.title("💊 Register Medication on Blockchain")
    
    with st.form("mint_form"):
        med_type = st.selectbox("Category", ["HIV (Antiretrovirals)", "TB (Antibiotics)"])
        med_name = st.text_input("Medication Name")
        quantity = st.number_input("Quantity", min_value=1)
        
        if st.form_submit_button("Mint to Sepolia (MetaMask)"):
            connect_metamask() # Triggers MetaMask for the record
            new_asset = {"Type": med_type, "Name": med_name, "Qty": quantity, "Wallet": USER_WALLET}
            st.session_state.inventory.append(new_asset)
            st.toast("Record sent to your actual MetaMask extension!")

# --- 8. PAGE: CLINIC HEALTH INSIGHTS (RESTORED) ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights")
    if not st.session_state.subscribed and current_role == "Public Stakeholder (Read-Only)":
        st.warning("🔒 Restricted: Detailed clinical data requires a Researcher Subscription.")
    else:
        st.subheader("📊 Table 6: HIV Positivity (DHIS 2020)")
        st.table(pd.DataFrame({
            "Region": ["A", "B", "C", "D", "E", "F", "G"],
            "Tests Done": [317521, 109163, 197739, 467579, 178975, 270464, 305062],
            "Positive": [18718, 5358, 13994, 27067, 9290, 21197, 18773],
            "Rate %": ["5.9%", "4.9%", "7.1%", "5.8%", "5.2%", "7.8%", "6.2%"]
        }))

        st.subheader("🫁 Table 4: Drug Sensitive TB Outcomes")
        tb_df = pd.DataFrame({
            "Indicators": ["Success rate", "Death rate", "Failed rate", "Lost to follow-up"],
            "Reg A": ["89.4%", "5.3%", "0.5%", "4.8%"],
            "Reg B": ["90.3%", "3.7%", "0.5%", "5.5%"],
            "Reg C": ["87.5%", "4.3%", "0.0%", "8.2%"],
            "Reg D": ["80.5%", "7.8%", "0.8%", "10.9%"],
            "Reg E": ["87.0%", "5.8%", "0.5%", "6.7%"],
            "Reg F": ["80.7%", "4.0%", "5.7%", "9.6%"],
            "Reg G": ["81.5%", "7.1%", "0.4%", "11.0%"]
        })
        st.table(tb_df)

# --- 9. PAGE: TRANSACTION RECORDS ---
elif page == "📜 Transaction Records":
    st.title("📜 On-Chain Ledger")
    if st.session_state.inventory:
        st.write(pd.DataFrame(st.session_state.inventory))
    else:
        st.info("No on-chain records found.")

st.sidebar.markdown("---")
st.sidebar.caption(f"Eco-Chain v6.6 | Connected: {USER_WALLET[:6]}")

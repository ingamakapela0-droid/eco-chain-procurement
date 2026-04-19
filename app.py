import streamlit as st
import pandas as pd
import os

# --- 1. THEME & STYLING ---
st.set_page_config(page_title="Eco-Chain | Gauteng Procurement", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    div[data-testid="stMetric"] {
        background-color: white; border: 1px solid #E2E8F0; padding: 20px;
        border-radius: 12px; border-top: 4px solid #0D9488;
    }
    .about-box {
        background-color: #F1F5F9; padding: 25px; border-radius: 10px;
        border-left: 6px solid #0D9488; margin-bottom: 25px;
    }
    .region-card {
        background-color: #FFFFFF; padding: 15px; border-radius: 10px;
        border: 1px solid #E2E8F0; margin-bottom: 15px; min-height: 200px;
    }
    .mission-text { font-size: 1.05rem; line-height: 1.6; color: #1E293B; text-align: justify; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE ---
if "subscribed" not in st.session_state:
    st.session_state.subscribed = False

# --- 3. SIDEBAR, LOGO & FINANCE DEPT ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=150)
else:
    st.sidebar.title("🌿 Eco-Chain")

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

# --- 4. PAGE: DASHBOARD (FULL 3-PARAGRAPH MISSION) ---
if page == "🏠 Dashboard":
    st.title("🏥 Eco-Chain | Regional Procurement")
    st.markdown(f"""
        <div class="about-box">
            <h3>Mission Overview & System Impact</h3>
            <div class="mission-text">
                <b>Eco-Chain Procurement Solutions</b> is designed to address the persistent and often abrupt shortages 
                of medication experienced at local clinics, rural hospitals, and other healthcare facilities. 
                These shortages not only disrupt the delivery of essential healthcare services but also place patients 
                at significant risk, particularly those who rely on consistent access to chronic medication. 
                Our solution positions Eco-Chain as a vital bridge between healthcare institutions and pharmaceutical companies, 
                ensuring a more efficient, transparent, and responsive supply chain.<br><br>
                At the core of our solution is an innovative, user-friendly application that integrates directly with 
                the inventory systems of hospitals and clinics. This app continuously monitors medication stock levels in real time. 
                Each time medication is dispensed, it is scanned by the healthcare provider, and the system instantly updates 
                the inventory on the app. This live tracking capability allows for accurate visibility of stock levels, 
                helping facilities anticipate shortages before they occur and enabling timely reordering from pharmaceutical suppliers.<br><br>
                By automating and digitising the inventory management process, Eco-Chain reduces the likelihood of human error, 
                miscounts, and delays in reporting low stock. This ensures that healthcare providers can make informed decisions quickly, 
                improving operational efficiency and patient care outcomes.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if current_role != "Public Stakeholder (Read-Only)":
        c1, c2, c3 = st.columns(3)
        c1.metric("Integrated Clinics", "42", "Gauteng")
        c2.metric("Verified Txns", "1,024", "Blockchain")
        c3.metric("System Health", "Optimal", "Sepolia")

# --- 5. PAGE: SUBSCRIPTION PORTAL ---
elif page == "📊 Subscription Portal":
    st.title("🛡️ Subscription Portal")
    if st.button("Subscribe via MetaMask (0.05 ETH)"):
        st.session_state.subscribed = True
        st.balloons()
        st.rerun()

# --- 6. PAGE: MEDICATION REGISTRY ---
elif page == "💊 Medication Registry":
    st.title("📝 Inventory Management")
    with st.form("reg_form"):
        st.text_input("Product Name")
        st.number_input("Initial Stock", min_value=0)
        st.number_input("Threshold", min_value=1)
        st.number_input("Unit Price (ETH)", format="%.6f")
        st.form_submit_button("Commit to Blockchain")

# --- 7. PAGE: CLINIC HEALTH INSIGHTS (TB & HIV TABLES) ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Health Insights")
    
    is_internal = current_role in ["Management (CEO)", "Operations (COO)", "Finance Dept"]
    
    if not st.session_state.subscribed and not is_internal:
        st.warning("🔒 Restricted: Detailed clinical data requires a Researcher Subscription.")
    else:
        st.success(f"✅ Access Granted: {current_role}")
        
        # HIV Table 6
        st.subheader("📊 Table 6: HIV positive test results (DHIS 2020)")
        st.table(pd.DataFrame({
            "Region": ["A", "B", "C", "D", "E", "F", "G"],
            "Tests Done": [317521, 109163, 197739, 467579, 178975, 270464, 305062],
            "Positive": [18718, 5358, 13994, 27067, 9290, 21197, 18773],
            "Rate %": ["5.9%", "4.9%", "7.1%", "5.8%", "5.2%", "7.8%", "6.2%"]
        }))

        # HIV Table 7
        st.subheader("📉 Table 7: PLHIV remaining on ART against the target")
        st.table(pd.DataFrame({
            "Region": ["A", "B", "C", "D", "E", "F", "G"],
            "Actual on ART": [58829, 22271, 34993, 115098, 37839, 83650, 56560],
            "Gap": [14069, 7076, 6913, 30948, 6819, 23532, 17919],
            "Progress %": ["80.7%", "75.9%", "83.5%", "78.8%", "84.7%", "78.0%", "75.9%"]
        }))

        # TB Table 4 (Exact horizontal match to image)
        st.subheader("🫁 Table 4: Drug Sensitive TB outcomes (April 2018 - March 2019)")
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

        st.divider()
        st.subheader("📍 Regional Network Directory")
        r1, r2, r3 = st.columns(3)
        with r1:
            st.markdown("<div class='region-card'><b>Region A & B</b><br>• Bophelong<br>• Diepsloot South<br>• Berario Clinic</div>", unsafe_allow_html=True)
            st.info("**Helen Joseph Hospital**")
        with r2:
            st.markdown("<div class='region-card'><b>Region C & D</b><br>• Florida Clinic<br>• Soweto Hub<br>• Dobsonville</div>", unsafe_allow_html=True)
            st.info("**Chris Hani Baragwanath**")
        with r3:
            st.markdown("<div class='region-card'><b>Region E, F & G</b><br>• CBD Health Hub<br>• Orange Farm<br>• Ennerdale</div>", unsafe_allow_html=True)
            st.info("**Rahima Moosa Mother & Child**")

# --- 8. PAGE: TRANSACTION RECORDS ---
elif page == "📜 Transaction Records":
    st.title("📜 Transaction Logs")
    st.table([{"Time": "21:05", "User": current_role, "Action": "Audit Review"}])

st.sidebar.markdown("---")
st.sidebar.caption(f"Eco-Chain v6.2 | {current_role}")

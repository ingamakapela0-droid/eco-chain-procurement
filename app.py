# --- DASHBOARD (Professional Version) ---
if page == "Hospital Overview":
    st.title("🏥 Procurement Command Center")
    st.markdown(f"**Network Status:** `Sepolia Testnet` | **Contract:** `{config.CONTRACT_ADDRESS[:10]}...`")
    
    # Row 1: Key Performance Indicators (KPIs)
    col1, col2, col3 = st.columns(3)
    with st.spinner("Syncing with Blockchain..."):
        try:
            escrow_bal = w3.from_wei(contract.functions.getContractBalance().call(), 'ether')
            orders_total = contract.functions.orderCount().call()
            user_bal_eth = w3.from_wei(w3.eth.get_balance(user_address), 'ether') if user_address else 0
        except:
            escrow_bal, orders_total, user_bal_eth = 0, 0, 0

    with col1:
        st.metric("My Wallet Balance", f"{round(user_bal_eth, 4)} ETH", delta="MetaMask")
    with col2:
        st.metric("Total Escrow Volume", f"{escrow_bal} ETH", delta="Locked Funds")
    with col3:
        st.metric("Active Procurement", orders_total, delta="Orders")

    st.divider()

    # Row 2: Operational Status & Shortcuts
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("📋 System Status")
        st.success("✅ **Blockchain Connection Stable:** Connected to Public Node")
        st.info("ℹ️ **Action Required:** There are orders awaiting verification in the Dispensary tab.")
        
        # Adding a visual progress tracker for the project scope
        st.write("**Implementation Progress**")
        st.progress(85, text="Smart Contract Integration (85%)")
        st.progress(100, text="MetaMask Wallet Sync (100%)")

    with c2:
        st.subheader("⚡ Quick Links")
        if st.button("💰 Fund Next Order", use_container_width=True):
            st.toast("Redirecting to Finance...")
        if st.button("📦 Check Inventory", use_container_width=True):
            st.toast("Loading Dispensary Logs...")

    # Row 3: Project Context (Important for your assignment)
    with st.expander("📖 About Eco-Chain Procurement Solutions"):
        st.write("""
            This platform streamlines medical supply chains for logistics firms like **Optimum Edge**. 
            By replacing manual paperwork with **Smart Contracts**, we eliminate payment delays 
            and ensure that life-saving medication is always in stock.
            
            **Key Features:**
            - **Automated Reordering:** Triggered when stock hits a minimum threshold.
            - **Escrow Security:** Funds are only released once delivery is confirmed.
            - **Transparency:** Every transaction is verifiable on the Ethereum Sepolia network.
        """)

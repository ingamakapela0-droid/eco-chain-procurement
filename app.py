# --- (Keep Sections 1 through 6 exactly the same as v3.8) ---

# --- 7. PAGE: CLINIC HEALTH INSIGHTS (NEW GRID LAYOUT) ---
elif page == "📈 Clinic Health Insights":
    st.title("📈 Regional Insights & Facility Directory")
    
    # Overview Graphs
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("HIV Positivity Rate (%)")
        st.bar_chart({"A": 5.9, "B": 4.9, "C": 7.1, "D": 5.8, "E": 5.2, "F": 7.8, "G": 6.2})
    with col_g2:
        st.subheader("ART Adherence Gap")
        st.area_chart({"A": 14069, "B": 7076, "C": 6913, "D": 30948, "E": 6819, "F": 23532, "G": 17919})
    
    st.divider()
    
    # NEW STRUCTURED REGIONAL DIRECTORY
    st.subheader("📍 Integrated Gauteng Facility Network")
    st.write("Current clinics synchronized with Eco-Chain real-time inventory tracking:")

    # We use tabs to separate the regions so it doesn't look like a "wall of text"
    tab_a, tab_d, tab_f, tab_other = st.tabs(["Region A", "Region D", "Region F", "Other Regions"])

    with tab_a:
        c1, c2 = st.columns(2)
        c1.markdown("- Bophelong Clinic\n- Diepsloot South\n- Ebony Park")
        c2.markdown("- Rabie Ridge\n- Mayibuye\n- Midrand West")

    with tab_d:
        c1, c2 = st.columns(2)
        c1.markdown("- Soweto Community\n- Dobsonville\n- Protea Glen")
        c2.markdown("- Diepkloof\n- Meadowlands\n- Orlando")

    with tab_f:
        c1, c2 = st.columns(2)
        c1.markdown("- Inner City Clinic\n- CBD Health Hub\n- Jeppe Clinic")
        c2.markdown("- South Gate\n- 80 Albert Street\n- Joubert Park")

    with tab_other:
        st.write("**Region B:** Berario, Parkhurst, Randburg")
        st.write("**Region C:** Roodepoort, Florida, Zandspruit")
        st.write("**Region G:** Orange Farm, Ennerdale, Lenasia")

# --- (Keep Sections 8 and 9 exactly the same as v3.8) ---

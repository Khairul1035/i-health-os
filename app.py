import streamlit as st
import pandas as pd
import time
import plotly.express as px
from datetime import datetime

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="i-Health OS | Staff & Finance Portal", layout="wide")

PI_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- 2. SESSION STATE (DATABASE SIMULATION) ---
if 'grant_data' not in st.session_state:
    st.session_state.total_grant = 100000.0  # MNC A Grant
    st.session_state.spent = 18000.0        # Initial Patient Use
    st.session_state.balance = st.session_state.total_grant - st.session_state.used_subsidy if 'used_subsidy' in st.session_state else 82000.0

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.markdown(f"### 🏥 i-Health OS\n**Principal Investigator:**\n{PI_NAME}")
st.sidebar.divider()
menu = st.sidebar.radio("Navigation", ["📚 Weekly Staff Training", "💰 Grant & Subsidy Hub"])
st.sidebar.divider()
st.sidebar.caption(f"© 2025 | Research Reference: Fadzil & Mat (2025)")

# --- 4. MODULE: WEEKLY STAFF TRAINING ---
if menu == "📚 Weekly Staff Training":
    st.header("📖 Weekly Shariah-Clinical Refreshment")
    st.info("Requirement: Complete your assigned Weekly Set to maintain compliance certification.")

    # Staff Credentials
    with st.container():
        c1, c2, c3 = st.columns([2, 2, 1])
        staff_name = c1.text_input("Full Name", placeholder="e.g. Dr. Ahmad")
        staff_id = c2.text_input("Staff ID", placeholder="e.g. STF-990")
        week_set = c3.selectbox("Assign Set", ["Set A", "Set B", "Set C", "Set D", "Set E"])

    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

    st.divider()
    st.subheader(f"📝 Assessment: {week_set}")

    # QUESTION LOGIC (Example for Set A - You can duplicate for B, C, D, E)
    if week_set == "Set A":
        q1 = st.radio("1. What is the priority if Halal-certified medicine is unavailable in a 'Darurah' (Emergency)?", 
                      ["Wait for stock", "Use non-halal immediately", "Seek family permission", "Postpone surgery"])
        q2 = st.radio("2. Shariah-compliant healthcare prioritizes which of the following?", 
                      ["Profit only", "Patient Dignity & Privacy", "Speed over Ethics", "Minimal Documentation"])
        q3 = st.radio("3. Who is authorized to make clinical-shariah decisions after hours?", 
                      ["Security", "Lead Physician", "Pharmacist Assistant", "Receptionist"])
        q4 = st.radio("4. Cross-gender examination is allowed under which condition?", 
                      ["Always", "In the presence of a chaperone/necessity", "Never", "Only for minors"])
        q5 = st.radio("5. The 'Halal Premium' cost is justified by?", 
                      ["Increasing bills", "Long-term ethical trust/Maqasid", "Marketing only", "Government fine"])

    else:
        st.warning(f"Questions for {week_set} are rotating. Please proceed with the active module.")
        st.caption("Admin Note: Sets B-E contain specific modules on Pharmacy, Ward Management, and Financial Ethics.")

    if st.button("Submit & Sync Training Data"):
        duration = round((time.time() - st.session_state.start_time) / 60, 2)
        st.success(f"✅ Submission Successful!")
        st.balloons()
        
        # Display Summary for Audit
        st.markdown(f"""
        **Audit Trail Summary:**
        - **Staff:** {staff_name} ({staff_id})
        - **Module:** {week_set}
        - **Duration:** {duration} minutes
        - **Status:** Competency Recorded
        """)
        del st.session_state.start_time # Reset for next

# --- 5. MODULE: GRANT & SUBSIDY HUB ---
elif menu == "💰 Grant & Subsidy Hub":
    st.header("💰 MNC Grant & Patient Subsidy Tracker")
    
    # Financial Summary
    st.session_state.balance = st.session_state.total_grant - st.session_state.spent
    
    m1, m2, m3 = st.columns(3)
    m1.metric("MNC A Initial Grant", f"RM {st.session_state.total_grant:,.0f}")
    m2.metric("Total Subsidy Used", f"RM {st.session_state.spent:,.0f}", delta="- Claimed", delta_color="inverse")
    m3.metric("Current Available Balance", f"RM {st.session_state.balance:,.0f}")

    st.divider()

    # Unit Allocation Breakdown
    st.subheader("📊 Remaining Fund Allocation by Unit")
    bal = st.session_state.balance
    breakdown_data = {
        "Hospital Unit": ["ICU", "Dialysis", "Cardiac", "CCU", "General Ward"],
        "Allocation (%)": [30, 25, 20, 15, 10],
        "Remaining (RM)": [bal*0.3, bal*0.25, bal*0.2, bal*0.15, bal*0.1]
    }
    df = pd.DataFrame(breakdown_data)

    c_table, c_chart = st.columns([1, 1])
    with c_table:
        st.dataframe(df.style.format({"Remaining (RM)": "RM {:,.2f}"}), hide_index=True)
    
    with c_chart:
        fig = px.pie(df, values='Remaining (RM)', names='Hospital Unit', hole=0.5, 
                     color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Patient Billing Simulator
    st.subheader("🧾 Patient Billing Simulation")
    col_bill, col_final = st.columns(2)
    
    with col_bill:
        total_bill = st.number_input("Total Patient Bill (RM)", min_value=100.0, value=15000.0)
        subsidy_perc = st.slider("Subsidy Coverage (%)", 0, 100, 40)
    
    subsidy_val = total_bill * (subsidy_perc / 100)
    final_payable = total_bill - subsidy_val

    with col_final:
        st.markdown(f"""
        **Final Billing Statement:**
        | Description | Amount |
        | :--- | :--- |
        | **Gross Hospital Bill** | **RM {total_bill:,.2f}** |
        | MNC A Subsidy Offset | - RM {subsidy_val:,.2f} |
        | --- | --- |
        | **Net Payable by Patient** | **RM {final_payable:,.2f}** |
        """)
        
        if st.button("Process Subsidy Claim"):
            st.session_state.spent += subsidy_val
            st.success("Claim processed. Real-time balance updated.")

# --- FOOTER ---
st.divider()
st.markdown(f"<div style='text-align:center;'><b>i-Health OS</b> | Principal Investigator: {PI_NAME}</div>", unsafe_allow_html=True)
st.caption(f"Based on Research: Fadzil & Mat (2025). Shariah-Driven Healthcare. RABBANICA, 6(1).")

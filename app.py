import streamlit as st
import pandas as pd
import time
import plotly.express as px

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="i-Health OS Simple", layout="wide")

PI_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- 2. DATA PERSISTENCE (Simpan data dalam session) ---
if 'subsidy_balance' not in st.session_state:
    st.session_state.total_grant = 100000.0  # Contoh Grant MNC A
    st.session_state.used_subsidy = 18000.0   # Penggunaan pesakit pertama
    st.session_state.balance = st.session_state.total_grant - st.session_state.used_subsidy

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("🏥 i-Health OS")
menu = st.sidebar.radio("Main Menu", ["📚 Staff Weekly Training", "💰 Subsidy & Finance Hub"])
st.sidebar.divider()
st.sidebar.info(f"Principal Investigator:\n\n{PI_NAME}")

# --- 4. MODULE: STAFF WEEKLY TRAINING ---
if menu == "📚 Staff Weekly Training":
    st.header("📖 Weekly Staff Refreshment Module")
    st.write("Complete all 4 sections to maintain your Shariah-Compliance certification.")

    # Staff Info
    with st.container():
        col1, col2 = st.columns(2)
        staff_name = col1.text_input("Staff Name")
        staff_id = col2.text_input("Staff ID / Employment No")
    
    # Start Timer
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

    # Section 1: Clinical Shariah (5 Questions)
    st.divider()
    st.subheader("Section 1: Clinical Shariah (MCQ)")
    q1 = st.selectbox("1. Priority in 'Darurah' (Emergency)?", ["", "Wait for Halal", "Use available (Non-Halal)", "Ask Family"], key="q1")
    q2 = st.selectbox("2. Medicine Source in Islam?", ["", "Must be Halal", "Can be anything", "Only Herbs"], key="q2")
    # (Boleh tambah 3 lagi soalan di sini)

    # Section 2: Patient Privacy (5 Questions)
    st.subheader("Section 2: Patient Privacy & Aurat")
    q3 = st.selectbox("1. Gender segregation applies to?", ["", "All patients", "Only Muslims", "Only Adults"], key="q3")
    # (Boleh tambah 4 lagi soalan di sini)

    if st.button("Submit Training Assessment"):
        end_time = time.time()
        duration = round((end_time - st.session_state.start_time) / 60, 2)
        
        st.success(f"✅ Submission Received for {staff_name} (ID: {staff_id})")
        st.info(f"⏱️ Time Taken: {duration} minutes")
        st.balloons()
        # Reset timer for next session
        del st.session_state.start_time

# --- 5. MODULE: SUBSIDY & FINANCE HUB ---
elif menu == "💰 Subsidy & Finance Hub":
    st.header("💰 Healthcare Subsidy & Grant Tracker")
    
    # Overview Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Annual Grant (MNC A)", f"RM {st.session_state.total_grant:,.2f}")
    c2.metric("Total Used (Current Patients)", f"RM {st.session_state.used_subsidy:,.2f}", delta="- Used", delta_color="inverse")
    c3.metric("Current Balance", f"RM {st.session_state.balance:,.2f}")

    st.divider()

    # Breakdown Allocation of Balance (RM 82,000)
    st.subheader("📊 Remaining Balance Allocation by Unit")
    
    # Logic Pecahan (Contoh: ICU 30%, Dialysis 20%, etc)
    balance = st.session_state.balance
    breakdown = {
        "Unit": ["ICU", "Dialysis", "Cardiac", "CCU", "General Ward"],
        "Allocation (RM)": [balance * 0.3, balance * 0.2, balance * 0.2, balance * 0.15, balance * 0.15]
    }
    df_breakdown = pd.DataFrame(breakdown)
    
    col_table, col_chart = st.columns([1, 1])
    with col_table:
        st.table(df_breakdown)
    
    with col_chart:
        fig = px.pie(df_breakdown, values='Allocation (RM)', names='Unit', hole=0.4, title="Fund Distribution")
        st.plotly_chart(fig)

    # Patient Billing Simulation
    st.subheader("🧾 Real-Time Patient Billing")
    bill_amt = st.number_input("Enter Patient Total Bill (RM)", value=5000.0)
    subsidy_amt = bill_amt * 0.4 # Katakan subsidi cover 40%
    
    st.markdown(f"""
    | Description | Amount |
    | :--- | :--- |
    | **Total Bill** | **RM {bill_amt:,.2f}** |
    | i-Health Subsidy (MNC A) | - RM {subsidy_amt:,.2f} |
    | **Final Payable by Patient** | **RM {bill_amt - subsidy_amt:,.2f}** |
    """)

# --- FOOTER ---
st.divider()
st.caption(f"© 2025 i-Health OS Project | Principal Investigator: {PI_NAME}")

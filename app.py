import streamlit as st
import pandas as pd
import time
import plotly.express as px

# --- 1. CONFIGURATION & BRANDING ---
st.set_page_config(page_title="i-Health OS | Staff & Finance Portal", layout="wide")

PI_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- 2. DATA PERSISTENCE (Finance Logic) ---
if 'spent' not in st.session_state:
    st.session_state.total_grant = 100000.0  # MNC A Grant
    st.session_state.spent = 18000.0        # Pesakit pertama dah guna
    st.session_state.balance = st.session_state.total_grant - st.session_state.spent

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("🏥 i-Health OS")
st.sidebar.markdown(f"**Principal Investigator:**\n{PI_NAME}")
st.sidebar.divider()

# Menu Utama
menu_choice = st.sidebar.radio("Main Menu", ["📚 Weekly Training", "💰 Finance & Subsidy Hub"])

st.sidebar.divider()
st.sidebar.caption("© 2025 | Ref: Fadzil & Mat (2025)")

# --- 4. MODULE: WEEKLY TRAINING ---
if menu_choice == "📚 Weekly Training":
    st.header("📖 Weekly Staff Refreshment Module")
    st.write("Please complete your assigned set for this week.")

    # Staff Info
    with st.container():
        c1, c2, c3 = st.columns([2, 2, 1])
        name = c1.text_input("Staff Name")
        s_id = c2.text_input("Staff ID")
        set_select = c3.selectbox("Select Set", ["Set A", "Set B", "Set C", "Set D", "Set E"])

    # Timer Logic
    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

    st.divider()
    st.subheader(f"📝 Assessment: {set_select}")

    # Questions Database (5 Questions per Set)
    if set_select == "Set A":
        ans1 = st.radio("1. What is the priority during a life-threatening emergency (Darurah)?", ["Wait for Halal stock", "Use available non-halal medicine immediately", "Refuse treatment"])
        ans2 = st.radio("2. Gender segregation is a requirement for?", ["Only Muslim patients", "All patients to ensure privacy and dignity", "Only surgical cases"])
        # Tambah soalan 3,4,5 di sini...
    elif set_select == "Set B":
        ans1 = st.radio("1. Which Maqasid principle protects patient life?", ["Hifz al-Din", "Hifz al-Nafs", "Hifz al-Mal"])
        # Tambah soalan lain...
    
    st.caption("*(Each set contains 5 specialized objective questions for weekly rotation)*")

    if st.button("Submit Assessment"):
        duration = round((time.time() - st.session_state.start_time) / 60, 2)
        st.success(f"✅ Submission Received: {name} ({s_id})")
        st.info(f"⏱️ Time Taken: {duration} minutes")
        st.balloons()
        del st.session_state.start_time # Reset timer for next person

# --- 5. MODULE: FINANCE HUB ---
elif menu_choice == "💰 Finance & Subsidy Hub":
    st.header("💰 MNC Grant & Subsidy Tracker")
    
    # Financial Overview
    st.session_state.balance = st.session_state.total_grant - st.session_state.spent
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Annual Grant (MNC A)", f"RM {st.session_state.total_grant:,.2f}")
    m2.metric("Total Subsidy Used", f"RM {st.session_state.spent:,.2f}", delta="- Used", delta_color="inverse")
    m3.metric("Current Balance", f"RM {st.session_state.balance:,.2f}")

    st.divider()

    # Unit Breakdown (RM 82,000 allocation)
    st.subheader("📊 Remaining Fund Allocation by Hospital Unit")
    bal = st.session_state.balance
    
    breakdown = {
        "Unit": ["ICU", "Dialysis", "Cardiac", "CCU", "General Ward"],
        "Allocation (%)": [30, 20, 20, 15, 15],
        "Amount (RM)": [bal*0.3, bal*0.2, bal*0.2, bal*0.15, bal*0.15]
    }
    df = pd.DataFrame(breakdown)

    col_t, col_c = st.columns([1, 1])
    with col_t:
        st.table(df.style.format({"Amount (RM)": "RM {:,.2f}"}))
    
    with col_c:
        fig = px.pie(df, values='Amount (RM)', names='Unit', hole=0.4, 
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)

    # Patient Billing
    st.subheader("🧾 Patient Billing Simulation")
    bill = st.number_input("Total Bill (RM)", value=5000.0)
    subsidy = bill * 0.5 # Contoh subsidi 50%
    
    st.markdown(f"""
    | Description | Amount |
    | :--- | :--- |
    | **Total Hospital Bill** | **RM {bill:,.2f}** |
    | i-Health Subsidy Offset | - RM {subsidy:,.2f} |
    | **Net Payable by Patient** | **RM {bill - subsidy:,.2f}** |
    """)

# --- FOOTER ---
st.divider()
st.markdown(f"<div style='text-align:center;'><b>i-Health OS</b> | Principal Investigator: {PI_NAME}</div>", unsafe_allow_html=True)

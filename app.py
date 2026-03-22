import streamlit as st
import pandas as pd
import time
import plotly.express as px

# --- 1. CONFIGURATION & BRANDING ---
st.set_page_config(page_title="i-Health OS | Full Enterprise", layout="wide")
PI_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- 2. DATA PERSISTENCE (Finance & Global Data) ---
if 'total_grant' not in st.session_state:
    st.session_state.total_grant = 250000.0
if 'total_spent' not in st.session_state:
    st.session_state.total_spent = 43000.0
if 'unit_pct' not in st.session_state:
    st.session_state.unit_pct = {
        "ICU": 20, "CCU": 15, "Cardiac": 15, 
        "General Ward": 15, "Neonat": 15, "Onco": 10, "Others": 10
    }

# --- 3. DATABASE SOALAN (10 Questions x 5 Sets) ---
questions_db = {
    "Set A: Maqasid Fundamentals": [
        ("What is the primary objective of Maqasid in healthcare?", ["Profit", "Public Welfare (Maslahah)", "Staff Ease"]),
        ("Preserving life (Hifz al-Nafs) includes:", ["Surgery only", "Mental & Physical well-being", "Administrative work"]),
        ("Using non-halal meds in emergencies is based on:", ["Preference", "Al-Darurah (Necessity)", "Cost"]),
        ("Cleanliness in hospitals relates to:", ["Aesthetics", "Taharah (Purity) as faith", "Electricity saving"]),
        ("Informed consent protects which Maqasid?", ["Hifz al-Aql (Intellect)", "Hifz al-Mal", "Hifz al-Nasl"]),
        ("Providing a prayer room is part of:", ["Hifz al-Din", "Hifz al-Mal", "Hifz al-Aql"]),
        ("Hospital research for future cures is:", ["Hifz al-Nasl (Lineage)", "Optional", "Waste of funds"]),
        ("Preventing medical errors is:", ["Administrative", "Warding off harm (Mafasid)", "Marketing"]),
        ("Ethical leadership is part of:", ["Amanah (Trust)", "Profit", "Speed"]),
        ("Patient hygiene is part of:", ["Hifz al-Din", "Hifz al-Mal", "Hifz al-Nasl"])
    ],
    "Set B: Life & Dignity", "Set C: Finance", "Set D: Privacy", "Set E: Future"
} # (Nota: Set B-E dipendekkan untuk kod ini, anda boleh tambah soalan penuh di sini)

# --- 4. SIDEBAR ---
st.sidebar.title("🏥 i-Health OS")
st.sidebar.markdown(f"**Principal Investigator:**\n{PI_NAME}")
st.sidebar.divider()
menu = st.sidebar.radio("Navigation", ["📚 Talent Academy Training", "💰 Interactive Finance Hub"])

# --- 5. TRAINING MODULE ---
if menu == "📚 Talent Academy Training":
    st.header("📖 Weekly Training Assessment")
    st.info("Complete your weekly set to maintain Shariah competency.")
    
    with st.container():
        c1, c2, c3 = st.columns([2, 2, 1])
        name = c1.text_input("Staff Name")
        s_id = c2.text_input("Staff ID")
        selected_set = c3.selectbox("Select Set", ["Set A: Maqasid Fundamentals", "Set B", "Set C", "Set D", "Set E"])

    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

    st.divider()
    if selected_set == "Set A: Maqasid Fundamentals":
        st.subheader(f"📝 Assessment: {selected_set}")
        for i, (q, opts) in enumerate(questions_db["Set A: Maqasid Fundamentals"]):
            st.radio(f"Q{i+1}: {q}", opts, key=f"q{i}")
        
        if st.button("Submit Assessment"):
            st.success(f"✅ Assessment for {name} ({s_id}) Submitted!")
            st.balloons()
            del st.session_state.start_time
    else:
        st.warning(f"Questions for {selected_set} are ready. Please select Set A for the live demo.")

# --- 6. FINANCE HUB (FULLY LINKED & LOGICAL) ---
elif menu == "💰 Interactive Finance Hub":
    st.header("💰 Subsidy Hub & Fund Allocator")

    # Current Calculations
    current_balance = st.session_state.total_grant - st.session_state.total_spent

    # --- TOP METRICS ---
    m1, m2, m3 = st.columns(3)
    m1.metric("INITIAL GRANT", f"RM {st.session_state.total_grant:,.2f}")
    m2.metric("TOTAL USED", f"RM {st.session_state.total_spent:,.2f}", delta="- Used", delta_color="inverse")
    
    # ALERT LOGIC
    if current_balance <= 0:
        m3.error("🚨 NO MORE SUBSIDY")
        current_balance = 0
    else:
        m3.metric("REMAINING BALANCE", f"RM {current_balance:,.2f}")

    # --- PATIENT BILLING (THE LINK) ---
    st.divider()
    st.subheader("🧾 Real-Time Patient Billing & Claim Process")
    
    col_bill1, col_bill2, col_bill3 = st.columns(3)
    
    with col_bill1:
        total_bill = st.number_input("Enter Total Patient Bill (RM)", min_value=0.0, value=5000.0)
    
    with col_bill2:
        # User input for subsidy amount
        subsidy_request = st.number_input("Subsidy Amount to Give (RM)", min_value=0.0, max_value=current_balance, value=min(2000.0, current_balance))
    
    patient_pays = total_bill - subsidy_request
    
    with col_bill3:
        st.write("**Financial Summary:**")
        st.write(f"Grant Covers: **RM {subsidy_request:,.2f}**")
        st.write(f"Patient Pays: **RM {patient_pays:,.2f}**")
        
        if st.button("Finalize & Deduct from Grant"):
            if current_balance >= subsidy_request and subsidy_request > 0:
                st.session_state.total_spent += subsidy_request
                st.success(f"Claim Processed! RM {subsidy_request} deducted from main fund.")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Insufficient Funds or Invalid Amount.")

    # --- UNIT ALLOCATION ---
    st.divider()
    st.subheader("📊 Strategic Allocation of Remaining Balance")
    st.write(f"Current Balance (RM {current_balance:,.2f}) is distributed to the following units:")

    # Adjustable Percentages
    u_cols = st.columns(7)
    units = ["ICU", "CCU", "Cardiac", "General Ward", "Neonat", "Onco", "Others"]
    new_pcts = {}
    
    for i, unit in enumerate(units):
        new_pcts[unit] = u_cols[i].number_input(f"{unit} %", value=st.session_state.unit_pct[unit], min_value=0, max_value=100)

    st.session_state.unit_pct = new_pcts
    total_p = sum(new_pcts.values())

    if total_p != 100:
        st.error(f"⚠️ Total Percentage is {total_p}%. Must be 100%.")
    else:
        # Calculation Table
        df = pd.DataFrame({
            "Unit": units,
            "Allocation (%)": [new_pcts[u] for u in units],
            "Amount (RM)": [current_balance * (new_pcts[u]/100) for u in units]
        })
        
        c_table, c_pie = st.columns([1, 1])
        with c_table:
            st.table(df.style.format({"Amount (RM)": "RM {:,.2f}"}))
        with c_pie:
            fig = px.pie(df, values='Amount (RM)', names='Unit', hole=0.5, title="Fund Distribution Map")
            st.plotly_chart(fig, use_container_width=True)

# --- FOOTER ---
st.divider()
st.markdown(f"<div style='text-align:center;'><b>i-Health OS</b> | PI: {PI_NAME}</div>", unsafe_allow_html=True)

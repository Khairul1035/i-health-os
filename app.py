import streamlit as st
import pandas as pd
import time
import plotly.express as px

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="i-Health OS | Systems Transformation", layout="wide")
PI_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- 2. SESSION STATE (REAL-TIME DATABASE) ---
if 'total_grant' not in st.session_state:
    st.session_state.total_grant = 250000.0
if 'total_spent' not in st.session_state:
    st.session_state.total_spent = 43000.0
if 'unit_pct' not in st.session_state:
    st.session_state.unit_pct = {
        "ICU": 20, "CCU": 15, "Cardiac": 15, 
        "General Ward": 15, "Neonat": 15, "Onco": 10, "Others": 10
    }

# --- 3. QUESTION DATABASE (SET A - E) ---
# Format dibetulkan untuk mengelakkan SyntaxError
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
    "Set B: Life & Dignity": [("Question placeholder for Set B", ["Option 1", "Option 2", "Option 3"])],
    "Set C: Finance": [("Question placeholder for Set C", ["Option 1", "Option 2", "Option 3"])],
    "Set D: Privacy": [("Question placeholder for Set D", ["Option 1", "Option 2", "Option 3"])],
    "Set E: Future": [("Question placeholder for Set E", ["Option 1", "Option 2", "Option 3"])]
}

# --- 4. SIDEBAR ---
st.sidebar.title("🏥 i-Health OS")
st.sidebar.markdown(f"**Principal Investigator:**\n{PI_NAME}")
st.sidebar.divider()
menu = st.sidebar.radio("Navigation", ["📚 Staff Weekly Training", "💰 Interactive Finance Hub"])
st.sidebar.divider()
st.sidebar.caption("© 2025 | Ref: Fadzil & Mat (2025)")

# --- 5. MODULE: STAFF TRAINING ---
if menu == "📚 Staff Weekly Training":
    st.header("📖 Weekly Staff Refreshment Module")
    
    with st.container():
        c1, c2, c3 = st.columns([2, 2, 1])
        name = c1.text_input("Staff Name")
        s_id = c2.text_input("Staff ID")
        selected_set = c3.selectbox("Select Set", list(questions_db.keys()))

    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

    st.divider()
    st.subheader(f"📝 Assessment: {selected_set}")
    
    # Render Questions
    for i, (q, opts) in enumerate(questions_db[selected_set]):
        st.radio(f"Q{i+1}: {q}", opts, key=f"q_{selected_set}_{i}")
    
    if st.button("Submit Assessment"):
        duration = round((time.time() - st.session_state.start_time) / 60, 2)
        st.success(f"✅ Submission Received for {name} ({s_id})")
        st.write(f"⏱️ **Time Taken:** {duration} minutes")
        st.balloons()
        del st.session_state.start_time

# --- 6. MODULE: FINANCE HUB (FULLY INTERACTIVE) ---
elif menu == "💰 Interactive Finance Hub":
    st.header("💰 Subsidy Hub & Fund Allocator")

    # Current Calculations
    current_balance = st.session_state.total_grant - st.session_state.total_spent

    # --- TOP METRICS ---
    m1, m2, m3 = st.columns(3)
    m1.metric("INITIAL GRANT (MNC A)", f"RM {st.session_state.total_grant:,.2f}")
    m2.metric("TOTAL USED", f"RM {st.session_state.total_spent:,.2f}", delta="- Used", delta_color="inverse")
    
    if current_balance <= 0:
        m3.error("🚨 NO MORE SUBSIDY")
        current_balance = 0
    else:
        m3.metric("REMAINING BALANCE", f"RM {current_balance:,.2f}")

    # --- PATIENT BILLING & CLAIM ---
    st.divider()
    st.subheader("🧾 Real-Time Patient Billing & Claim Simulation")
    
    col_b1, col_b2, col_b3 = st.columns(3)
    
    with col_b1:
        total_bill = st.number_input("Enter Total Patient Bill (RM)", min_value=0.0, value=5000.0)
    
    with col_b2:
        max_sub = current_balance if current_balance > 0 else 0.0
        subsidy_request = st.number_input("Subsidy to Apply (RM)", min_value=0.0, max_value=max_sub, value=min(2000.0, max_sub))
    
    patient_pays = total_bill - subsidy_request
    
    with col_b3:
        st.write("**Payment Summary:**")
        st.write(f"Subsidy Discount: **RM {subsidy_request:,.2f}**")
        st.markdown(f"### Patient Pays: RM {patient_pays:,.2f}")
        
        if st.button("Finalize & Deduct from Grant"):
            if current_balance >= subsidy_request and subsidy_request > 0:
                st.session_state.total_spent += subsidy_request
                st.success(f"Claim Processed! RM {subsidy_request} deducted.")
                time.sleep(1)
                st.rerun()
            else:
                st.error("No subsidy available or invalid amount.")

    # --- UNIT ALLOCATION ---
    st.divider()
    st.subheader("📊 Remaining Fund Allocation by Unit")
    st.write(f"Current Balance (RM {current_balance:,.2f}) redistributed to hospital units:")

    units = ["ICU", "CCU", "Cardiac", "General Ward", "Neonat", "Onco", "Others"]
    u_cols = st.columns(len(units))
    new_pcts = {}
    
    for i, unit in enumerate(units):
        new_pcts[unit] = u_cols[i].number_input(f"{unit} %", value=st.session_state.unit_pct[unit], min_value=0, max_value=100)

    st.session_state.unit_pct = new_pcts
    total_p = sum(new_pcts.values())

    if total_p != 100:
        st.error(f"⚠️ Total Percentage is {total_p}%. Adjust to exactly 100% to view map.")
    else:
        df_units = pd.DataFrame({
            "Unit": units,
            "Amount (RM)": [current_balance * (new_pcts[u]/100) for u in units]
        })
        
        c_t, c_c = st.columns([1, 1])
        with c_t:
            st.table(df_units.style.format({"Amount (RM)": "RM {:,.2f}"}))
        with c_c:
            fig = px.pie(df_units, values='Amount (RM)', names='Unit', hole=0.5, title="Live Allocation Map")
            st.plotly_chart(fig, use_container_width=True)

# --- FOOTER ---
st.divider()
st.markdown(f"<div style='text-align:center;'><b>i-Health OS</b> | Principal Investigator: {PI_NAME}</div>", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import time
import plotly.express as px

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="i-Health OS | Interactive Portal", layout="wide")
PI_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- 2. SESSION STATE (Simpan Data Secara Real-Time) ---
if 'total_grant' not in st.session_state:
    st.session_state.total_grant = 100000.0  # Modal Awal
if 'total_spent' not in st.session_state:
    st.session_state.total_spent = 18000.0   # Duit yang sudah diguna
if 'allocation_pct' not in st.session_state:
    # Peratusan default (Total must be 100)
    st.session_state.allocation_pct = {"ICU": 30, "Dialysis": 20, "Cardiac": 20, "CCU": 15, "General Ward": 15}

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("🏥 i-Health OS")
st.sidebar.markdown(f"**Principal Investigator:**\n{PI_NAME}")
st.sidebar.divider()
menu = st.sidebar.radio("Main Menu", ["📚 Staff Weekly Training", "💰 Interactive Finance Hub"])
st.sidebar.divider()
st.sidebar.caption("© 2025 | Ref: Fadzil & Mat (2025)")

# --- 4. MODULE: STAFF WEEKLY TRAINING ---
if menu == "📚 Staff Weekly Training":
    st.header("📖 Weekly Staff Refreshment Module")
    
    with st.container():
        c1, c2, c3 = st.columns([2, 2, 1])
        name = c1.text_input("Staff Name", placeholder="Enter name")
        s_id = c2.text_input("Staff ID", placeholder="Enter ID")
        set_select = c3.selectbox("Select Set", ["Set A", "Set B", "Set C", "Set D", "Set E"])

    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

    st.divider()
    st.subheader(f"📝 Assessment: {set_select}")
    
    # Contoh Soalan Set A
    if set_select == "Set A":
        st.radio("1. What is the priority during 'Darurah'?", ["Wait for Halal", "Use available (Non-Halal)", "Refuse"], key="seta_q1")
        st.radio("2. Who makes the clinical-ethical decision after hours?", ["Security", "Lead Physician", "Pharmacist"], key="seta_q2")
    else:
        st.info(f"Questions for {set_select} are ready for rotation.")

    if st.button("Submit Assessment"):
        duration = round((time.time() - st.session_state.start_time) / 60, 2)
        st.success(f"✅ Submission Received for {name}!")
        st.write(f"⏱️ Total Time Taken: {duration} minutes")
        del st.session_state.start_time

# --- 5. MODULE: INTERACTIVE FINANCE HUB ---
elif menu == "💰 Interactive Finance Hub":
    st.header("💰 Real-Time Subsidy & Grant Manager")

    # --- BAGIAN A: SETUP GERAN (User boleh ubah) ---
    st.subheader("⚙️ Step 1: Grant & Transaction Setup")
    col_setup1, col_setup2 = st.columns(2)
    
    with col_setup1:
        new_grant = st.number_input("Set Initial Grant Amount (RM)", value=st.session_state.total_grant, step=1000.0)
        if st.button("Update Initial Grant"):
            st.session_state.total_grant = new_grant
            st.success("Initial Grant Updated!")

    with col_setup2:
        spend_amount = st.number_input("Record New Patient Subsidy (RM)", value=0.0, step=100.0)
        if st.button("Process New Claim"):
            st.session_state.total_spent += spend_amount
            st.warning(f"RM {spend_amount} deducted from balance.")

    # --- BAGIAN B: METRICS ---
    st.divider()
    current_balance = st.session_state.total_grant - st.session_state.total_spent
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Annual Grant", f"RM {st.session_state.total_grant:,.2f}")
    m2.metric("Total Used (Claims)", f"RM {st.session_state.total_spent:,.2f}", delta="- Used", delta_color="inverse")
    m3.metric("CURRENT BALANCE", f"RM {current_balance:,.2f}")

    # --- BAGIAN C: ADJUSTABLE ALLOCATION (User boleh adjust slider) ---
    st.divider()
    st.subheader("📊 Step 2: Adjust Unit Allocation (%)")
    st.write("Drag the sliders to redistribute the remaining balance across hospital units.")

    c_icu, c_dia, c_car, c_ccu, c_gen = st.columns(5)
    
    # Slider untuk setiap unit
    icu_p = c_icu.slider("ICU (%)", 0, 100, st.session_state.allocation_pct["ICU"])
    dia_p = c_dia.slider("Dialysis (%)", 0, 100, st.session_state.allocation_pct["Dialysis"])
    car_p = c_car.slider("Cardiac (%)", 0, 100, st.session_state.allocation_pct["Cardiac"])
    ccu_p = c_ccu.slider("CCU (%)", 0, 100, st.session_state.allocation_pct["CCU"])
    gen_p = c_gen.slider("General Ward (%)", 0, 100, st.session_state.allocation_pct["General Ward"])

    # Update session state percentages
    st.session_state.allocation_pct = {"ICU": icu_p, "Dialysis": dia_p, "Cardiac": car_p, "CCU": ccu_p, "General Ward": gen_p}
    
    total_p = icu_p + dia_p + car_p + ccu_p + gen_p
    if total_p != 100:
        st.error(f"⚠️ Total percentage is {total_p}%. Please adjust until it reaches 100%.")
    else:
        st.success("✅ Allocation is balanced at 100%.")

    # Calculation Table & Chart
    df = pd.DataFrame({
        "Unit": ["ICU", "Dialysis", "Cardiac", "CCU", "General Ward"],
        "Allocation (%)": [icu_p, dia_p, car_p, ccu_p, gen_p],
        "Amount (RM)": [current_balance * (icu_p/100), current_balance * (dia_p/100), 
                         current_balance * (car_p/100), current_balance * (ccu_p/100), 
                         current_balance * (gen_p/100)]
    })

    col_t, col_c = st.columns([1, 1])
    with col_t:
        st.table(df.style.format({"Amount (RM)": "RM {:,.2f}"}))
    
    with col_c:
        fig = px.pie(df, values='Amount (RM)', names='Unit', hole=0.5, title="Live Fund Distribution")
        st.plotly_chart(fig, use_container_width=True)

    # --- BAGIAN D: PATIENT BILLING ---
    st.divider()
    st.subheader("🧾 Step 3: Real-Time Patient Billing Simulation")
    bill = st.number_input("Enter Patient Total Bill (RM)", value=5000.0)
    subsidy_rate = st.slider("Subsidy Rate (%)", 0, 100, 40)
    subsidy_val = bill * (subsidy_rate / 100)

    st.markdown(f"""
    | Description | Amount |
    | :--- | :--- |
    | **Total Hospital Bill** | **RM {bill:,.2f}** |
    | i-Health Subsidy (MNC A) | - RM {subsidy_val:,.2f} |
    | **Final Payable by Patient** | **RM {bill - subsidy_val:,.2f}** |
    """)

# --- FOOTER ---
st.divider()
st.markdown(f"<div style='text-align:center;'><b>i-Health OS</b> | Principal Investigator: {PI_NAME}</div>", unsafe_allow_html=True)

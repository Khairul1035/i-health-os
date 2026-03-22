import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. SETTINGS ---
st.set_page_config(page_title="i-Health OS | Precise Finance", layout="wide")
PI_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- 2. SESSION STATE (PENTING UNTUK INTERAKSI) ---
if 'total_grant' not in st.session_state:
    st.session_state.total_grant = 250000.0
if 'total_spent' not in st.session_state:
    st.session_state.total_spent = 43000.0
if 'p_icu' not in st.session_state: st.session_state.p_icu = 30
if 'p_dia' not in st.session_state: st.session_state.p_dia = 20
if 'p_car' not in st.session_state: st.session_state.p_car = 20
if 'p_ccu' not in st.session_state: st.session_state.p_ccu = 15
if 'p_gen' not in st.session_state: st.session_state.p_gen = 15

# --- 3. SIDEBAR ---
st.sidebar.title("🏥 i-Health OS")
st.sidebar.markdown(f"**Principal Investigator:**\n{PI_NAME}")
menu = st.sidebar.radio("Navigation", ["📚 Talent Academy Training", "💰 Interactive Finance Hub"])

# --- 4. FINANCE HUB (LOGIK BARU) ---
if menu == "💰 Interactive Finance Hub":
    st.header("💰 Real-Time Subsidy & Grant Manager")

    # --- STEP 1: TRANSACTION CENTER ---
    st.subheader("⚙️ Step 1: Grant & Spent Management")
    c1, c2 = st.columns(2)
    
    with c1:
        # Update Grant
        input_grant = st.number_input("Update Initial Grant (RM)", value=st.session_state.total_grant, step=1000.0)
        if st.button("Apply New Grant"):
            st.session_state.total_grant = input_grant
            st.success("Grant Updated")

    with c2:
        # Deduct Subsidy
        input_spend = st.number_input("Record New Claim/Spent (RM)", value=0.0, step=100.0)
        if st.button("Process Transaction"):
            st.session_state.total_spent += input_spend
            st.warning(f"RM {input_spend:,.2f} Deducted")

    # --- STEP 2: REAL-TIME METRICS ---
    st.divider()
    # LOGIK UTAMA: Baki mesti tolak perbelanjaan
    current_balance = st.session_state.total_grant - st.session_state.total_spent
    
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("INITIAL GRANT", f"RM {st.session_state.total_grant:,.2f}")
    col_m2.metric("TOTAL SPENT", f"RM {st.session_state.total_spent:,.2f}", delta="- Claimed", delta_color="inverse")
    col_m3.metric("CURRENT BALANCE (To be Allocated)", f"RM {current_balance:,.2f}")

    # --- STEP 3: ADJUSTABLE ALLOCATION ---
    st.divider()
    st.subheader("📊 Step 2: Unit Allocation (%)")
    st.write("Distribute the **Current Balance** (RM {:,.2f}) across units.".format(current_balance))

    # Sliders
    sl1, sl2, sl3, sl4, sl5 = st.columns(5)
    p_icu = sl1.slider("ICU (%)", 0, 100, st.session_state.p_icu)
    p_dia = sl2.slider("Dialysis (%)", 0, 100, st.session_state.p_dia)
    p_car = sl3.slider("Cardiac (%)", 0, 100, st.session_state.p_car)
    p_ccu = sl4.slider("CCU (%)", 0, 100, st.session_state.p_ccu)
    p_gen = sl5.slider("General Ward (%)", 0, 100, st.session_state.p_gen)

    # Simpan peratusan ke session
    st.session_state.p_icu, st.session_state.p_dia, st.session_state.p_car, st.session_state.p_ccu, st.session_state.p_gen = p_icu, p_dia, p_car, p_ccu, p_gen

    total_p = p_icu + p_dia + p_car + p_ccu + p_gen
    
    # Validation
    if total_p != 100:
        st.error(f"⚠️ TOTAL PERCENTAGE IS {total_p}%. MUST BE EXACTLY 100% TO CALCULATE.")
    else:
        st.success("✅ Allocation Balanced (100%)")
        
        # LOGIK PENGIRAAN UNIT: Baki Sebenar x Peratusan
        unit_data = {
            "Unit": ["ICU", "Dialysis", "Cardiac", "CCU", "General Ward"],
            "Allocation (%)": [p_icu, p_dia, p_car, p_ccu, p_gen],
            "Amount (RM)": [
                current_balance * (p_icu/100),
                current_balance * (p_dia/100),
                current_balance * (p_car/100),
                current_balance * (p_ccu/100),
                current_balance * (p_gen/100)
            ]
        }
        df_final = pd.DataFrame(unit_data)

        col_table, col_pie = st.columns([1, 1])
        with col_table:
            st.table(df_final.style.format({"Amount (RM)": "RM {:,.2f}"}))
        
        with col_pie:
            fig = px.pie(df_final, values='Amount (RM)', names='Unit', hole=0.5, 
                         title=f"Distribution of RM {current_balance:,.2f}")
            st.plotly_chart(fig, use_container_width=True)

    # --- STEP 4: PATIENT BILLING ---
    st.divider()
    st.subheader("🧾 Step 3: Billing Simulation")
    bill = st.number_input("Patient Bill (RM)", value=5000.0)
    subsidy_rate = st.slider("Grant Subsidy Rate (%)", 0, 100, 40)
    
    discount = bill * (subsidy_rate/100)
    st.markdown(f"""
    | Description | Amount |
    | :--- | :--- |
    | Total Bill | RM {bill:,.2f} |
    | **Subsidy Offset** | **- RM {discount:,.2f}** |
    | **Final Payable** | **RM {bill - discount:,.2f}** |
    """)

# --- TRAINING MODULE (SIMPEL) ---
elif menu == "📚 Talent Academy Training":
    st.header("📖 Weekly Training Assessment")
    st.write("Complete your weekly set to maintain Shariah competency.")
    # (Kod soalan Set A-E anda kekal di sini)

# --- FOOTER ---
st.divider()
st.markdown(f"<div style='text-align:center;'><b>i-Health OS</b> | PI: {PI_NAME}</div>", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- SYSTEM CONFIGURATION ---
st.set_page_config(page_title="i-Health OS: Systems Transformation", layout="wide")

# --- RESEARCH BRANDING ---
PI_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"
PROJECT_TITLE = "Shariah-Driven Healthcare: Systems Transformation Framework"
JOURNAL_REF = "Fadzil & Mat (2025). Shariah-Driven Healthcare. RABBANICA Journal, 6(1)."

# --- DATA INITIALIZATION (Session State) ---
if 'simulation_data' not in st.session_state:
    st.session_state.simulation_data = {
        'std_cost': 100000,
        'halal_cost': 130000,
        'knowledge_score': 45,
        'ward_capacity': 50,
        'social_fund': 15000
    }

# --- HEADER SECTION ---
st.title("🛡️ i-Health OS: Healthcare Systems Transformation")
st.markdown(f"**Principal Investigator:** {PI_NAME} | **Reference:** {JOURNAL_REF}")
st.divider()

# --- SIDEBAR: THE TRANSFORMATION JOURNEY ---
st.sidebar.header("🗺️ Transformation Journey")
step = st.sidebar.radio("Go to Step:", [
    "1. Audit (Diagnostic)",
    "2. Academy (Knowledge)",
    "3. Infrastructure (Space)",
    "4. Vault (Social Finance)",
    "5. Results (Affordability)"
])

# --- GLOBAL CALCULATIONS ---
halal_premium = st.session_state.simulation_data['halal_cost'] - st.session_state.simulation_data['std_cost']
offset = st.session_state.simulation_data['social_fund']
net_burden = halal_premium - offset
affordability_boost = (offset / halal_premium * 100) if halal_premium > 0 else 100

# --- STEP 1: AUDIT (DIAGNOSTIC) ---
if step == "1. Audit (Diagnostic)":
    st.subheader("Step 1: Financial & Compliance Audit")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Input current hospital costs to identify the 'Halal Premium' gap.")
        st.session_state.simulation_data['std_cost'] = st.number_input("Standard Annual Procurement (RM)", value=st.session_state.simulation_data['std_cost'])
        st.session_state.simulation_data['halal_cost'] = st.number_input("Halal-Certified Procurement (RM)", value=st.session_state.simulation_data['halal_cost'])
    with col2:
        st.metric("Identified Halal Premium", f"RM {halal_premium:,}")
        st.warning(f"Your hospital is currently spending RM {halal_premium:,} extra per year to maintain Shariah compliance.")

# --- STEP 2: ACADEMY (KNOWLEDGE) ---
elif step == "2. Academy (Knowledge)":
    st.subheader("Step 2: Staff Academy & Knowledge Empowerment")
    st.write("Solving the 'Practitioner Knowledge Gap' identified in the 2025 research.")
    
    knowledge = st.slider("Current Staff Shariah Competency (%)", 0, 100, st.session_state.simulation_data['knowledge_score'])
    st.session_state.simulation_data['knowledge_score'] = knowledge
    
    if knowledge < 50:
        st.error("🚨 **High Risk:** Over-reliance on Shariah Officers detected. Urgent 'Structured Shariah Training' required.")
    else:
        st.success("✅ **Competency Stable:** Staff can make independent clinical-Shariah decisions.")

# --- STEP 3: INFRASTRUCTURE (SPACE) ---
elif step == "3. Infrastructure (Space)":
    st.subheader("Step 3: AI-Driven Ward Optimization")
    st.write("Optimizing existing space for gender segregation (hifz al-nafs) to save CAPEX.")
    
    capacity = st.number_input("Total Bed Capacity", value=st.session_state.simulation_data['ward_capacity'])
    st.session_state.simulation_data['ward_capacity'] = capacity
    
    st.info("AI Digital Twin Suggestion: Reconfiguring Ward B & C into gender-segregated zones saves RM 250,000 in construction costs.")
    
    fig = go.Figure(data=[go.Pie(labels=['Female Optimized', 'Male Optimized', 'Critical/Mixed'], 
                                 values=[capacity*0.4, capacity*0.4, capacity*0.2], hole=.3)])
    st.plotly_chart(fig)

# --- STEP 4: VAULT (SOCIAL FINANCE) ---
elif step == "4. Vault (Social Finance)":
    st.subheader("Step 4: The Blockchain-Waqf Finance Vault")
    st.write("Using Islamic Social Finance to neutralize the Halal Premium.")
    
    fund = st.select_slider("Simulate Zakat/Waqf Fund Injection (RM)", options=list(range(0, 50001, 5000)), value=st.session_state.simulation_data['social_fund'])
    st.session_state.simulation_data['social_fund'] = fund
    
    st.write("🔍 **Blockchain Ledger (Mock):**")
    st.table(pd.DataFrame({
        "Transaction ID": ["TX882", "TX885", "TX890"],
        "Source": ["State Waqf Fund", "Zakat Asnaf Fund", "Public Donation"],
        "Target Component": ["Clinical Meds", "Infrastructure", "Staff Training"],
        "Amount (RM)": [fund*0.5, fund*0.3, fund*0.2]
    }))

# --- STEP 5: RESULTS (AFFORDABILITY) ---
elif step == "5. Results (Affordability)":
    st.subheader("Step 5: Patient Affordability & Impact")
    st.write("Final outcome of the Systems Transformation.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Sustainability Index", f"{round(affordability_boost, 1)}%")
        st.metric("Net Hospital Burden", f"RM {max(0, net_burden):,}")
    
    with col_b:
        st.markdown("### 🤖 AI Co-Analyst Final Report")
        if affordability_boost >= 100:
            st.success(f"**TRANSFORMATION SUCCESSFUL:** The Shariah-Compliance cost is now 100% covered by Social Finance. Hospital is highly affordable.")
        else:
            st.error(f"**GAP DETECTED:** You still have a RM {net_burden:,} deficit. Refer to Pillar 2 (Training) to improve operational efficiency.")

    # Practical Billing Example
    st.divider()
    st.subheader("💳 Practical Billing Simulation (For Patient)")
    patient_bill = 1500
    discount = (patient_bill * (affordability_boost/100)) * 0.3 # Simulated 30% bill reduction logic
    st.markdown(f"""
    | Description | Amount |
    | :--- | :--- |
    | **Total Medical Treatment Cost** | **RM {patient_bill:,.2f}** |
    | i-Health OS Social Fund Offset | - RM {discount:,.2f} |
    | **Final Amount Payable by Patient** | **RM {patient_bill-discount:,.2f}** |
    """)

# --- FOOTER ---
st.divider()
st.markdown(f"**© 2025 i-Health OS Project** | Principal Investigator: **{PI_NAME}**")
st.markdown(f"**Academic Link:** Read full framework in *{JOURNAL_REF}*")

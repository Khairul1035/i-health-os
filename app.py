import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# --- CORPORATE CONFIGURATION ---
st.set_page_config(page_title="i-Health OS | Enterprise Systems", page_icon="🏢", layout="wide")

# --- PREMIUM CORPORATE CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #F9FAFB; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #E5E7EB; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .sidebar .sidebar-content { background-color: #111827; color: white; }
    .pi-header { background: linear-gradient(90deg, #1E3A8A 0%, #1E40AF 100%); padding: 30px; border-radius: 15px; color: white; margin-bottom: 25px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.2); }
    .assessment-box { background-color: #ffffff; padding: 25px; border-radius: 15px; border: 1px solid #D1D5DB; margin-bottom: 20px; }
    .ai-report { background-color: #EFF6FF; border-left: 5px solid #1D4ED8; padding: 20px; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- LEADERSHIP & AUTHENTICATION ---
PI_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"
PROJECT_REF = "Fadzil & Mat (2025). Shariah-Driven Healthcare. RABBANICA, 6(1)."

# --- DATA PERSISTENCE (SESSION STATE) ---
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'audit_data' not in st.session_state:
    st.session_state.audit_data = {"std": 500000, "hal": 650000, "zakat": 50000}

def log_event(module, action):
    st.session_state.logs.append({
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Module": module,
        "Action": action,
        "Status": "✅ Synced"
    })

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2764/2764442.png", width=70)
    st.title("i-Health OS")
    st.caption("Enterprise Systems Transformation")
    st.divider()
    menu = st.radio("Transformation Phases", [
        "🏢 Executive Overview",
        "📊 Phase 1: Diagnostic Audit",
        "🎓 Phase 2: Talent Academy",
        "📐 Phase 3: Spatial Optimizer",
        "🔐 Phase 4: Social Finance Vault",
        "📈 Phase 5: Affordability Report"
    ])
    st.divider()
    st.info(f"**PI:** {PI_NAME}")

# --- MODULE 0: OVERVIEW ---
if menu == "🏢 Executive Overview":
    st.markdown(f"""
    <div class="pi-header">
        <h1>i-Health OS: Healthcare Systems Transformation</h1>
        <p>Principal Investigator: <b>{PI_NAME}</b> | Global Reference: {PROJECT_REF}</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("National Compliance Score", "82%", "+1.5%")
    c2.metric("Knowledge Gap Reduction", "45%", "In Progress")
    c3.metric("Social Fund Coverage", "RM 12.4M", "Stable")

    st.subheader("📡 Real-Time Transformation Logs")
    if st.session_state.logs:
        st.table(pd.DataFrame(st.session_state.logs).tail(5))
    else:
        st.write("System Ready. Waiting for input...")

# --- MODULE 1: AUDIT ---
elif menu == "📊 Phase 1: Diagnostic Audit":
    st.subheader("🛠️ Step 1: Operational Cost & Compliance Diagnostic")
    col_in, col_viz = st.columns([1, 1])
    with col_in:
        st.session_state.audit_data['std'] = st.number_input("Standard Annual Procurement (RM)", value=st.session_state.audit_data['std'])
        st.session_state.audit_data['hal'] = st.number_input("Halal-Certified Procurement (RM)", value=st.session_state.audit_data['hal'])
        if st.button("Sync Audit Data"):
            log_event("Audit", "Cost Gap Analysis Executed")
    with col_viz:
        premium = st.session_state.audit_data['hal'] - st.session_state.audit_data['std']
        st.metric("Detected 'Halal Premium' Burden", f"RM {premium:,}")
        fig = px.pie(values=[st.session_state.audit_data['std'], premium], names=['Standard Cost', 'Halal Premium'], 
                     color_discrete_sequence=['#1E3A8A', '#EF4444'], hole=0.5)
    st.plotly_chart(fig, use_container_width=True)

# --- MODULE 2: ACADEMY (ENHANCED WITH 15+5 QUESTIONS) ---
elif menu == "🎓 Phase 2: Talent Academy":
    st.subheader("🎓 Phase 2: Bi-Weekly Talent Competency Assessment")
    st.markdown("""
    **Mandatory Evaluation:** Clinical staff must complete this every 14 days to maintain 'Shariah-Practitioner' status.
    *Includes 15 Objective & 5 Subjective Case Studies analyzed by AI.*
    """)
    
    set_choice = st.selectbox("Select Training Set", ["Set A: Clinical Emergencies", "Set B: Gender & Privacy", "Set C: Pharmacy Logistics"])

    with st.container():
        st.write("---")
        st.write("### 📝 Part A: Objective Assessment (15 MCQ)")
        
        # Displaying 3 sample MCQ representing the 15-question structure
        q1 = st.radio("1. Under 'Darurah' (Necessity), which medicine takes priority?", ["Wait for Halal stock", "Use non-halal alternative immediately", "Request patient consent first"])
        q2 = st.radio("2. Gender segregation in physical examination is primary related to which Maqasid?", ["Protection of Wealth", "Protection of Dignity (Nafs)", "Protection of Religion"])
        q3 = st.radio("3. A Shariah Officer is unavailable after 11 PM. Who makes the clinical-ethical decision?", ["The Lead Physician", "The Patient's Family", "Postpone treatment"])
        st.caption("*(System displays 12 additional validated MCQ here...)*")

        st.divider()
        st.write("### ✍️ Part B: Subjective Logic (5 Scenarios)")
        st.info("AI Co-Researcher uses Semantic Logic to verify your alignment with the Hospital Framework.")
        
        s1 = st.text_area("S1: Explain how you would manage a conflict where a non-muslim doctor disagrees with a Shariah-based gender protocol?")
        s2 = st.text_area("S2: If the CFO asks you to cut costs by switching to non-halal consumables, what is your Shariah-Clinical justification to maintain Halal?")
        st.caption("*(System displays 3 additional Scenario-based Subjective questions...)*")

        if st.button("Submit to AI Co-Researcher"):
            with st.spinner("AI analyzing semantic patterns and Maqasid-alignment..."):
                time.sleep(2)
                st.success("Assessment Recorded!")
                log_event("Academy", f"Assessment {set_choice} Completed")
                
                st.markdown("""
                <div class="ai-report">
                    <h4>🤖 AI Co-Researcher Evaluation</h4>
                    <p><b>Objective Score:</b> 14/15 | <b>Subjective Alignment:</b> 92% (Optimal)</p>
                    <p><b>Critical Insight:</b> Your response to S2 shows a strong grasp of 'Sustainability through Ethics'. However, improve your understanding of 'Hifz al-Mal' in Phase 4.</p>
                </div>
                """, unsafe_allow_html=True)

# --- MODULE 4: VAULT ---
elif menu == "🔐 Phase 4: Social Finance Vault":
    st.subheader("🔐 Phase 4: Transparency Ledger & Fund Injection")
    amount = st.select_slider("Inject Social Capital (Zakat/Waqf) - RM", options=[50000, 100000, 150000, 200000], value=st.session_state.audit_data['zakat'])
    st.session_state.audit_data['zakat'] = amount
    
    if st.button("Authorize Blockchain Transfer"):
        log_event("Vault", f"Injected RM {amount:,}")
        st.balloons()

    ledger = pd.DataFrame({
        "Hash ID": ["0x992...f1", "0x884...a3", "0x771...e2"],
        "Source": ["Waqf Healthcare Fund", "State Zakat Authority", "Corporate CSR"],
        "Impact": ["Halal Meds Offset", "Training Academy", "Ward Segregation"],
        "Value (RM)": [amount*0.5, amount*0.2, amount*0.3]
    })
    st.table(ledger)

# --- MODULE 5: RESULTS ---
elif menu == "📈 Phase 5: Affordability Report":
    st.subheader("📈 Phase 5: Systems Transformation Results")
    
    premium = st.session_state.audit_data['hal'] - st.session_state.audit_data['std']
    offset = st.session_state.audit_data['zakat']
    sustainability = (offset / premium * 100) if premium > 0 else 100
    
    st.markdown(f"""
    <div style="background-color:#1E3A8A; color:white; padding:25px; border-radius:15px;">
        <h2>Financial Resilience Score: {round(sustainability, 1)}%</h2>
        <p>The system successfully offsets the Halal Premium through Social Finance integration.</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.subheader("💳 Patient Receipt Simulation")
    col_bill, col_ai = st.columns(2)
    
    with col_bill:
        base_bill = 2500
        offset_value = base_bill * (sustainability/100) * 0.4
        st.markdown(f"""
        | Item Description | Amount (RM) |
        | :--- | :--- |
        | Total Hospital Treatment Cost | RM {base_bill:,.2f} |
        | **i-Health OS Social Offset (Zakat/Waqf)** | **- RM {offset_value:,.2f}** |
        | **Final Amount Payable by Patient** | **RM {base_bill - offset_value:,.2f}** |
        """)
        
    with col_ai:
        st.info("**🤖 AI Co-Analyst Strategic Recommendation:** Your high 'Talent Academy' score (92%) has reduced operational risk by 15%. Recommend re-allocating 10% of Zakat funds to 'Infrastructure Pillar' for long-term scalability.")

# --- CORPORATE FOOTER ---
st.markdown("---")
st.markdown(f"""
<div style="text-align:center; padding:20px;">
    <p><b>i-Health OS Enterprise</b> | Principal Investigator: <b>{PI_NAME}</b></p>
    <p><small>Reference: Fadzil, M. K. R. M. & Mat, H. (2025). Shariah-Driven Healthcare. RABBANICA, 6(1).</small></p>
</div>
""", unsafe_allow_html=True)

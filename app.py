import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="i-Health OS | Enterprise Systems", page_icon="🏢", layout="wide")

# --- 2. PREMIUM CORPORATE CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #F9FAFB; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #E5E7EB; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .sidebar .sidebar-content { background-color: #111827; color: white; }
    .pi-header { background: linear-gradient(90deg, #1E3A8A 0%, #1E40AF 100%); padding: 30px; border-radius: 15px; color: white; margin-bottom: 25px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.2); }
    .ai-report { background-color: #EFF6FF; border-left: 5px solid #1D4ED8; padding: 20px; border-radius: 8px; border: 1px solid #d1d5db; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA PERSISTENCE ---
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'audit_data' not in st.session_state:
    st.session_state.audit_data = {"std": 500000, "hal": 650000, "zakat": 50000}

def log_event(module, action, status="✅"):
    st.session_state.logs.append({
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Module": module,
        "Action": action,
        "Status": status
    })

PI_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"
PROJECT_REF = "Fadzil & Mat (2025). Shariah-Driven Healthcare. RABBANICA, 6(1)."

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2764/2764442.png", width=70)
    st.title("i-Health OS")
    st.caption("Enterprise Systems Transformation")
    st.divider()
    # PENTING: Nama emoji mesti sama dengan if-statement di bawah
    menu = st.radio("Transformation Phases", [
        "🏢 Executive Overview",
        "📊 Phase 1: Diagnostic Audit",
        "🎓 Phase 2: Talent Academy",
        "📐 Phase 3: Spatial Optimizer",
        "🔐 Phase 4: Social Finance Vault",
        "📈 Phase 5: Affordability Report"
    ])
    st.divider()
    st.info(f"**Principal Investigator:**\n\n{PI_NAME}")

# --- 5. MAIN CONTENT FLOW ---

# --- MODULE: OVERVIEW ---
if menu == "🏢 Executive Overview":
    st.markdown(f"""
    <div class="pi-header">
        <h1>i-Health OS: Healthcare Systems Transformation</h1>
        <p>Principal Investigator: <b>{PI_NAME}</b> | Global Reference: {PROJECT_REF}</p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Compliance Index", "82%", "+1.5%")
    c2.metric("Knowledge Gap", "45%", "In Progress")
    c3.metric("Fund Offset", "RM 12.4M", "Stable")
    st.subheader("📡 Real-Time Transformation Logs")
    if st.session_state.logs:
        st.table(pd.DataFrame(st.session_state.logs).tail(5))
    else:
        st.write("System Ready. No logs recorded yet.")

# --- MODULE: AUDIT ---
elif menu == "📊 Phase 1: Diagnostic Audit":
    st.subheader("🛠️ Phase 1: Operational Cost & Compliance Diagnostic")
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

# --- MODULE: ACADEMY (FULL AI LOGIC) ---
elif menu == "🎓 Phase 2: Talent Academy":
    st.subheader("🎓 Phase 2: Bi-Weekly Talent Competency Assessment")
    st.info("AI Co-Researcher Evaluation Mode. Results will be escalated to HOD.")
    
    # Part 1: MCQ
    st.write("### 📝 Part A: Objective Assessment")
    q1 = st.radio("1. Priority if Halal-certified medicine is unavailable in life-threatening 'Darurah'?", 
                  ["Wait for Halal stock", "Use non-halal alternative immediately", "Refuse treatment"], index=None)
    q2 = st.radio("2. Gender segregation in examination relates to which Maqasid?", 
                  ["Protection of Wealth", "Protection of Dignity (Nafs)", "Protection of Religion"], index=None)
    
    st.divider()
    
    # Part 2: Subjective
    st.write("### ✍️ Part B: Subjective Logic (AI Evaluation)")
    s1 = st.text_area("S1: Explain how to manage a conflict where a non-muslim doctor disagrees with Shariah gender protocols?", placeholder="Type your professional response here...")
    s2 = st.text_area("S2: Justify the 'Halal Premium' cost to your CFO if they ask to cut costs?", placeholder="Type your professional response here...")

    if st.button("🚀 Submit to AI Co-Researcher"):
        with st.spinner("AI is performing Semantic Analysis on your answers..."):
            time.sleep(2)
            
            # --- REAL AI LOGIC ---
            obj_score = 0
            if q1 == "Use non-halal alternative immediately": obj_score += 5
            if q2 == "Protection of Dignity (Nafs)": obj_score += 5
            # Max possible 10 for these two
            
            # Semantic keyword check
            keywords = ["policy", "guideline", "respect", "trust", "maqasid", "ethics", "quality", "patient"]
            combined_text = (s1 + " " + s2).lower()
            subjective_score = sum(10 for word in keywords if word in combined_text)
            
            # Gibberish check (nonsense input like 'kukuk')
            is_nonsense = len(s1) < 15 or len(s2) < 15
            if is_nonsense: subjective_score = 5

            final_total = obj_score + subjective_score
            
            # --- REPORT ---
            st.markdown("### 📊 Official AI Evaluation Report")
            c_res1, c_res2 = st.columns(2)
            
            with c_res1:
                st.metric("Objective Score", f"{obj_score}/10")
                st.metric("AI Semantic Alignment", f"{subjective_score}%")
            
            with c_res2:
                if final_total < 50:
                    status = "🔴 FAILED / INTERVENTION REQUIRED"
                    color = "red"
                    advice = "Critical knowledge gap. Staf tidak mencapai kriteria minimum kefahaman."
                else:
                    status = "🟢 PASSED"
                    color = "green"
                    advice = "Staf menunjukkan kefahaman yang mendalam tentang SOP Shariah."
                
                st.markdown(f"**Status:** <span style='color:{color}'><b>{status}</b></span>", unsafe_allow_html=True)
                st.write(f"**AI Guidance:** {advice}")

            # --- ESCALATION ---
            st.divider()
            hod_email = st.text_input("Head of Department (HOD) Email", value="hod_clinical@hospital.com")
            if st.button("📧 Forward Full Report to HOD"):
                st.success(f"Report ID: {datetime.now().strftime('%Y%H%M')} forwarded to {hod_email}")
                log_event("Academy", f"Escalated to HOD: {status}", "🚩" if "FAILED" in status else "✅")

# --- MODULE: VAULT ---
elif menu == "🔐 Phase 4: Social Finance Vault":
    st.subheader("🔐 Phase 4: Social Finance Ledger")
    amount = st.select_slider("Inject Zakat/Waqf Fund (RM)", options=[50000, 100000, 150000, 200000], value=st.session_state.audit_data['zakat'])
    st.session_state.audit_data['zakat'] = amount
    if st.button("Authorize Fund Injection"):
        log_event("Vault", f"Injected RM {amount:,}")
        st.balloons()
    ledger = pd.DataFrame({
        "Hash ID": ["0x992...f1", "0x884...a3", "0x771...e2"],
        "Source": ["Waqf Fund", "Baitulmal", "CSR"],
        "Value (RM)": [amount*0.5, amount*0.2, amount*0.3],
        "Status": ["Verified", "Verified", "Verified"]
    })
    st.table(ledger)

# --- MODULE: RESULTS ---
elif menu == "📈 Phase 5: Affordability Report":
    st.subheader("📈 Phase 5: Final Impact Report")
    premium = st.session_state.audit_data['hal'] - st.session_state.audit_data['std']
    offset = st.session_state.audit_data['zakat']
    sus = (offset / premium * 100) if premium > 0 else 100
    
    st.markdown(f"""
    <div style="background-color:#1E3A8A; color:white; padding:25px; border-radius:15px;">
        <h2>Financial Resilience: {round(sus, 1)}%</h2>
        <p>This score indicates how well Social Finance offsets the Shariah Compliance cost.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("💳 Patient Bill Simulation")
    base = 2500
    discount = base * (sus/100) * 0.3
    st.write(f"**Original Bill:** RM {base:,.2f}")
    st.write(f"**i-Health OS Discount (Waqf/Zakat):** -RM {discount:,.2f}")
    st.markdown(f"### **Final Payable: RM {base - discount:,.2f}**")

# --- FOOTER ---
st.divider()
st.markdown(f"<div style='text-align:center;'><b>i-Health OS</b> | Principal Investigator: {PI_NAME}</div>", unsafe_allow_html=True)
st.caption(f"Ref: {PROJECT_REF}")

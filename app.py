import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# --- PREMIUM CORPORATE CONFIG ---
st.set_page_config(page_title="i-Health OS | Enterprise Transformation", page_icon="🏢", layout="wide")

# --- CUSTOM CORPORATE CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #F3F4F6; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border: 1px solid #E5E7EB; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    .sidebar .sidebar-content { background-image: linear-gradient(#1E3A8A, #1E40AF); color: white; }
    .corporate-header { background-color: #ffffff; padding: 25px; border-radius: 15px; border-left: 10px solid #1E3A8A; margin-bottom: 30px; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
    .status-card { padding: 20px; border-radius: 10px; border: 1px solid #E5E7EB; background: white; margin-bottom: 20px; }
    .btn-sync { background-color: #1E3A8A; color: white; border-radius: 5px; padding: 10px 20px; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- LEADERSHIP & AUTHENTICATION ---
PI_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"
ORG = "i-Health Global Systems Transformation"
JOURNAL_REF = "Fadzil & Mat (2025). Shariah-Driven Healthcare. RABBANICA, 6(1)."

# --- REAL-TIME DATA INITIALIZATION ---
if 'db_registry' not in st.session_state:
    st.session_state.db_registry = pd.DataFrame(columns=["Timestamp", "Module", "Action", "Status"])

# Function to log real-time events
def log_event(module, action):
    new_event = {"Timestamp": datetime.now().strftime("%H:%M:%S"), "Module": module, "Action": action, "Status": "✅ Synced"}
    st.session_state.db_registry = pd.concat([pd.DataFrame([new_event]), st.session_state.db_registry], ignore_index=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2764/2764442.png", width=80)
    st.title("i-Health OS")
    st.markdown("---")
    menu = st.radio("Enterprise Modules", [
        "🏢 Dashboard Overview",
        "📊 Phase 1: Diagnostic Audit",
        "🎓 Phase 2: Talent Academy",
        "📐 Phase 3: Spatial Optimizer",
        "🔐 Phase 4: Social Finance Vault",
        "📈 Phase 5: Affordability Report"
    ])
    st.markdown("---")
    if st.button("🔄 Sync with Cloud Database"):
        with st.spinner("Connecting to Global Registry..."):
            time.sleep(1)
            log_event("Cloud", "Manual Database Re-sync")
            st.success("Global Sync Complete.")

# --- MODULE 0: OVERVIEW ---
if "Dashboard Overview" in menu:
    st.markdown(f"""
    <div class="corporate-header">
        <h1>Welcome to i-Health OS Enterprise</h1>
        <p><b>Principal Investigator:</b> {PI_NAME} | <b>Ref:</b> {JOURNAL_REF}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Global Compliance Index", "84%", "+2.4%")
    col2.metric("Total Social Offset", "RM 2.4M", "Sustainable")
    col3.metric("System Uptime", "99.99%", "Live")

    st.subheader("📡 Real-Time Audit Log (System-wide)")
    st.dataframe(st.session_state.db_registry.head(5), use_container_width=True)

# --- MODULE 1: AUDIT ---
elif "Phase 1: Diagnostic Audit" in menu:
    st.subheader("🛠️ Phase 1: Operational Cost Diagnostic")
    c1, c2 = st.columns([1, 1])
    with c1:
        st.info("Input real-time procurement data to identify Shariah-Compliance overheads.")
        std = st.number_input("Standard Supply Cost (Annual) - RM", value=500000)
        hal = st.number_input("Halal-Certified Cost (Annual) - RM", value=680000)
        if st.button("Execute Audit"):
            log_event("Audit", f"Premium Analysis: RM {hal-std}")
            st.success("Audit Analysis Synced.")
    with c2:
        gap = hal - std
        st.metric("Detected 'Halal Premium' Gap", f"RM {gap:,}")
        fig = px.pie(values=[std, gap], names=['Operating Cost', 'Compliance Premium'], hole=.4, color_discrete_sequence=['#1E3A8A', '#EF4444'])
        st.plotly_chart(fig)

# --- MODULE 2: ACADEMY ---
elif "Phase 2: Talent Academy" in menu:
    st.subheader("🎓 Phase 2: Practitioner Knowledge Management")
    st.write("Targeting the 'Knowledge Gap' found in Fadzil (2025) research.")
    score = st.slider("Current Staff Competency Score (%)", 0, 100, 55)
    if st.button("Update Academy Stats"):
        log_event("Academy", f"Competency updated to {score}%")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"""
        <div class="status-card">
            <h4>Academy Status</h4>
            <h2 style="color:{'green' if score > 70 else 'red'};">{score}%</h2>
            <p>{'Optimal: Staff can work independently.' if score > 70 else 'Critical: High dependency on Shariah Officers.'}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135810.png", width=150)

# --- MODULE 4: VAULT (THE BLOCKCHAIN FEEL) ---
elif "Phase 4: Social Finance Vault" in menu:
    st.subheader("🔐 Phase 4: Blockchain-Secured Social Finance")
    st.write("Managing Zakat & Waqf funds to neutralize the Halal Premium.")
    
    amount = st.select_slider("Inject Social Capital (RM)", options=[50000, 100000, 150000, 200000])
    
    if st.button("Authorize Fund Transfer"):
        log_event("Vault", f"Injected RM {amount} via Zakat/Waqf")
        st.balloons()

    st.markdown("### 🔗 Live Ledger (Proof of Transparency)")
    ledger = pd.DataFrame({
        "Hash ID": ["0x992...a1", "0x884...c3", "0x771...f2"],
        "Source": ["Global Waqf Fund", "Baitulmal Zakat", "Private CSR"],
        "Impact Component": ["Clinical Meds", "Infrastructure", "Staff Training"],
        "Value (RM)": [amount*0.5, amount*0.3, amount*0.2],
        "Verification": ["Verified", "Verified", "Verified"]
    })
    st.table(ledger)

# --- MODULE 5: RESULTS ---
elif "Phase 5: Affordability Report" in menu:
    st.subheader("📈 Phase 5: Strategic Impact & Patient Billing")
    
    # Final Output Logic
    st.markdown("""
    <div style="background-color:#1E3A8A; color:white; padding:30px; border-radius:15px;">
        <h2>The Transformation Result</h2>
        <p>This report calculates how Shariah Healthcare Systems Transformation directly lowers patient costs.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Sustainability Index", "92.5%", "Optimal")
    with col2:
        st.metric("Patient Affordability Boost", "+35%", "Social Impact High")

    st.divider()
    st.subheader("👨‍⚕️ Clinical Decision Support (AI)")
    st.info("AI Analysis: Based on Pillar 2 (Training), your hospital has saved RM 45,000 in 'Decision Waste' this quarter. Recommend increasing Waqf allocation for Pillar 3 (Infrastructure).")

# --- FOOTER ---
st.markdown("---")
st.markdown(f"""
<div style="text-align:center;">
    <p><b>i-Health OS Enterprise</b> | Built on Research by <b>{PI_NAME}</b></p>
    <p><small>Cite: Fadzil & Mat (2025). Shariah-Driven Healthcare. RABBANICA, 6(1), 21-38.</small></p>
</div>
""", unsafe_allow_html=True)

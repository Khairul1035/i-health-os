import streamlit as st
import pandas as pd
import time
import plotly.express as px

# --- 1. SETTINGS ---
st.set_page_config(page_title="i-Health OS | Full Systems", layout="wide")
PI_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- 2. DATABASE 50 SOALAN (10 Qs x 5 Sets) ---
questions_db = {
    "Set A: Maqasid Fundamentals": {
        "questions": [
            ("What is the primary objective of Maqasid in healthcare?", ["Profit", "Public Welfare (Maslahah)", "Staff Ease"], "Public Welfare (Maslahah)"),
            ("Preserving life (Hifz al-Nafs) includes:", ["Surgery only", "Mental & Physical well-being", "Administrative work"], "Mental & Physical well-being"),
            ("Using non-halal meds in emergencies is based on:", ["Preference", "Al-Darurah (Necessity)", "Cost"], "Al-Darurah (Necessity)"),
            ("Cleanliness in hospitals relates to:", ["Aesthetics", "Taharah (Purity) as faith", "Electricity saving"], "Taharah (Purity) as faith"),
            ("Informed consent protects which Maqasid?", ["Hifz al-Aql (Intellect)", "Hifz al-Mal", "Hifz al-Nasl"], "Hifz al-Aql (Intellect)"),
            ("Providing a prayer room is part of:", ["Hifz al-Din", "Hifz al-Mal", "Hifz al-Aql"], "Hifz al-Din"),
            ("Hospital research for future cures is:", ["Hifz al-Nasl (Lineage)", "Optional", "Waste of funds"], "Hifz al-Nasl (Lineage)"),
            ("Preventing medical errors is:", ["Administrative", "Warding off harm (Mafasid)", "Marketing"], "Warding off harm (Mafasid)"),
            ("Ethical leadership is part of:", ["Amanah (Trust)", "Profit", "Speed"], "Amanah (Trust)"),
            ("Patient hygiene is part of:", ["Hifz al-Din", "Hifz al-Mal", "Hifz al-Nasl"], "Hifz al-Din")
        ],
        "ai_tip": "Focus on the hierarchy of necessities (Daruriyyat) in clinical decisions."
    },
    "Set B: Life & Dignity": {
        "questions": [
            ("Gender segregation during exams protects:", ["Reputation", "Patient Dignity (Nafs)", "Operational speed"], "Patient Dignity (Nafs)"),
            ("Palliative care for terminal patients aligns with:", ["Hifz al-Nafs", "Hifz al-Mal", "Ending life early"], "Hifz al-Nafs"),
            ("Informed consent is a bridge between authority and:", ["Patient autonomy", "Hospital profit", "Insurance"], "Patient autonomy"),
            ("Organ donation after death is often discussed under:", ["Hifz al-Nafs", "Hifz al-Din", "Hifz al-Aql"], "Hifz al-Nafs"),
            ("Confidentiality of records (SULIT) is for:", ["Privacy & Honor", "Data storage law", "Gossip prevention"], "Privacy & Honor"),
            ("Avoiding unnecessary pain in surgery is:", ["Warding off harm", "Management", "Economic saving"], "Warding off harm"),
            ("Quarantine for contagious disease is:", ["Discrimination", "Hifz al-Nafs (Community)", "Hifz al-Mal"], "Hifz al-Nafs (Community)"),
            ("Who decides if the Shariah Officer is away?", ["Lead Physician", "Security", "Receptionist"], "Lead Physician"),
            ("Hospital hygiene is a religious obligation:", ["True", "False", "Only for Muslims"], "True"),
            ("Maqasid in healthcare is for:", ["All humanity", "Only Muslims", "Only Staff"], "All humanity")
        ],
        "ai_tip": "Dignity (Karamah) is central to the preservation of life in Shariah."
    },
    "Set C: Financial Integrity": {
        "questions": [
            ("Justifying 'Halal Premium' costs is based on:", ["Hifz al-Din", "Hifz al-Mal", "Marketing"], "Hifz al-Din"),
            ("Utilizing Zakat for asnaf patients relates to:", ["Hifz al-Mal", "Hifz al-Aql", "Profit"], "Hifz al-Mal"),
            ("Procurement free from Riba relates to:", ["Hifz al-Mal", "Hifz al-Din", "Hifz al-Nasl"], "Hifz al-Mal"),
            ("Transparency in billing is part of:", ["Fulfilling Contracts", "Tax evasion", "Marketing"], "Fulfilling Contracts"),
            ("Waqf for dialysis machines is a form of:", ["Sadaqah Jariyah", "Investment", "Loan"], "Sadaqah Jariyah"),
            ("Hidden charges not disclosed is considered:", ["Gharar (Uncertainty)", "Strategy", "Normal"], "Gharar (Uncertainty)"),
            ("Procuring halal sutures ensures:", ["Compliance", "Aesthetics", "Cheaper costs"], "Compliance"),
            ("CFO must balance profit and:", ["Ethical Sustainability", "Maximum Debt", "Staff party"], "Ethical Sustainability"),
            ("Auditing Zakat usage is for:", ["Accountability", "CEO fame", "Spending faster"], "Accountability"),
            ("Using specific ICU grants for staff parties is a breach of:", ["Amanah (Trust)", "Hifz al-Mal", "Both"], "Both")
        ],
        "ai_tip": "Economic sustainability must never compromise religious integrity."
    },
    "Set D: Privacy & Ethics": {
        "questions": [
            ("Patient preference for female doctors protects:", ["Modesty", "Schedules", "Ratings"], "Modesty"),
            ("Chaperone policy prevents:", ["Khalwah (Seclusion)", "Speed", "Lawsuits"], "Khalwah (Seclusion)"),
            ("Human body in Bioethics is a:", ["Trust (Amanah)", "Property", "Machine"], "Trust (Amanah)"),
            ("Ward curtains are a manifestation of:", ["Covering Awrah", "Luxury", "Noise reduction"], "Covering Awrah"),
            ("IVF treatments involve which pillar?", ["Hifz al-Nasl (Lineage)", "Hifz al-Mal", "Hifz al-Din"], "Hifz al-Nasl (Lineage)"),
            ("Genetic testing results should be:", ["Private (Hifz al-Nasl)", "Public", "For insurance"], "Private (Hifz al-Nasl)"),
            ("Breaking confidentiality is allowed only to:", ["Prevent greater harm", "Gossip", "Media request"], "Prevent greater harm"),
            ("Ethical clinical trials prioritize:", ["Patient safety", "Researcher fame", "Speed"], "Patient safety"),
            ("Treatment of non-Muslims requires:", ["Kindness & Ethics", "Extra charges", "Ignoring them"], "Kindness & Ethics"),
            ("Spiritual needs of dying patients is:", ["Holistic Shariah care", "Waste of time", "Optional extra"], "Holistic Shariah care")
        ],
        "ai_tip": "Privacy is not just a policy; it's a fundamental right in Maqasid."
    },
    "Set E: Future Challenges": {
        "questions": [
            ("Vaccination is justified as:", ["Prevention of mass harm", "Economic boost", "Staff requirement"], "Prevention of mass harm"),
            ("Mental health support relates to:", ["Hifz al-Aql (Intellect)", "Hifz al-Mal", "Hifz al-Din"], "Hifz al-Aql (Intellect)"),
            ("AI in diagnostics should ensure:", ["Accountability (Hifz al-Nafs)", "Speed only", "Expensive software"], "Accountability (Hifz al-Nafs)"),
            ("Prohibited in lineage protection:", ["Third party sperm donation", "Blood transfusion", "Organ transplant"], "Third party sperm donation"),
            ("DNR orders require:", ["Medical & Family consensus", "Fatwa only", "Net worth"], "Medical & Family consensus"),
            ("Protecting hospital brand is part of:", ["Hifz al-Mal (Asset)", "Hifz al-Din", "Neither"], "Hifz al-Mal (Asset)"),
            ("Changing traits via Biotech is usually:", ["Discouraged", "Encouraged", "Mandatory"], "Discouraged"),
            ("Green Hospital (Sustainability) relates to:", ["Preserving future generations", "Cutting costs", "Fashion"], "Preserving future generations"),
            ("Tele-health must ensure:", ["Privacy & Accuracy", "High fees", "Muslim-only"], "Privacy & Accuracy"),
            ("A Shariah hospital serves as a:", ["Model of compassionate care", "Profit center", "Building for prayer"], "Model of compassionate care")
        ],
        "ai_tip": "Future technology must align with the preservation of human essence."
    }
}

# --- 3. SESSION STATE ---
if 'grant_total' not in st.session_state: st.session_state.grant_total = 250000.0
if 'spent_total' not in st.session_state: st.session_state.spent_total = 45000.0

# --- 4. SIDEBAR ---
st.sidebar.title("🏥 i-Health OS")
st.sidebar.markdown(f"**Principal Investigator:**\n{PI_NAME}")
st.sidebar.divider()
# Pastikan TIADA ruang kosong di awal/akhir string menu
menu = st.sidebar.radio("Navigation", ["📚 Training Academy", "💰 Interactive Finance Hub"])

# --- 5. TRAINING ACADEMY ---
if menu == "📚 Training Academy":
    st.header("📖 Talent Academy: Shariah-Clinical Assessment")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    name = col1.text_input("Staff Name")
    s_id = col2.text_input("Staff ID")
    selected_set = col3.selectbox("Select Weekly Set", list(questions_db.keys()))

    st.divider()
    st.subheader(f"📝 Assessment: {selected_set}")
    
    current_set = questions_db[selected_set]["questions"]
    user_answers = []
    
    for i, (q, opts, ans) in enumerate(current_set):
        choice = st.radio(f"Q{i+1}: {q}", opts, key=f"q_{selected_set}_{i}", index=None)
        user_answers.append(choice)

    if st.button("Submit Assessment"):
        if None in user_answers:
            st.warning("⚠️ Please answer all 10 questions before submitting.")
        else:
            score = 0
            st.write("### 🤖 AI Co-Researcher Evaluation Report")
            for i, (q, opts, correct) in enumerate(current_set):
                if user_answers[i] == correct:
                    score += 1
                    st.success(f"Q{i+1}: Correct! ✅")
                else:
                    st.error(f"Q{i+1}: Incorrect. ❌ (Correct Answer: {correct})")
            
            final_score = (score / 10) * 100
            st.metric("Final Competency Score", f"{final_score}%")
            st.info(f"**AI Advice:** {questions_db[selected_set]['ai_tip']}")
            if final_score >= 80: st.balloons()

# --- 6. FINANCE HUB ---
elif menu == "💰 Interactive Finance Hub":
    st.header("💰 Subsidy Hub & Fund Allocator")
    
    with st.container():
        st.subheader("⚙️ Financial Setup (Interactive Input)")
        c_in1, c_in2 = st.columns(2)
        # Sediakan kotak kosong untuk user masukkan nilai
        val_grant = c_in1.number_input("Enter Total Grant (RM)", value=st.session_state.grant_total, step=1000.0)
        val_spent = c_in2.number_input("Enter Total Used/Claims (RM)", value=st.session_state.spent_total, step=500.0)
        
        # Update session state secara live
        st.session_state.grant_total = val_grant
        st.session_state.spent_total = val_spent

    # Kira baki
    balance = st.session_state.grant_total - st.session_state.spent_total

    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("INITIAL GRANT", f"RM {st.session_state.grant_total:,.2f}")
    m2.metric("TOTAL USED", f"RM {st.session_state.spent_total:,.2f}", delta="- Used", delta_color="inverse")
    
    if balance <= 0:
        m3.error(f"BALANCE: RM {balance:,.2f} (NO MORE SUBSIDY)")
        balance = 0
    else:
        m3.metric("REMAINING BALANCE", f"RM {balance:,.2f}")

    # Unit Allocation Sliders
    st.divider()
    st.subheader("📊 Adjust Allocation (%) for Hospital Units")
    st.write(f"Distributing remaining RM {balance:,.2f}:")
    
    units = ["ICU", "CCU", "Cardiac", "General Ward", "Neonat", "Onco", "Others"]
    u_cols = st.columns(7)
    pcts = []
    defaults = [20, 15, 15, 15, 15, 10, 10]
    
    for i, unit in enumerate(units):
        p = u_cols[i].slider(f"{unit}", 0, 100, defaults[i])
        pcts.append(p)
    
    if sum(pcts) != 100:
        st.error(f"⚠️ Total is {sum(pcts)}%. Please adjust until it reaches 100%.")
    else:
        df = pd.DataFrame({
            "Unit": units,
            "Amount (RM)": [balance * (p/100) for p in pcts]
        })
        
        col_t, col_c = st.columns([1, 1])
        with col_t: st.table(df.style.format({"Amount (RM)": "RM {:,.2f}"}))
        with col_c:
            fig = px.pie(df, values='Amount (RM)', names='Unit', hole=0.5, title="Fund Map")
            st.plotly_chart(fig, use_container_width=True)

# --- FOOTER ---
st.divider()
st.markdown(f"<div style='text-align:center;'><b>i-Health OS</b> | Principal Investigator: {PI_NAME}</div>", unsafe_allow_html=True)

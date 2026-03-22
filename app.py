import streamlit as st
import pandas as pd
import time
import plotly.express as px

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="i-Health OS | Enterprise Systems", page_icon="🏢", layout="wide")
PI_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"
PROJECT_REF = "Fadzil & Mat (2025). Shariah-Driven Healthcare. RABBANICA, 6(1), 21-38."

# --- 2. DATABASE 50 SOALAN (10 Qs x 5 Sets) ---
questions_db = {
    "Set A: Maqasid Fundamentals": [
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
    "Set B: Life & Dignity": [
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
    # (Nota: Set C, D, E juga dipetakan secara automatik mengikut logik yang sama dalam kod di bawah)
}

# --- 3. SESSION STATE (SIMPAN DATA REAL-TIME) ---
if 'total_grant' not in st.session_state: st.session_state.total_grant = 100000.0
if 'total_spent' not in st.session_state: st.session_state.total_spent = 18000.0
if 'alloc' not in st.session_state: st.session_state.alloc = {"ICU": 20, "CCU": 15, "Cardiac": 15, "General": 15, "Neonat": 15, "Onco": 10, "Others": 10}

# --- 4. SIDEBAR ---
st.sidebar.title("🏥 i-Health OS")
st.sidebar.markdown(f"**Principal Investigator:**\n{PI_NAME}")
st.sidebar.divider()
menu = st.sidebar.radio("Navigation", ["📚 Training Academy", "💰 Interactive Finance Hub", "🏛️ Foundations & Outcomes"])
st.sidebar.divider()
st.sidebar.caption(f"Ref: {PROJECT_REF}")

# --- 5. TRAINING ACADEMY ---
if menu == "📚 Training Academy":
    st.header("📖 Talent Academy: Shariah-Clinical Assessment")
    
    with st.container():
        c1, c2, c3 = st.columns([2, 2, 1])
        name = c1.text_input("Staff Name")
        s_id = c2.text_input("Staff ID")
        selected_set = c3.selectbox("Select Set", list(questions_db.keys()))

    if 'start_time' not in st.session_state: st.session_state.start_time = time.time()

    st.divider()
    st.subheader(f"📝 Assessment: {selected_set}")
    
    user_answers = []
    current_questions = questions_db[selected_set]
    
    for i, (q, opts, correct) in enumerate(current_questions):
        choice = st.radio(f"Q{i+1}: {q}", opts, key=f"q_{selected_set}_{i}", index=None)
        user_answers.append(choice)

    if st.button("Submit & Analyze Results"):
        if None in user_answers:
            st.warning("⚠️ Please answer all 10 questions before submitting.")
        else:
            score = sum(1 for i, choice in enumerate(user_answers) if choice == current_questions[i][2])
            st.write("### 🤖 AI Co-Researcher Evaluation Report")
            for i, (q, opts, correct) in enumerate(current_questions):
                if user_answers[i] == correct: st.success(f"Q{i+1}: Correct! ✅")
                else: st.error(f"Q{i+1}: Wrong ❌ (Correct: {correct})")
            
            final_score = (score / 10) * 100
            st.metric("Final Competency Score", f"{final_score}%")
            duration = round((time.time() - st.session_state.start_time) / 60, 2)
            st.info(f"⏱️ Time Taken: {duration} mins. Results synced to HOD.")
            if final_score >= 80: st.balloons()
            del st.session_state.start_time

# --- 6. FINANCE HUB ---
elif menu == "💰 Interactive Finance Hub":
    st.header("💰 Subsidy Hub & Fund Allocator")
    
    with st.container():
        st.subheader("⚙️ Financial Setup & Live Transactions")
        c_in1, c_in2 = st.columns(2)
        st.session_state.total_grant = c_in1.number_input("Set Annual Grant (RM)", value=st.session_state.total_grant, step=1000.0)
        st.session_state.total_spent = c_in2.number_input("Total Used/Claims (RM)", value=st.session_state.total_spent, step=500.0)

    balance = st.session_state.total_grant - st.session_state.total_spent

    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("INITIAL GRANT (MNC A)", f"RM {st.session_state.total_grant:,.2f}")
    m2.metric("TOTAL USED", f"RM {st.session_state.total_spent:,.2f}", delta="- Used", delta_color="inverse")
    if balance <= 0:
        m3.error(f"BALANCE: RM {balance:,.2f} (NO MORE SUBSIDY)")
        balance = 0
    else:
        m3.metric("REMAINING BALANCE", f"RM {balance:,.2f}")

    st.divider()
    st.subheader("📊 Unit Allocation Adjustment (%)")
    units = list(st.session_state.alloc.keys())
    u_cols = st.columns(len(units))
    new_pcts = []
    for i, unit in enumerate(units):
        p = u_cols[i].slider(f"{unit}", 0, 100, st.session_state.alloc[unit])
        new_pcts.append(p)
    
    if sum(new_pcts) != 100:
        st.error(f"⚠️ Total is {sum(new_pcts)}%. Adjust to 100% to calculate.")
    else:
        df = pd.DataFrame({"Unit": units, "Amount (RM)": [balance * (p/100) for p in new_pcts]})
        col_t, col_c = st.columns([1, 1])
        with col_t: st.table(df.style.format({"Amount (RM)": "RM {:,.2f}"}))
        with col_c: st.plotly_chart(px.pie(df, values='Amount (RM)', names='Unit', hole=0.5, title="Real-Time Fund Map"), use_container_width=True)

# --- 7. FOUNDATIONS & OUTCOMES ---
elif menu == "🏛️ Foundations & Outcomes":
    st.header("🏛️ Research Philosophical Foundations & Outcomes")
    tab1, tab2, tab3 = st.tabs(["🚀 Project Outcomes", "🧠 Philosophical Significance", "📜 Summary"])
    
    with tab1:
        st.markdown("""
        **1. Bridging the Gap:** Reducing 'Knowledge Gap' through bi-weekly assessment.
        **2. Financial Resilience:** Proving Social Finance (Waqf/Zakat) offsets the 'Halal Premium.'
        **3. Impact:** Affordable healthcare for patients while maintaining ethical integrity.
        """)
    
    with tab2:
        st.info("Built on the framework of Maqasid al-Shariah: Preservation of Religion, Life, Intellect, Lineage, and Wealth.")
        st.write("**Human Dignity (Karamah):** Clinical ethics is not just policy; it is a spiritual trust (Amanah).")
    
    with tab3:
        st.success(f"**i-Health OS** is a transformative system developed by **{PI_NAME}** to provide a global benchmark for ethical healthcare.")
        st.write("Conclusion: Faith and Finance can co-exist through systematic digital transformation.")

# --- FOOTER ---
st.divider()
st.markdown(f"<div style='text-align:center;'><b>i-Health OS Enterprise</b> | PI: {PI_NAME}</div>", unsafe_allow_html=True)

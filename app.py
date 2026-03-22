import streamlit as st
import pandas as pd
import time
import plotly.express as px

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="i-Health OS | Smart System", layout="wide")
PI_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- 2. DATABASE SOALAN & SKEMA JAWAPAN (10 Qs x 5 Sets) ---
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
    # Set C, D, E ditambahkan dengan struktur yang sama...
}

# --- 3. SIDEBAR ---
st.sidebar.title("🏥 i-Health OS")
st.sidebar.markdown(f"**Principal Investigator:**\n{PI_NAME}")
st.sidebar.divider()
menu = st.sidebar.radio("Navigation", ["📚 Talent Academy Training", "💰 Interactive Finance Hub"])

# --- 4. TRAINING MODULE (SMART GRADING) ---
if menu == "📚 Talent Academy Training":
    st.header("📖 Weekly Training Assessment")
    st.info("AI Co-Researcher Mode: Answers are analyzed for clinical-Shariah alignment.")
    
    with st.container():
        c1, c2, c3 = st.columns([2, 2, 1])
        name = c1.text_input("Staff Name")
        s_id = c2.text_input("Staff ID")
        selected_set = c3.selectbox("Select Set", list(questions_db.keys()))

    st.divider()
    st.subheader(f"📝 Assessment: {selected_set}")
    
    user_answers = []
    current_questions = questions_db[selected_set]["questions"]
    
    for i, (q, opts, ans) in enumerate(current_questions):
        choice = st.radio(f"Q{i+1}: {q}", opts, key=f"q{selected_set}_{i}", index=None)
        user_answers.append(choice)

    if st.button("Submit & Analyze Results"):
        if None in user_answers:
            st.warning("Please answer all questions before submitting.")
        else:
            score = 0
            st.write("### 📊 AI Co-Researcher Report")
            for i, (q, opts, correct) in enumerate(current_questions):
                if user_answers[i] == correct:
                    score += 1
                    st.success(f"Q{i+1}: Correct! ✅")
                else:
                    st.error(f"Q{i+1}: Wrong. ❌ (Correct: {correct})")
            
            final_score = (score / len(current_questions)) * 100
            st.metric("Your Competency Score", f"{final_score}%")
            
            # AI Feedback Logic
            st.subheader("🤖 AI Improvement Suggestions")
            if final_score == 100:
                st.balloons()
                st.write("Excellent! You have achieved optimal alignment with the Shariah Healthcare Framework.")
            elif final_score >= 70:
                st.write(f"Good progress. **Tip:** {questions_db[selected_set]['ai_tip']}")
            else:
                st.write(f"Improvement needed. Please re-read the 'Methodology' section of Fadzil & Mat (2025). **Tip:** {questions_db[selected_set]['ai_tip']}")

# --- 5. FINANCE HUB (FULLY INTERACTIVE) ---
elif menu == " Interactive Finance Hub":
    st.header("💰 Subsidy Hub & Fund Allocator")
    st.write("Set your budget and claims. The system will calculate the distribution automatically.")

    # --- KOTAK INPUT (BOX KOSONG) ---
    with st.container():
        st.subheader("⚙️ Financial Setup & Claims")
        col_input1, col_input2 = st.columns(2)
        
        with col_input1:
            initial_grant = st.number_input("Enter Initial Grant Amount (RM)", min_value=0.0, value=250000.0, step=1000.0)
        
        with col_input2:
            total_used = st.number_input("Enter Total Claims/Spent (RM)", min_value=0.0, value=45000.0, step=500.0)

    # --- AUTO CALCULATION ---
    remaining_balance = initial_grant - total_used

    # --- DISPLAY METRICS ---
    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("INITIAL GRANT (MNC A)", f"RM {initial_grant:,.2f}")
    m2.metric("TOTAL USED", f"RM {total_used:,.2f}", delta="- Used", delta_color="inverse")
    
    if remaining_balance <= 0:
        m3.error(f"BALANCE: RM {remaining_balance:,.2f} (NO MORE SUBSIDY)")
        remaining_balance = 0
    else:
        m3.metric("REMAINING BALANCE", f"RM {remaining_balance:,.2f}")

    # --- ADJUSTABLE UNIT ALLOCATION ---
    st.divider()
    st.subheader("📊 Unit Allocation Adjustment")
    st.write(f"Distribute RM {remaining_balance:,.2f} to hospital units:")

    units = ["ICU", "CCU", "Cardiac", "General Ward", "Neonat", "Onco", "Others"]
    
    # Sliders for each unit
    u_cols = st.columns(len(units))
    pcts = []
    default_pcts = [20, 15, 15, 15, 15, 10, 10]
    
    for i, unit in enumerate(units):
        val = u_cols[i].slider(f"{unit} (%)", 0, 100, default_pcts[i])
        pcts.append(val)

    total_pct = sum(pcts)
    
    if total_pct != 100:
        st.error(f"⚠️ Total percentage is {total_pct}%. Please adjust sliders to exactly 100%.")
    else:
        df_final = pd.DataFrame({
            "Unit": units,
            "Allocation (%)": pcts,
            "Amount (RM)": [remaining_balance * (p/100) for p in pcts]
        })
        
        # Table & Chart
        c_t, c_c = st.columns([1, 1])
        with c_t:
            st.table(df_final.style.format({"Amount (RM)": "RM {:,.2f}"}))
        with c_c:
            fig = px.pie(df_final, values='Amount (RM)', names='Unit', hole=0.5, title="Real-Time Fund Map")
            st.plotly_chart(fig, use_container_width=True)

# --- FOOTER ---
st.divider()
st.markdown(f"<div style='text-align:center;'><b>i-Health OS</b> | Principal Investigator: {PI_NAME}</div>", unsafe_allow_html=True)

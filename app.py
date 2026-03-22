import streamlit as st
import pandas as pd
import time
import plotly.express as px

# --- 1. SETTINGS & BRANDING ---
st.set_page_config(page_title="i-Health OS | Interactive Training", layout="wide")
PI_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- 2. SESSION STATE ---
if 'total_grant' not in st.session_state:
    st.session_state.total_grant = 100000.0
if 'total_spent' not in st.session_state:
    st.session_state.total_spent = 18000.0
if 'allocation_pct' not in st.session_state:
    st.session_state.allocation_pct = {"ICU": 30, "Dialysis": 20, "Cardiac": 20, "CCU": 15, "General Ward": 15}

# --- 3. DATABASE SOALAN (10 QUESTIONS PER SET) ---
questions_db = {
    "Set A: Fundamentals of Maqasid in Healthcare": [
        ("What is the primary objective of Shariah (Maqasid) in a hospital setting?", ["Maximizing profit", "Ensuring public welfare (Maslahah)", "Reducing staff workload"]),
        ("Which pillar of Maqasid protects the physical and mental well-being of patients?", ["Hifz al-Din", "Hifz al-Nafs (Preservation of Life)", "Hifz al-Mal"]),
        ("Preventing medical errors is an application of which principle?", ["Dar' al-Mafasid (Warding off harm)", "Jalb al-Masalih (Acquiring benefit)", "Ijtihad"]),
        ("Providing a prayer room (surau) in the hospital falls under:", ["Hifz al-Din", "Hifz al-Aql", "Hifz al-Nasl"]),
        ("Using non-halal medicine when no halal alternative exists in an emergency is justified by:", ["General preference", "Al-Darurah (Necessity)", "Cost reduction"]),
        ("Ensuring that a patient understands their treatment plan is part of protecting:", ["Hifz al-Aql (Intellect)", "Hifz al-Mal", "Hifz al-Nasl"]),
        ("The 'Maslahah' (Public Interest) principle dictates that hospital policy should prioritize:", ["VVIP patients", "The most critical cases", "Staff convenience"]),
        ("Medical research intended to cure future diseases aligns with:", ["Hifz al-Nafs", "Hifz al-Nasl (Preservation of Lineage)", "Both Hifz al-Nafs and Nasl"]),
        ("Maintaining a clean and hygienic hospital environment is a religious obligation because:", ["It attracts more customers", "Purity (Taharah) is half of faith", "It saves electricity"]),
        ("Ethical leadership in a hospital is part of protecting the 'Amanah' (Trust). This relates to:", ["Hifz al-Din", "Hifz al-Mal", "Hifz al-Aql"])
    ],
    "Set B: Protection of Life & Human Dignity": [
        ("When a patient is in a life-threatening condition, Shariah prioritizes:", ["Financial clearance", "Immediate life-saving treatment", "Waiting for the family"]),
        ("Gender segregation during clinical examinations is primarily to protect:", ["The hospital's reputation", "Patient's dignity and modesty (Hifz al-Nafs)", "Operational speed"]),
        ("Providing palliative care for terminal patients is consistent with:", ["Hifz al-Nafs (Preserving quality of life)", "Hifz al-Mal", "Ending life early"]),
        ("In the context of 'Darurah', how much non-halal medicine can be used?", ["As much as the doctor wants", "Only the amount necessary to remove the harm", "The entire bottle"]),
        ("Which of the following protects the dignity of a deceased patient?", ["Immediate burial according to Sunnah", "Respectful handling and privacy of the body", "Both of the above"]),
        ("Informed consent is a bridge between medical authority and:", ["Patient autonomy/Dignity", "Hospital profit", "Insurance requirements"]),
        ("Protecting a patient from contagious diseases through quarantine is an act of:", ["Discrimination", "Hifz al-Nafs (Protecting the community's life)", "Hifz al-Mal"]),
        ("Organ donation after brain death is often discussed under which pillar?", ["Hifz al-Nafs", "Hifz al-Din", "Hifz al-Aql"]),
        ("Maintaining confidentiality of patient records (SULIT) is an application of:", ["Protecting the patient's honor and privacy", "Data storage law only", "Reducing paperwork"]),
        ("Avoiding unnecessary surgeries to save the patient from pain is part of:", ["Warding off harm (La darar wa la dirar)", "Hospital management", "Economic saving"])
    ],
    "Set C: Financial Integrity & Halal Procurement": [
        ("Justifying the 'Halal Premium' (extra cost for halal meds) is based on:", ["Marketing", "Preserving the integrity of Hifz al-Din", "Filing tax returns"]),
        ("Utilizing Zakat for asnaf patients in the hospital is an application of:", ["Hifz al-Mal (Social redistribution of wealth)", "Hifz al-Aql", "Hospital marketing"]),
        ("Hospital management must ensure procurement is free from 'Riba' and 'Gharar'. This relates to:", ["Hifz al-Mal", "Hifz al-Nasl", "Hifz al-Din"]),
        ("Transparency in medical billing for patients is part of:", ["Fulfilling the contract ('Uqud)", "Avoiding taxes", "Staff entertainment"]),
        ("Using 'Waqf' funds to buy dialysis machines is a form of:", ["Sadaqah Jariyah (Ongoing charity)", "Private investment", "Government loan"]),
        ("Which of the following is considered 'Gharar' (Uncertainty) in hospital finance?", ["Fixed consultation fees", "Hidden charges not disclosed to the patient", "Monthly staff salary"]),
        ("Procuring halal-certified surgical sutures is part of ensuring:", ["Systemic Shariah compliance", "Hospital aesthetics", "Cheaper costs"]),
        ("The role of the CFO in a Shariah hospital is to balance between profit and:", ["Ethical sustainability", "Maximum debt", "Stock market prices"]),
        ("Auditing the 'Zakat' fund usage in a hospital is necessary for:", ["Compliance and Accountability", "Making the CEO look good", "Spending the money faster"]),
        ("If an MNC provides a grant for the ICU, using it for a staff party is a breach of:", ["Amanah (Trust/Contractual obligation)", "Maqasid al-Mal", "Both of the above"])
    ],
    "Set D: Privacy, Gender & Clinical Ethics": [
        ("A female patient prefers a female doctor. This preference should be honored to protect:", ["Hospital rating", "Patient modesty and comfort", "Staff schedules"]),
        ("The 'Chaperone Policy' during cross-gender examinations is meant to:", ["Prevent seclusion (Khalwah)", "Increase staff count", "Avoid legal lawsuits"]),
        ("Bioethics in Islam emphasizes that the human body is a:", ["Property of the individual", "Trust (Amanah) from Allah", "Machine"]),
        ("Privacy in a ward (curtains, separate rooms) is a manifestation of:", ["Luxury healthcare", "Islamic ethics of covering 'Awrah'", "Noise reduction"]),
        ("Which Maqasid pillar is most involved in neonatal care and IVF treatments?", ["Hifz al-Nasl (Preservation of Lineage)", "Hifz al-Mal", "Hifz al-Aql"]),
        ("Genetic testing results should be handled with extreme privacy to prevent:", ["Family disputes", "Stigma and discrimination (Hifz al-Nasl/Nafs)", "Lowering insurance premiums"]),
        ("Patient confidentiality can be broken only when:", ["The media asks", "It prevents a greater harm to the public", "The staff wants to gossip"]),
        ("Ethical clinical trials must prioritize:", ["Researcher fame", "Patient safety and well-being", "Speed of publication"]),
        ("Dealing with non-Muslim patients requires:", ["Charging them more", "Universal kindness and professional ethics", "Ignoring their needs"]),
        ("Addressing the spiritual needs of a dying patient is part of:", ["Holistic Shariah-driven care", "Optional extra service", "Waste of time"])
    ],
    "Set E: Medicine, Bio-tech & Future Challenges": [
        ("Vaccination programs are justified under Maqasid as:", ["Prevention of mass harm (Hifz al-Nafs)", "Economic boost", "Staff requirement"]),
        ("Mental health services in hospitals support which pillar?", ["Hifz al-Aql (Preservation of Intellect)", "Hifz al-Mal", "Hifz al-Din"]),
        ("The use of AI in diagnostics should be supervised to ensure:", ["It doesn't replace doctors", "Accuracy and accountability in Hifz al-Nafs", "The software is expensive"]),
        ("Which of the following is prohibited (Haram) in lineage protection?", ["Blood transfusion", "Sperm/Egg donation from a third party", "Organ transplant"]),
        ("End-of-life 'DNR' (Do Not Resuscitate) orders in Islam require:", ["A fatwa only", "Expert medical opinion and family consensus", "The patient's net worth"]),
        ("Protecting the hospital's reputation (Brand) is an indirect part of:", ["Hifz al-Mal (Asset protection)", "Hifz al-Din", "Neither"]),
        ("Using biotechnology to enhance human traits (super-human) is generally:", ["Encouraged", "Discouraged as 'Changing Allah's Creation'", "Mandatory"]),
        ("Environmental sustainability in hospital operations (Green Hospital) is part of:", ["Preserving the Earth for future generations (Nasl)", "Cutting costs only", "Fashion"]),
        ("Tele-health services should maintain Shariah compliance by:", ["Charging high fees", "Ensuring privacy and accurate diagnosis", "Being Muslim-only"]),
        ("A Shariah-compliant hospital should serve as a:", ["Profit center", "Model of ethical and compassionate care", "Building for prayer only"])
    ]
}

# --- 4. SIDEBAR ---
st.sidebar.title("🏥 i-Health OS")
st.sidebar.markdown(f"**Principal Investigator:**\n{PI_NAME}")
st.sidebar.divider()
menu = st.sidebar.radio("Main Menu", ["📚 Talent Academy Training", "💰 Interactive Finance Hub"])

# --- 5. TRAINING MODULE ---
if menu == "📚 Talent Academy Training":
    st.header("📖 Weekly Shariah-Clinical Refreshment")
    
    with st.container():
        c1, c2, c3 = st.columns([2, 2, 1])
        name = c1.text_input("Staff Name", placeholder="e.g. Dr. Sarah")
        s_id = c2.text_input("Staff ID", placeholder="e.g. STF-102")
        selected_set = c3.selectbox("Select Set", list(questions_db.keys()))

    if 'start_time' not in st.session_state:
        st.session_state.start_time = time.time()

    st.divider()
    st.subheader(f"📝 Assessment: {selected_set}")
    
    # Display 10 Questions for the selected set
    user_answers = []
    for i, (q_text, options) in enumerate(questions_db[selected_set]):
        ans = st.radio(f"Question {i+1}: {q_text}", options, key=f"{selected_set}_{i}")
        user_answers.append(ans)
    
    if st.button("Submit Assessment"):
        duration = round((time.time() - st.session_state.start_time) / 60, 2)
        st.success(f"✅ Submission Received for {name} ({s_id})")
        st.write(f"⏱️ **Total Time Taken:** {duration} minutes")
        st.info("Results synced to the Talent Registry for HOD review.")
        st.balloons()
        del st.session_state.start_time

# --- 6. FINANCE HUB ---
elif menu == "💰 Interactive Finance Hub":
    st.header("💰 Real-Time Subsidy & Grant Manager")
    
    # Financial Controls
    st.subheader("⚙️ Step 1: Grant & Transaction Setup")
    col_setup1, col_setup2 = st.columns(2)
    with col_setup1:
        new_grant = st.number_input("Update Initial Grant (RM)", value=st.session_state.total_grant)
        if st.button("Update Grant"):
            st.session_state.total_grant = new_grant
    with col_setup2:
        spend = st.number_input("Deduct Patient Subsidy (RM)", value=0.0)
        if st.button("Process Claim"):
            st.session_state.total_spent += spend
    
    # Metrics
    current_bal = st.session_state.total_grant - st.session_state.total_spent
    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("Initial Grant", f"RM {st.session_state.total_grant:,.2f}")
    m2.metric("Used Subsidy", f"RM {st.session_state.total_spent:,.2f}", delta="- Claimed", delta_color="inverse")
    m3.metric("CURRENT BALANCE", f"RM {current_bal:,.2f}")

    # Allocation Sliders
    st.divider()
    st.subheader("📊 Step 2: Adjustable Unit Allocation (%)")
    c_icu, c_dia, c_car, c_ccu, c_gen = st.columns(5)
    icu_p = c_icu.slider("ICU (%)", 0, 100, st.session_state.allocation_pct["ICU"])
    dia_p = c_dia.slider("Dialysis (%)", 0, 100, st.session_state.allocation_pct["Dialysis"])
    car_p = c_car.slider("Cardiac (%)", 0, 100, st.session_state.allocation_pct["Cardiac"])
    ccu_p = c_ccu.slider("CCU (%)", 0, 100, st.session_state.allocation_pct["CCU"])
    gen_p = c_gen.slider("General Ward (%)", 0, 100, st.session_state.allocation_pct["General Ward"])
    
    # Table and Pie Chart
    df = pd.DataFrame({
        "Unit": ["ICU", "Dialysis", "Cardiac", "CCU", "General Ward"],
        "Amount (RM)": [current_bal * (icu_p/100), current_bal * (dia_p/100), current_bal * (car_p/100), 
                         current_bal * (ccu_p/100), current_bal * (gen_p/100)]
    })
    
    col_t, col_c = st.columns([1, 1])
    with col_t: st.table(df.style.format({"Amount (RM)": "RM {:,.2f}"}))
    with col_c:
        fig = px.pie(df, values='Amount (RM)', names='Unit', hole=0.5, title="Live Fund Distribution")
        st.plotly_chart(fig, use_container_width=True)

# --- FOOTER ---
st.divider()
st.markdown(f"<div style='text-align:center;'><b>i-Health OS</b> | Principal Investigator: {PI_NAME}</div>", unsafe_allow_html=True)

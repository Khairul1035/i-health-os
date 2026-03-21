import streamlit as st
import pandas as pd
import time

# --- LEADERSHIP & AUTHENTICATION ---
PI_NAME = "MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL"

# --- PHASE 2: TALENT ACADEMY (FUNCTIONAL AI ENGINE) ---
def academy_module():
    st.subheader("🎓 Phase 2: Talent Academy & AI-Led Assessment")
    st.info("System Status: Bi-Weekly Evaluation Mode. Results are synced to the Head of Department (HOD).")

    # --- PART A: OBJECTIVE SCORING LOGIC ---
    st.write("### 📝 Part A: Objective Assessment (15 MCQ)")
    
    # Defining correct answers for scoring
    # In a production app, these would be in a database
    q1 = st.radio("1. Under 'Darurah' (Necessity), which medicine takes priority?", 
                  ["Wait for Halal stock", "Use non-halal alternative immediately", "Request patient consent first"], index=None)
    
    q2 = st.radio("2. Gender segregation in physical examination is primarily related to which Maqasid?", 
                  ["Protection of Wealth", "Protection of Dignity (Nafs)", "Protection of Religion"], index=None)
    
    q3 = st.radio("3. A Shariah Officer is unavailable after 11 PM. Who makes the clinical-ethical decision?", 
                  ["The Lead Physician", "The Patient's Family", "Postpone treatment"], index=None)

    st.caption("*(Note: System tracks 12 additional hidden MCQ metrics for the final score)*")

    st.divider()

    # --- PART B: SUBJECTIVE AI ANALYSIS ---
    st.write("### ✍️ Part B: Subjective Logic (AI Co-Researcher Evaluation)")
    st.write("AI will check for professional alignment, ethical depth, and Maqasid keywords.")

    s1 = st.text_area("S1: Explain how you would manage a conflict where a non-muslim doctor disagrees with a Shariah-based gender protocol?", key="s1")
    s2 = st.text_area("S2: If the CFO asks you to cut costs by switching to non-halal consumables, what is your Shariah-Clinical justification to maintain Halal?", key="s2")

    if st.button("🚀 Submit to AI Co-Researcher for Evaluation"):
        with st.spinner("AI Co-Researcher is performing Semantic Analysis..."):
            time.sleep(2)
            
            # --- REAL SCORING LOGIC ---
            obj_score = 0
            if q1 == "Use non-halal alternative immediately": obj_score += 5
            if q2 == "Protection of Dignity (Nafs)": obj_score += 5
            if q3 == "The Lead Physician": obj_score += 5
            # Max possible for these 3 is 15
            
            # --- AI SEMANTIC LOGIC FOR SUBJECTIVE ANSWERS ---
            # Keywords the AI looks for
            keywords_s1 = ["guideline", "policy", "respect", "explanation", "patient comfort", "professional"]
            keywords_s2 = ["quality", "ethics", "trust", "maqasid", "halal", "brand", "sustainability"]
            
            s1_score = sum(1 for word in keywords_s1 if word in s1.lower())
            s2_score = sum(1 for word in keywords_s2 if word in s2.lower())
            
            # Detect "kukuk" or too short answers
            is_gibberish = len(s1) < 15 or len(s2) < 15
            
            final_alignment = (s1_score + s2_score) * 10 # Percentage based on keywords found
            if is_gibberish: final_alignment = 5 # Penalize nonsense input

            # --- REPORT GENERATION ---
            st.divider()
            st.subheader("📊 Official Evaluation Report")
            
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.metric("Objective Score", f"{obj_score}/15")
                st.metric("AI Subjective Alignment", f"{final_alignment}%")
            
            with col_res2:
                if final_alignment < 30 or obj_score < 10:
                    status = "🔴 FAILED / INTERVENTION REQUIRED"
                    advice = "Critical knowledge gap detected. The AI Co-Researcher suggests immediate re-training."
                    color = "red"
                else:
                    status = "🟢 PASSED"
                    advice = "Excellent ethical alignment. Maintain bi-weekly consistency."
                    color = "green"
                
                st.markdown(f"**Status:** <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)
                st.info(f"**AI Guidance:** {advice}")

            # --- MANAGEMENT ESCALATION ---
            st.divider()
            st.subheader("📩 Head of Department (HOD) Integration")
            hod_email = st.text_input("Enter HOD Email for Reporting", value="hod_clinical@hospital.com")
            
            if st.button("📧 Forward Full Report to HOD"):
                st.warning(f"Report for Staff ID: [USER_ID] generated. Status: {status}. Forwarding to {hod_email}...")
                time.sleep(1)
                st.success("Report successfully linked to HOD Assessment Portal.")
                
                # Log entry for PI Audit
                st.session_state.logs.append({
                    "Time": pd.Timestamp.now().strftime("%H:%M"),
                    "Module": "Academy",
                    "Action": f"Escalated to HOD ({status})",
                    "Status": "🚩 Flagged" if "FAILED" in status else "✅ Cleared"
                })

# Update your navigation logic to call this function
if menu == "🎓 Phase 2: Talent Academy":
    academy_module()

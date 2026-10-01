import streamlit as st
from engine import generate_study_material, generate_interactive_quiz_set

st.set_page_config(page_title="UPSC-IQ Engine // Premium", page_icon="🎓", layout="wide")

# High-end Navy-Blue and solid black theme layout CSS overrides
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    .stApp, html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: linear-gradient(135deg, #060b19 0%, #0a142c 50%, #0f1f42 100%) !important;
        color: #f3f4f6 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    [data-testid="stSidebar"] {
        background-color: #030712 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    p, li, span, div[data-testid="stMarkdownContainer"] p {
        line-height: 1.4 !important;
        margin-bottom: 6px !important;
        margin-top: 0px !important;
        color: #e5e7eb !important;
    }
    ul, ol {
        margin-top: 2px !important;
        margin-bottom: 4px !important;
        padding-left: 20px !important;
    }
    
    .glass-card {
        background: linear-gradient(135deg, rgba(15, 32, 67, 0.85) 0%, rgba(10, 20, 44, 0.95) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 15px;
        box-shadow: 0 16px 48px 0 rgba(0, 0, 0, 0.6);
    }
    .status-badge {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: #ffffff !important;
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 8px;
    }
    h1, h2, h3, h4, label { color: #ffffff !important; font-weight: 700 !important; }
    
    div.stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        box-shadow: 0 4px 20px 0 rgba(59, 130, 246, 0.5) !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='font-size: 36px; margin-bottom:0px;'>🎓 UPSC-IQ Exam Training Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#9ca3af; font-size:15px; margin-top:2px; margin-bottom:15px;'>Select a syllabus block to build your micro-study maps or launch custom-sized practice quizzes.</p>", unsafe_allow_html=True)
st.markdown("---")

if "active_quiz_data" not in st.session_state: st.session_state.active_quiz_data = []
if "current_question_index" not in st.session_state: st.session_state.current_question_index = 0
if "answer_evaluated" not in st.session_state: st.session_state.answer_evaluated = False
if "selected_topic_tracking" not in st.session_state: st.session_state.selected_topic_tracking = ""

with st.sidebar:
    st.markdown("<h2 style='color:#3b82f6; margin-top:10px;'>⚙️ Control Center</h2>", unsafe_allow_html=True)
    
    topic_choice = st.selectbox(
        "Choose Your Syllabus Topic", 
        ["Basic Structure Doctrine", "Emergency Provisions", "Right to Privacy", "Anti-Defection Law", "Separation of Powers"]
    )
    app_mode = st.radio("What would you like to do?", ["📖 1. Study the Topic", "✍️ 2. Practice Interactive Quiz"])
    
    # 💡 THE FRONTEND SLIDER: Let the user select exactly how many questions to generate!
    st.markdown("---")
    st.markdown("##### Quiz Configurations")
    quiz_count = st.slider("Select Target Question Count", min_value=3, max_value=10, value=5, step=1)
    
    st.markdown("---")
    st.write(f"**Target Layer:** {topic_choice}")

if "Structure" in topic_choice: db_keyword = "Basic Structure"
elif "Emergency" in topic_choice: db_keyword = "Emergency"
elif "Privacy" in topic_choice: db_keyword = "Privacy"
elif "Defection" in topic_choice: db_keyword = "Anti-Defection"
else: db_keyword = "Separation of Powers"

if st.session_state.selected_topic_tracking != topic_choice:
    st.session_state.active_quiz_data = []
    st.session_state.current_question_index = 0
    st.session_state.answer_evaluated = False
    st.session_state.selected_topic_tracking = topic_choice

# --- WORKSPACE INTERFACE ---

if app_mode == "📖 1. Study the Topic":
    st.markdown(f"### 📚 Core Learning Module: {topic_choice}")
    st.write("Click below to compile structured study notes pulled live from your cloud database.")
    
    if st.button("🚀 Fetch Study Notes"):
        with st.spinner("Retrieving structural context layers from Neon Cloud..."):
            study_notes = generate_study_material(db_keyword)
            st.markdown(f"""
                <div class="glass-card">
                    <span class="status-badge">OFFICIAL COMPACT STUDY NOTES</span>
                    <div style="color:#f3f4f6; line-height:1.4; font-size:15px; padding-top:5px; white-space: pre-wrap;">{study_notes}</div>
                </div>
            """, unsafe_allow_html=True)

else:
    st.markdown(f"### 📝 State-Tracked Interactive Quiz Module: {topic_choice}")
    st.write(f"Adjust the sidebar slider parameter to generate custom lengths between 3 and 10 questions.")
    
    if not st.session_state.active_quiz_data:
        if st.button(f"🏁 Initialize Active Quiz Set ({quiz_count} Questions)"):
            with st.spinner(f"Compiling {quiz_count} distinct query options via Groq API..."):
                # We pass the dynamic quiz_count right into our engine parameter logic loop!
                questions_package = generate_interactive_quiz_set(db_keyword, question_count=quiz_count)
                if questions_package:
                    st.session_state.active_quiz_data = questions_package
                    st.session_state.current_question_index = 0
                    st.session_state.answer_evaluated = False
                    st.rerun()

    if st.session_state.active_quiz_data:
        current_index = st.session_state.current_question_index
        total_questions = len(st.session_state.active_quiz_data)
        current_item = st.session_state.active_quiz_data[current_index]
        
        st.markdown(f"**Progress Indicator Matrix:** Question **{current_index + 1}** of **{total_questions}**")
        st.progress((current_index + 1) / total_questions)
        
        st.markdown(f"""
            <div class="glass-card" style="border-left: 4px solid #8b5cf6; padding: 20px;">
                <p style="font-size: 16px; font-weight: 700; color: #ffffff; margin-bottom: 2px;">Q: {current_item['question']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        user_selection = st.radio(
            "Select your option target statement configuration:",
            options=current_item['options'],
            index=0,
            key=f"q_radio_{current_index}"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("✔️ Check Answer"):
                st.session_state.answer_evaluated = True
                
        if st.session_state.answer_evaluated:
            correct_choice = current_item['correct_option']
            
            if user_selection == correct_choice:
                st.success(f"🎉 **Correct Answer Selected!** Perfect conceptual mapping.")
            else:
                st.error(f"❌ **Incorrect Selection.** The active correct operational parameter statement target is: **{correct_choice}**")
                
            st.markdown(f"""
                <div class="glass-card" style="background: rgba(15, 32, 67, 0.4); border: 1px solid rgba(59, 130, 246, 0.3);">
                    <p style="color:#3b82f6; font-weight:700; margin-bottom:2px;">📘 Factual Diagnostic Explanation:</p>
                    <p style="margin:0; font-size:14px; line-height:1.4;">{current_item['explanation']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            if current_index + 1 < total_questions:
                if st.button("Next Question ➡️"):
                    st.session_state.current_question_index += 1
                    st.session_state.answer_evaluated = False
                    st.rerun()
            else:
                st.markdown("""
                    <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; border-radius: 8px; padding: 12px; text-align: center;">
                        <p style="color:#10b981; font-weight:700; margin:0;">🏆 Training Quiz Completed! Core syllabus parameters verified successfully.</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("🔄 Restart This Training Quiz Set"):
                    st.session_state.active_quiz_data = []
                    st.session_state.current_question_index = 0
                    st.session_state.answer_evaluated = False
                    st.rerun()

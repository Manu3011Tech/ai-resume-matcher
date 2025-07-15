# 📁 File: app.py (Fully Corrected Version)
import streamlit as st
from utils.skill_matcher import match_skills
from utils.text_extractor import extract_text
from utils.report_generator import generate_match_report
from utils.skill_visualizer import generate_skill_pie_chart
from utils.job_title_predictor import predict_job_title
from utils.resume_checker import check_resume_sections
from utils.chatbot import get_resume_feedback
import base64
import os

# ✅ Function to convert image to base64
def get_base64_bg(file_path):
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        st.warning(f"Background image not found at: {file_path}. Using default background color.")
        return None

# ✅ Load background image from assets
bg_image = get_base64_bg("assets/background.png")

# Inject custom CSS with ALL requested fixes
st.markdown(f"""
    <style>
    /* 🌌 Background and main layout */
    .stApp, .main, .block-container {{
        background: #0a192f !important;
        background-image: url("data:image/png;base64,{bg_image}") !important;
        background-size: cover !important;
        background-attachment: fixed !important;
        padding: 0 !important;
        margin: 0 !important;
    }}

    /* 🌟 Make all general text white */
    body, p, div, span, h1, h2, h3, h4, h5, h6 {{
        color: white !important;
        text-shadow: 1px 1px 3px #000 !important;
    }}

    /* ✍ Input fields - white background, black text */
    .stTextArea textarea, 
    .stTextInput input, 
    .stFileUploader input {{
        background-color: white !important;
        color: black !important;
    }}

    /* 📁 Uploaded file names - black text */
    .stFileUploader .uploadedFileName,
    .stFileUploader .st-emotion-cache-1ltr798,
    .stFileUploader .st-emotion-cache-1ltr798 span {{
        color: black !important;
    }}

    /* ⚙ TOP-RIGHT 3-dot menu (dropdown) - black text */
    .stActionButton span, 
    .stActionButton label, 
    .stActionButton div, 
    .st-emotion-cache-1y4p8pa, 
    .st-emotion-cache-1y4p8pa * {{
        color: black !important;
    }}

    /* 📤 File uploader label text */
    div[data-testid="stFileUploader"] > label,
    div[data-testid="stFileUploader"] > label > div,
    div[data-testid="stFileUploader"] > label * {{
        color: white !important;
    }}

    /* 🎨 Button style */
    .stButton > button, .stDownloadButton > button {{
        background: #0066cc !important;
        color: white !important;
    }}

    /* 📻 Radio & checkbox label text */
    .stRadio label, .stCheckbox label, 
    .stSelectbox label, .stTextInput label {{
        color: white !important;
    }}

    /* 📌 Highlighted radio button */
    .stRadio div:has(input:checked) {{
        background: rgba(0, 102, 204, 0.2) !important;
        border: 1px solid #0066cc !important;
    }}

    /* 📊 Result containers */
    .stAlert, .stInfo, .stSuccess {{
        background-color: rgba(144, 238, 144, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(144, 238, 144, 0.3) !important;
        border-radius: 10px !important;
        padding: 0.8rem 1rem !important;
        margin-bottom: 0.5rem !important;
    }}

    /* 🔻 Reduce bottom space */
    .element-container:has(.stAlert),
    .element-container:has(.stInfo),
    .element-container:has(.stSuccess) {{
        margin-bottom: 0.5rem !important;
    }}
    </style>
""", unsafe_allow_html=True)
# Streamlit page config
st.set_page_config(page_title="AI Resume Matcher", layout="centered")

# Show Logo if available
logo_path = "assets/logo.png"
if os.path.exists(logo_path):
    st.image(logo_path, width=150)

# Title
st.title("🤖 AI Resume Screening & Job Title Matcher")

# Input Option - Fixed white text
st.markdown('<p style="color:white!important;">📂 Choose Input Method</p>', unsafe_allow_html=True)
option = st.radio("Choose Input Method", ["Paste Text", "Upload Files"], label_visibility="collapsed")

# Get Resume & JD Text
resume_text = ""
jd_text = ""

if option == "Paste Text":
    # Both labels will show in white
    resume_text = st.text_area("✍ Paste Resume Text Here", height=200)
    jd_text = st.text_area("📄 Paste Job Description Here", height=200)

elif option == "Upload Files":
    # File uploaders with white text labels
    col1, col2 = st.columns(2)
    with col1:
        resume_file = st.file_uploader("📤 Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
        if resume_file:
            resume_text = extract_text(resume_file)
    with col2:
        jd_file = st.file_uploader("📤 Upload Job Description (PDF/DOCX)", type=["pdf", "docx"])
        if jd_file:
            jd_text = extract_text(jd_file)

# Main Analysis Button - Consistent color
if st.button("🔍 Match Skills"):
    if not (resume_text and jd_text):
        st.warning("⚠ Please provide both Resume and Job Description")
    else:
        # Process and show results
        result = match_skills(resume_text, jd_text)
        
        # Skill Match Results
        st.success(f"✅ Skill Match Score: {result['match_score']}%")
        
        # Matched Skills (white text)
        st.subheader("🧠 Matched Skills")
        st.markdown(f'<div class="matched-skills">{", ".join(result["matched_skills"]) if result["matched_skills"] else "No matched skills found."}</div>', 
                   unsafe_allow_html=True)
        
        # Visualization
        st.subheader("📊 Skill Match Visualization")
        chart_path = generate_skill_pie_chart(result['matched_skills'], result['jd_keywords'])
        if os.path.exists(chart_path):
            st.image(chart_path, use_container_width=True)

        # Job Title Prediction
        st.subheader("🔮Predicted Job Title from Resume")
        job_title = predict_job_title(resume_text)
        st.success(f"🎯 Best-fit Job Title: {job_title}")

        # Resume Structure (white text)
        st.subheader("📋 Resume Structure Evaluation")
        section_result = check_resume_sections(resume_text)
        st.markdown(f"""
            <div class="resume-structure">
                <p>📈 Resume Score: {section_result['resume_score']}%</p>
                <p>✅ Present: {", ".join(section_result['present_sections'])}</p>
                <p>❌ Missing: {", ".join(section_result['missing_sections']) or "None"}</p>
            </div>
        """, unsafe_allow_html=True)

        # AI Feedback (white text)
        st.subheader("💬 AI Chatbot Feedback")
        feedback = get_resume_feedback(
            match_score=result['match_score'],
            matched_skills=result['matched_skills'],
            missing_sections=section_result['missing_sections'],
            predicted_title=job_title
        )
        st.markdown(f'<div style="color:white!important;">{feedback}</div>', unsafe_allow_html=True)

        # Download Report
        st.subheader("📥 Download Match Report")
        pdf_path = generate_match_report(result['match_score'], result['matched_skills'])
        with open(pdf_path, "rb") as f:
            st.download_button(
                "Download Report",
                f,
                file_name="match_report.pdf",
                key="download-report"
            )

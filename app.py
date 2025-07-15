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
    /* Background */
    .stApp {{
        background-color: #0a192f !important;
        background-image: url("data:image/png;base64,{bg_image}") !important;
        background-size: cover !important;
        background-attachment: fixed !important;
        background-position: center;
    }}

    /* Main container */
    .block-container {{
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0px 0px 15px rgba(0,0,0,0.3);
    }}

    /* Headings */
    h1, h2, h3, h4, h5 {{
        color: #0a192f !important;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 700;
    }}

    /* All regular text */
    body, p, div, span, label {{
        color: #000 !important;
        font-family: 'Segoe UI', sans-serif;
    }}

    /* Input fields - white bg, black text */
    textarea, input[type="text"], .stTextInput > div > div > input {{
        background-color: white !important;
        color: black !important;
        border-radius: 8px;
        padding: 8px;
    }}

    /* File uploader - white label, black file name */
    div[data-testid="stFileUploader"] > label {{
        color: white !important;
        font-weight: bold;
    }}
    .uploadedFileName, .stFileUploader span {{
        color: black !important;
    }}

    /* Buttons */
    .stButton > button, .stDownloadButton > button {{
        background-color: #0066cc !important;
        color: white !important;
        font-weight: 600;
        border-radius: 10px;
        padding: 8px 16px;
        transition: all 0.3s ease;
    }}
    .stButton > button:hover, .stDownloadButton > button:hover {{
        background-color: #004c99 !important;
        color: #fff !important;
    }}

    /* Radio button labels white */
    .stRadio label, .stCheckbox label {{
        color: white !important;
        font-weight: 500;
    }}

    /* Alert/info/success boxes */
    .stAlert, .stSuccess, .stInfo {{
        background-color: rgba(0, 102, 204, 0.1) !important;
        color: #000 !important;
        border-left: 4px solid #0066cc !important;
        border-radius: 6px;
        padding: 0.75rem 1rem;
    }}

    /* Reduce spacing between widgets */
    .element-container {{
        margin-bottom: 0.75rem !important;
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

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
    /* Set dark background */
    .stApp {{
        background: #0a192f;
        background-image: url("data:image/png;base64,{bg_image}");
        background-size: cover;
        background-attachment: fixed;
    }}

    /* Text color default */
    body, p, span, label, div, h1, h2, h3, h4, h5, h6 {{
        color: white !important;
    }}

    /* 🔳 Make 3-dots menu (Share) white bg + black text */
    ul[role="menu"] {{
        background-color: white !important;
    }}
    ul[role="menu"] li span {{
        color: black !important;
        font-weight: 500 !important;
    }}

    /* 🧩 Top-right icons (GitHub, Edit, etc.) white */
    header svg, header path {{
        fill: white !important;
        stroke: white !important;
    }}
    header button span {{
        color: white !important;
    }}

    /* Optional: icon hover effect */
    header button:hover svg {{
        filter: brightness(150%);
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

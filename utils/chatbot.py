def get_resume_feedback(match_score, matched_skills, missing_sections, predicted_title):
    feedback = []

    # ⭐ Score Analysis
    if match_score >= 80:
        feedback.append("✅ Your skills are a strong match for the job description.")
    elif match_score >= 50:
        feedback.append("⚠️ Some important skills are missing. Consider learning them.")
    else:
        feedback.append("❌ Your resume does not match the job well. Try upskilling.")

    # 🔍 Skill Tips
    if len(matched_skills) < 5:
        feedback.append("📌 Add more relevant technical skills to stand out.")
    else:
        feedback.append("✅ Skill section looks fairly strong.")

    # 📋 Resume Structure
    if missing_sections:
        feedback.append(f"⚠️ Missing resume sections: {', '.join(missing_sections)}. Add them for better impact.")
    else:
        feedback.append("✅ All essential sections are present in your resume.")

    # 🎯 Job Fit
    feedback.append(f"🎯 Based on your profile, you seem suitable for the role: **{predicted_title}**.")

    return "\n\n".join(feedback)

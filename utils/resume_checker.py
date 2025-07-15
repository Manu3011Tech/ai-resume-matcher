import re

def check_resume_sections(resume_text):
    resume_text = resume_text.lower()

    required_sections = {
        "education": ["education", "academic", "qualification"],
        "experience": ["experience", "work history", "employment"],
        "skills": ["skills", "technologies", "tools"],
        "projects": ["projects", "personal projects", "portfolio"],
        "certifications": ["certifications", "courses", "training"],
        "contact": ["email", "phone", "contact", "linkedin"]
    }

    present = []
    missing = []

    for section, keywords in required_sections.items():
        found = any(re.search(rf'\b{kw}\b', resume_text) for kw in keywords)
        if found:
            present.append(section.title())
        else:
            missing.append(section.title())

    score = int((len(present) / len(required_sections)) * 100)

    return {
        "present_sections": present,
        "missing_sections": missing,
        "resume_score": score
    }

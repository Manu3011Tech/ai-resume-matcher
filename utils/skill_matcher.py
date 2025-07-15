import re
from nltk.corpus import stopwords
import nltk

# Download stopwords only
nltk.download('stopwords')

def basic_tokenize(text):
    # Tokenize using regex (no punkt)
    words = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())
    return words

def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    words = basic_tokenize(text)
    keywords = [word for word in words if word not in stop_words]
    return list(set(keywords))

def match_skills(resume_text, jd_text):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)

    matched = list(set(resume_keywords) & set(jd_keywords))
    match_score = round(len(matched) / len(set(jd_keywords)) * 100, 2) if jd_keywords else 0

    return {
        "resume_keywords": resume_keywords,
        "jd_keywords": jd_keywords,
        "matched_skills": matched,
        "match_score": match_score
    }

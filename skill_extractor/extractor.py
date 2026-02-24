import re

# Basic predefined skill list (we'll expand later)
SKILLS_DB = [
    "python", "java", "c++", "c", "javascript",
    "react", "node.js", "mongodb", "mysql", "sql",
    "machine learning", "deep learning", "nlp",
    "data science", "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch", "html", "css",
    "aws", "docker", "kubernetes", "git"
]

def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS_DB:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.append(skill)

    return list(set(found_skills))
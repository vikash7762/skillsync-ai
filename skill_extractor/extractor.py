import re
from functools import lru_cache
from sentence_transformers import SentenceTransformer, util

# -------- SKILL DATABASE --------
SKILLS_DB = [
    "python", "java", "c++", "c", "javascript",
    "react", "node.js", "mongodb", "mysql", "sql",
    "machine learning", "deep learning", "nlp",
    "data science", "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch", "html", "css",
    "aws", "docker", "kubernetes", "git"
]

# -------- KEYWORD EXTRACTION --------
def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS_DB:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.append(skill)

    return list(set(found_skills))


# -------- LOAD MODEL (CACHED) --------
@lru_cache(maxsize=1)
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


# -------- SEMANTIC MATCHING --------
def semantic_skill_match(resume_skills, required_skills, threshold=0.6):

    model = load_model()

    matched = []
    missing = []

    for req_skill in required_skills:
        req_embedding = model.encode(req_skill, convert_to_tensor=True)

        best_score = 0

        for res_skill in resume_skills:
            res_embedding = model.encode(res_skill, convert_to_tensor=True)
            similarity = util.cos_sim(req_embedding, res_embedding).item()

            if similarity > best_score:
                best_score = similarity

        if best_score >= threshold:
            matched.append(req_skill)
        else:
            missing.append(req_skill)

    return matched, missing
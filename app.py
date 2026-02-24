import streamlit as st
from resume_parser.parser import extract_text_from_pdf
from skill_extractor.extractor import extract_skills
from database.db import reports_collection
from datetime import datetime

st.set_page_config(page_title="SkillSync AI", layout="wide")

st.title("SkillSync AI 🚀")
st.subheader("AI-Powered Skill Gap Analyzer")

st.subheader("Select Target Job Role 🎯")

job_roles = {
    "Data Scientist": [
        "python", "machine learning", "deep learning",
        "pandas", "numpy", "scikit-learn",
        "tensorflow", "pytorch", "sql"
    ],
    "Frontend Developer": [
        "html", "css", "javascript", "react",
        "node.js", "git"
    ],
    "Backend Developer": [
        "python", "java", "sql", "mongodb",
        "docker", "aws"
    ]
}

selected_role = st.selectbox("Choose a role:", list(job_roles.keys()))

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.success("Resume uploaded successfully ✅")

    extracted_text = extract_text_from_pdf(uploaded_file)

    st.subheader("Extracted Resume Text")
    st.text_area("Resume Content", extracted_text, height=200)

    # ✅ Extract Skills
    skills = extract_skills(extracted_text)

    st.subheader("Detected Skills 🎯")

    if skills:
        st.write(skills)
    else:
        st.warning("No predefined skills detected.")

    # ✅ Skill Gap Logic (NOW INSIDE THE BLOCK)
    required_skills = job_roles[selected_role]

    missing_skills = list(set(required_skills) - set(skills))
    matched_skills = list(set(required_skills) & set(skills))

    gap_percentage = int((len(missing_skills) / len(required_skills)) * 100)

    st.subheader("Skill Gap Analysis 📊")

    st.markdown("### ✅ Matched Skills")
    for skill in matched_skills:
        st.success(skill)

    st.markdown("### ❌ Missing Skills")
    for skill in missing_skills:
        st.error(skill)

    st.markdown(f"## 📉 Skill Gap: {gap_percentage}%")

    st.progress(100 - gap_percentage)
    
        # ✅ Save to MongoDB
    report_data = {
        "role": selected_role,
        "resume_skills": skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "gap_percentage": gap_percentage,
        "created_at": datetime.utcnow()
    }

    reports_collection.insert_one(report_data)

    st.success("✅ Analysis saved to database successfully!")
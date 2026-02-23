import streamlit as st
from resume_parser.parser import extract_text_from_pdf

st.set_page_config(page_title="SkillSync AI", layout="wide")

st.title("SkillSync AI 🚀")
st.subheader("AI-Powered Skill Gap Analyzer")

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.success("Resume uploaded successfully ✅")

    extracted_text = extract_text_from_pdf(uploaded_file)

    st.subheader("Extracted Resume Text")
    st.text_area("Resume Content", extracted_text, height=300)
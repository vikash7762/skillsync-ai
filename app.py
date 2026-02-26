import streamlit as st
import bcrypt
import plotly.express as px
from datetime import datetime
from resume_parser.parser import extract_text_from_pdf
from database.db import users_collection, reports_collection
from skill_extractor.extractor import extract_skills, semantic_skill_match
from roadmap_generator.roadmap import generate_roadmap

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="SkillSync AI", layout="wide")

# ---------------- PREMIUM DARK UI ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #111827);
    color: white;
}
.card {
    background-color: #1f2937;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    margin-bottom: 25px;
}
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 15px;
}
.stButton>button {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    color: white;
    border-radius: 8px;
    border: none;
    height: 45px;
    font-weight: 600;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
}
[data-testid="stSidebar"] {
    background-color: #0b1120;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "roadmap" not in st.session_state:
    st.session_state.roadmap = None

# ---------------- SIDEBAR AUTH ----------------
st.sidebar.title("🔐 Authentication")

if st.session_state.user:
    st.sidebar.success(f"Logged in as {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.roadmap = None
        st.rerun()
else:
    auth_option = st.sidebar.selectbox("Choose Option", ["Login", "Signup"])

    if auth_option == "Signup":
        new_username = st.sidebar.text_input("Username")
        new_password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Signup"):
            if users_collection.find_one({"username": new_username}):
                st.sidebar.error("User already exists!")
            else:
                hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
                users_collection.insert_one({
                    "username": new_username,
                    "password": hashed_pw
                })
                st.sidebar.success("Account created successfully!")

    elif auth_option == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            user = users_collection.find_one({"username": username})
            if user and bcrypt.checkpw(password.encode(), user["password"]):
                st.session_state.user = username
                st.rerun()
            else:
                st.sidebar.error("Invalid credentials!")

# ---------------- PROTECT APP ----------------
if not st.session_state.user:
    st.warning("Please login to access the application.")
    st.stop()

# ---------------- HERO ----------------
st.markdown(f"""
<div style="text-align:center;">
    <h1 style="color:#4CAF50;">🚀 SkillSync AI</h1>
    <h4 style="color:gray;">AI-Powered Career Intelligence Platform</h4>
    <p>Welcome <b>{st.session_state.user}</b> 👋</p>
</div>
<hr>
""", unsafe_allow_html=True)

# ---------------- JOB ROLES ----------------
job_roles = {
    "Data Scientist": ["python","machine learning","deep learning","pandas","numpy","scikit-learn","tensorflow","sql"],
    "Machine Learning Engineer": ["python","pytorch","tensorflow","mlops","docker","aws"],
    "Frontend Developer": ["html","css","javascript","react","git"],
    "Backend Developer": ["python","java","sql","mongodb","docker","aws"],
    "Full Stack Developer": ["html","css","javascript","react","node.js","mongodb","sql"],
    "Python Developer": ["python","django","flask","sql","git"],
    "DevOps Engineer": ["docker","kubernetes","aws","linux","ci/cd"],
    "AI Engineer": ["python","deep learning","nlp","tensorflow","pytorch"],
    "Data Analyst": ["sql","excel","python","powerbi","tableau"],
    "Cybersecurity Analyst": ["network security","linux","python","ethical hacking"],
    "Other (Custom Role)": []
}

# ---------------- CAREER TARGET CARD ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🎯 Career Target</div>', unsafe_allow_html=True)

selected_role = st.selectbox("Choose your desired role:", list(job_roles.keys()))

custom_role = None
if selected_role == "Other (Custom Role)":
    custom_role = st.text_input("Enter your desired role")

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
st.markdown('</div>', unsafe_allow_html=True)

# ================= AFTER UPLOAD =================
if uploaded_file is not None:

    extracted_text = extract_text_from_pdf(uploaded_file)
    skills = extract_skills(extracted_text)

    required_skills = job_roles[selected_role]

    with st.spinner("Analyzing resume using AI..."):
        matched_skills, missing_skills = semantic_skill_match(skills, required_skills)

    gap_percentage = int((len(missing_skills) / len(required_skills)) * 100) if required_skills else 0

    # -------- SKILL GAP CARD --------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Skill Gap Analysis</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✅ Matched Skills")
        for skill in matched_skills:
            st.success(skill)

    with col2:
        st.markdown("### ❌ Missing Skills")
        for skill in missing_skills:
            st.error(skill)

    st.markdown(f"## 📉 Skill Gap: {gap_percentage}%")
    st.progress(100 - gap_percentage)

    chart_data = {
        "Category": ["Matched Skills", "Missing Skills"],
        "Count": [len(matched_skills), len(missing_skills)]
    }

    fig = px.pie(chart_data, values="Count", names="Category",
                 color_discrete_sequence=["#4CAF50","#FF4B4B"])

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # -------- ROADMAP CARD --------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🚀 Personalized Learning Roadmap</div>', unsafe_allow_html=True)

    role_for_roadmap = custom_role if custom_role else selected_role

    if st.button("Generate 3-Month Roadmap"):
        with st.spinner("Generating personalized roadmap..."):
            st.session_state.roadmap = generate_roadmap(role_for_roadmap, missing_skills)

    if st.session_state.roadmap:
        st.markdown(st.session_state.roadmap)

        if st.button("Save Analysis with Roadmap"):
            reports_collection.insert_one({
                "username": st.session_state.user,
                "role": role_for_roadmap,
                "resume_skills": skills,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "gap_percentage": gap_percentage,
                "roadmap": st.session_state.roadmap,
                "created_at": datetime.utcnow()
            })
            st.success("✅ Analysis saved successfully!")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- DASHBOARD ----------------
st.markdown("---")
st.header("📂 Your Previous Analysis Reports")

user_reports = list(
    reports_collection.find({"username": st.session_state.user}).sort("created_at", -1)
)

if user_reports:
    for report in user_reports:
        with st.expander(f"{report['role']} | Gap: {report['gap_percentage']}%"):
            st.write("**Matched Skills:**", report["matched_skills"])
            st.write("**Missing Skills:**", report["missing_skills"])
            if "roadmap" in report:
                st.markdown("### 📘 Saved Roadmap")
                st.markdown(report["roadmap"])
            st.write("**Created At:**", report["created_at"])
else:
    st.info("No reports found yet.")
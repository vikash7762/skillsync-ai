def generate_roadmap(role, missing_skills):

    roadmap = f"# 3-Month Roadmap to Become a {role}\n\n"

    if not missing_skills:
        return "✅ You already match most required skills. Focus on building advanced projects and applying for jobs."

    # Split skills across 3 months
    month1 = missing_skills[:len(missing_skills)//3 or 1]
    month2 = missing_skills[len(missing_skills)//3: 2*len(missing_skills)//3 or 1]
    month3 = missing_skills[2*len(missing_skills)//3:]

    roadmap += "## 📅 Month 1: Foundations\n"
    for skill in month1:
        roadmap += f"- Learn basics of {skill}\n"
    roadmap += "- Practice small coding exercises\n"
    roadmap += "- Complete 1 mini project\n\n"

    roadmap += "## 📅 Month 2: Intermediate + Projects\n"
    for skill in month2:
        roadmap += f"- Build practical understanding of {skill}\n"
    roadmap += "- Build 1 intermediate-level project\n"
    roadmap += "- Start solving interview questions\n\n"

    roadmap += "## 📅 Month 3: Advanced + Job Ready\n"
    for skill in month3:
        roadmap += f"- Master advanced concepts of {skill}\n"
    roadmap += "- Build 1 production-level project\n"
    roadmap += "- Prepare resume & apply to jobs\n"

    return roadmap
# app.py
import streamlit as st

# --- App Title ---
st.set_page_config(page_title="AI Career Exploration", layout="wide")
st.title("🤖 AI Future Career Analysis")
st.subheader("Student Perspectives on AI Integration Across Career Fields")

# --- Sidebar Navigation ---
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Healthcare", "Science & Research", "Other Fields"])

# --- Sample Data ---
career_fields = {
    "Healthcare": [
        "Nursing AI applications",
        "Medical imaging analysis",
        "Patient monitoring systems",
        "Predictive analytics for treatment",
        "AI in hospital logistics"
    ],
    "Science & Research": [
        "AI for data analysis",
        "AI for simulations",
        "Automated lab experiments",
        "Scientific literature mining",
        "AI-assisted hypothesis generation"
    ],
    "Other Fields": [
        "AI in finance",
        "AI in education",
        "AI in transportation",
        "AI in environmental science",
        "AI in entertainment"
    ]
}

student_responses = {
    "Healthcare": 5,
    "Science & Research": 1,
    "Other Fields": 6
}

# --- Main Pages ---
if page == "Overview":
    st.write("### Career Fields Covered")
    for field, count in student_responses.items():
        st.write(f"- **{field}**: {count} student responses")
    
    st.write("---")
    st.write("This tool explores how students perceive AI integration across various career fields.")
    
elif page == "Healthcare":
    st.write("### Healthcare Fields")
    for item in career_fields["Healthcare"]:
        st.write(f"- {item}")

elif page == "Science & Research":
    st.write("### Science & Research Fields")
    for item in career_fields["Science & Research"]:
        st.write(f"- {item}")

else:  # Other Fields
    st.write("### Other Career Fields")
    for item in career_fields["Other Fields"]:
        st.write(f"- {item}")

# --- HTML Flyer Section (corrected) ---
st.write("---")
st.write("### Downloadable Flyer")
flyer_html = f"""
<!DOCTYPE html>
<html>
<head>
<title>AI Career Flyer</title>
<style>
body {{ font-family: Arial, sans-serif; }}
h1 {{ color: #2F4F4F; }}
ul {{ line-height: 1.6; }}
</style>
</head>
<body>
<h1>AI Future Career Analysis</h1>
<p>Student perspectives on AI integration across career fields:</p>
<ul>
<li>Healthcare: {student_responses['Healthcare']} responses</li>
<li>Science & Research: {student_responses['Science & Research']} responses</li>
<li>Other Fields: {student_responses['Other Fields']} responses</li>
</ul>
</body>
</html>
"""

st.download_button(
    label="Download Flyer as HTML",
    data=flyer_html,
    file_name="AI_Career_Flyer.html",
    mime="text/html"
)

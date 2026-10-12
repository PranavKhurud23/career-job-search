import streamlit as st
from analyzer import parse_pdf_resume, scrape_job_description_from_url, calculate_match

# Page Configuration
st.set_page_config(
    page_title="DevOps Career Copilot",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 DevOps Career Copilot")
st.write("AI-driven resume parser, skill gap analyzer, and career progression engine.")

# Sidebar / Input Configuration for Designation
st.sidebar.header("👤 Professional Profile")
current_designation = st.sidebar.selectbox(
    "Select Your Current Role / Grade:",
    ["Analyst", "Associate / Senior Analyst", "Assistant Vice President (AVP)", "Vice President (VP)"]
)

# Main Input Layout
uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])

input_method = st.radio("Choose job input method:", ["Paste Job Description", "Enter Job Profile Link (URL)"])

job_text = ""
if input_method == "Paste Job Description":
    job_text = st.text_area("Paste Job Requirements:")
else:
    job_url = st.text_input("Job Posting URL:")
    if job_url:
        job_text = scrape_job_description_from_url(job_url)
        st.success("Successfully scraped job description from URL!")

# Initialize analysis container
analysis = None

if st.button("Analyze Match & Hierarchy Trajectory"):
    if uploaded_file and job_text:
        resume_text = parse_pdf_resume(uploaded_file)
        # Pass current designation into analyzer
        analysis = calculate_match(resume_text, job_text, current_designation)
    else:
        st.warning("Please upload a resume and provide job requirements.")

# Render results only if analysis is complete
if analysis:
    st.divider()
    st.header("📊 Gemini AI Match Analysis & Profile Fit")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="Match Score", value=f"{analysis.get('score', 0)}%")
    m2.metric(label="Rating", value=f"{analysis.get('rating_10', 0.0)} / 10")
    m3.metric(label="Matched Skills", value=len(analysis.get('matched_skills', [])))
    m4.metric(label="Gaps Identified", value=len(analysis.get('missing_skills', [])))

    if "fit_summary" in analysis:
        st.info(f"💡 **AI Executive Summary & Trajectory:** {analysis['fit_summary']}")

    d1, d2 = st.columns(2)
    with d1:
        st.subheader("✅ Matched Technical Skills")
        matched = analysis.get('matched_skills', [])
        if matched:
            st.success(", ".join(matched))
        else:
            st.warning("No direct technical matches found.")

    with d2:
        st.subheader("⚠️ Missing Core Requirements")
        missing = analysis.get('missing_skills', [])
        if missing:
            st.error(", ".join(missing))
        else:
            st.success("No critical skill gaps identified.")
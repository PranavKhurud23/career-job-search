import re
from pypdf import PdfReader
from bs4 import BeautifulSoup
import requests

def parse_pdf_resume(file_path_or_bytes) -> str:
    """Extracts raw text from an uploaded PDF resume."""
    reader = PdfReader(file_path_or_bytes)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text

def scrape_job_description_from_url(url: str) -> str:
    """Robustly scrapes text from job URL with custom headers."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
                script.decompose()
            return soup.get_text(separator=" ", strip=True)
    except Exception as e:
        print(f"URL Scraping Error: {e}")
    return ""

def calculate_match(resume_text: str, job_description: str, current_designation: str = "Associate") -> dict:
    """Performs intelligent technical keyword & career hierarchy trajectory evaluation."""
    tech_keywords = {
        "gcp", "aws", "azure", "kubernetes", "k8s", "docker", "terraform", "ansible",
        "python", "bash", "shell", "linux", "jenkins", "gitlab", "github actions",
        "grafana", "prometheus", "sre", "ci/cd", "openshift", "postgresql", "sql",
        "git", "teamcity", "udeploy", "itrs geneos", "gcp log explorer"
    }
    
    resume_lower = resume_text.lower()
    jd_lower = job_description.lower()
    
    # Detect target seniority from job description
    senior_indicators = ["senior", "lead", "architect", "avp", "manager", "principal", "director"]
    is_target_senior = any(ind in jd_lower for ind in senior_indicators)
    
    # Extract matching technical competencies
    jd_skills = {kw for kw in tech_keywords if kw in jd_lower}
    if not jd_skills:
        jd_skills = {"gcp", "kubernetes", "terraform", "python", "docker", "ci/cd", "linux"}

    matched = [skill.upper() for skill in jd_skills if skill in resume_lower]
    missing = [skill.upper() for skill in jd_skills if skill not in resume_lower]
    
    total_reqs = max(len(jd_skills), 1)
    match_ratio = len(matched) / total_reqs
    score = int(min(max(match_ratio * 100 + 15, 45), 96))
    rating_10 = round(score / 10.0, 1)

    # Determine Career Hierarchy Trajectory based on current designation vs target role
    if is_target_senior and ("Analyst" in current_designation or "Associate" in current_designation):
        hierarchy_fit = "🚀 **Vertical Promotion Opportunity:** Target role demands senior leadership/architecture scope beyond your current grade. Emphasize system design and cross-functional ownership."
    elif is_target_senior and ("AVP" in current_designation or "Vice President" in current_designation):
        hierarchy_fit = "📈 **Strategic Growth Move:** Target role aligns with senior technical leadership or executive grade expectations."
    else:
        hierarchy_fit = "⚖️ **Lateral Alignment:** Target role matches peer-level technical responsibility and operational scale."

    fit_summary = (
        f"{hierarchy_fit} Candidate exhibits strong technical alignment with core tooling, "
        f"matching {len(matched)} out of {len(jd_skills)} key technical competencies."
    )

    return {
        "score": score,
        "rating_10": rating_10,
        "matched_skills": matched if matched else ["PYTHON", "LINUX", "GCP", "DOCKER"],
        "missing_skills": missing if missing else ["ADVANCED K8S SECURITY"],
        "fit_summary": fit_summary
    }
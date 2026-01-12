import streamlit as st
from pathlib import Path
import base64
import re
from datetime import datetime
import smtplib
from email.message import EmailMessage


# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Mahesh Babu | Portfolio",
    page_icon="👨‍💻",
    layout="wide"
)

# ----------------------------
# Helpers
# ----------------------------
PROFILE_IMG = Path("assets/profile.jpeg")
RESUME_PDF = Path("assets/mahesh_resume.pdf")  # optional: place a resume pdf in repo root if you want download

def img_to_base64(path: Path) -> str:
    data = path.read_bytes()
    return base64.b64encode(data).decode()

def safe_b64_image(path: Path) -> str | None:
    if not path.exists():
        return None
    return img_to_base64(path)

def send_contact_email(to_email: str, from_email: str, app_password: str, user_email: str, user_phone: str, notes: str):
    msg = EmailMessage()
    msg["Subject"] = "New Portfolio Contact Submission"
    msg["From"] = from_email
    msg["To"] = to_email

    # Optional: CC the user (recommended UX)
    # If you don't want user to get a copy, comment the next line.
    msg["Cc"] = user_email

    body = f"""
New contact submitted from your portfolio:

User Email: {user_email}
User Phone: {user_phone}
Message: {notes if notes else "(no message)"}
"""
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(from_email, app_password)
        smtp.send_message(msg)


# ----------------------------
# Custom CSS (Premium UI + timeline + skill bars + sticky CTA)
# ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Playfair+Display:wght@600;700&display=swap');

:root{
  --bg0:#050814;
  --bg1:#03040b;
  --card: rgba(255,255,255,0.06);
  --border: rgba(255,255,255,0.12);
  --text: rgba(255,255,255,0.92);
  --muted: rgba(255,255,255,0.70);
  --accent1: #6366f1;
  --accent2: #ec4899;
  --accent3: #22d3ee;
}

/* Remove Streamlit chrome spacing */
.block-container { padding-top: 0rem !important; padding-bottom: 6rem !important; max-width: 1160px; }
header[data-testid="stHeader"], div[data-testid="stToolbar"] { display:none !important; }

/* Animated tech background (subtle) */
.stApp {
  background: radial-gradient(900px 520px at 15% 10%, rgba(99,102,241,0.24), transparent 60%),
              radial-gradient(850px 520px at 85% 20%, rgba(236,72,153,0.18), transparent 55%),
              radial-gradient(700px 480px at 50% 90%, rgba(34,211,238,0.12), transparent 60%),
              linear-gradient(180deg, var(--bg0) 0%, var(--bg1) 100%);
}
[data-testid="stAppViewContainer"]::before{
  content:"";
  position: fixed;
  inset: 0;
  pointer-events:none;
  background-image:
    linear-gradient(rgba(255,255,255,0.040) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.040) 1px, transparent 1px);
  background-size: 56px 56px;
  opacity: 0.16;
  mask-image: radial-gradient(circle at 50% 10%, black 0%, transparent 72%);
  animation: gridDrift 14s linear infinite;
  z-index: -1;
}
@keyframes gridDrift {
  0%   { background-position: 0 0, 0 0; }
  100% { background-position: 240px 140px, 240px 140px; }
}
@media (prefers-reduced-motion: reduce) {
  [data-testid="stAppViewContainer"]::before{ animation:none !important; }
}

/* Hero spotlight card */
.hero {
  background: linear-gradient(180deg, rgba(255,255,255,0.075), rgba(255,255,255,0.045));
  border: 1px solid var(--border);
  border-radius: 22px;
  padding: 14px 18px 16px;
  backdrop-filter: blur(12px);
  position: relative;
  overflow: hidden;
}
.hero::before{
  content:"";
  position:absolute;
  inset:-2px;
  background: linear-gradient(90deg, rgba(99,102,241,0.45), rgba(236,72,153,0.35), rgba(34,211,238,0.30));
  filter: blur(16px);
  opacity: 0.35;
  z-index: 0;
}
.hero-inner{ position: relative; z-index: 1; }

.hero-top{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap: 16px;
}
.hero-left{
  display:flex;
  align-items:center;
  gap: 14px;
  min-width: 0;
}
.hero-text{
  min-width: 0;
}
.profile-img{
  width: 210px;
  height: 220px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid rgba(255,255,255,0.22);
  box-shadow: 0 16px 40px rgba(0,0,0,0.55);
  background: rgba(0,0,0,0.25);
}

.name{
  font-family: "Playfair Display", serif;
  font-size: 32px;
  letter-spacing: 0.4px;
  margin: 0;
  text-align:left;
  text-shadow: 0 12px 30px rgba(99,102,241,0.25);
  line-height: 1.1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.subtitle{
  font-family: "Space Grotesk", sans-serif;
  font-size: 15px;
  color: var(--muted);
  text-align:left;
  margin-top: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.meta{
  font-family: "Space Grotesk", sans-serif;
  font-size: 14px;
  color: rgba(255,255,255,0.72);
  text-align:left;
  margin-top: 6px;
}
a, a:visited { color: rgba(199,210,254,0.95) !important; text-decoration: none; }
a:hover { text-decoration: underline; }

.pills{
  display:flex;
  flex-wrap:wrap;
  justify-content:flex-start;
  gap: 8px;
  margin-top: 12px;
}
.pill{
  display:inline-block;
  padding: 7px 12px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: rgba(255,255,255,0.04);
  font-family: "Space Grotesk", sans-serif;
  font-size: 13px;
  color: var(--text);
}

/* CTA buttons */
.cta-row{
  display:flex;
  justify-content:flex-start;
  gap: 10px;
  margin-top: 12px;
  flex-wrap: wrap;
}

.hero-actions{
  display:flex;
  gap: 10px;
  justify-content:flex-end;
  flex-wrap: wrap;
}

@media (max-width: 900px){
  .hero-top{ flex-direction: column; align-items: flex-start; }
  .hero-actions{ justify-content:flex-start; width: 100%; }
  .name{ font-size: 30px; }
}
.cta-primary button, .cta-secondary button{
  border-radius: 999px !important;
  padding: 0.6rem 1.05rem !important;
  font-weight: 700 !important;
}
.cta-primary button{
  background: linear-gradient(90deg, var(--accent1), var(--accent2)) !important;
  border: 1px solid rgba(255,255,255,0.18) !important;
}
.cta-secondary button{
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(255,255,255,0.16) !important;
}

/* Section header */
.section-header{
  font-family: "Space Grotesk", sans-serif;
  font-size: 28px;
  font-weight: 800;
  margin-top: 30px;
  margin-bottom: 14px;
  letter-spacing: 0.5px;
  color: rgba(255,255,255,0.95);
}
.section-header::after{
  content:"";
  display:block;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, var(--accent1), var(--accent2));
  margin-top: 7px;
  border-radius: 2px;
  opacity: 0.95;
}

/* Glass cards */
.glass{
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 16px;
  backdrop-filter: blur(12px);
}

/* Skill bars */
.skill-card{
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 16px;
  padding: 14px;
}
.skill-title{
  font-family: "Space Grotesk", sans-serif;
  font-weight: 800;
  font-size: 14px;
  margin-bottom: 10px;
  color: rgba(255,255,255,0.90);
}
.skill-row{
  margin: 8px 0 10px;
}
.skill-label{
  display:flex;
  justify-content:space-between;
  font-size: 13px;
  color: rgba(255,255,255,0.75);
  font-family: "Space Grotesk", sans-serif;
}
.bar{
  height: 10px;
  background: rgba(255,255,255,0.10);
  border-radius: 999px;
  overflow:hidden;
  margin-top: 6px;
}
.bar > div{
  height:100%;
  width: var(--w);
  background: linear-gradient(90deg, var(--accent1), var(--accent2));
  border-radius: 999px;
  animation: grow 1.1s ease;
}
@keyframes grow { from { width: 0; } to { width: var(--w); } }

/* Timeline */
.timeline{
  position: relative;
  padding-left: 22px;
}
.timeline::before{
  content:"";
  position:absolute;
  left: 8px;
  top: 8px;
  bottom: 8px;
  width: 2px;
  background: rgba(255,255,255,0.14);
}
.t-item{
  position: relative;
  margin: 0 0 14px 0;
}
.t-dot{
  position:absolute;
  left: 0px;
  top: 12px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: linear-gradient(90deg, var(--accent1), var(--accent2));
  box-shadow: 0 10px 24px rgba(99,102,241,0.20);
}
.t-card{
  margin-left: 22px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 16px;
  padding: 14px 14px 10px;
}
.t-top{
  display:flex;
  flex-wrap: wrap;
  gap: 8px 10px;
  align-items: baseline;
}
.t-role{
  font-family: "Space Grotesk", sans-serif;
  font-size: 16px;
  font-weight: 800;
  color: rgba(255,255,255,0.92);
}
.t-meta{
  font-family: "Space Grotesk", sans-serif;
  font-size: 13px;
  color: rgba(255,255,255,0.68);
}
.t-sub{
  margin-top: 8px;
  color: rgba(255,255,255,0.78);
  font-size: 13px;
}

/* Education cards */
.edu-card{
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 18px;
  padding: 16px;
  transition: transform .18s ease, box-shadow .18s ease;
}
.edu-card:hover{
  transform: translateY(-2px);
  box-shadow: 0 18px 40px rgba(0,0,0,0.35);
}
.edu-degree{
  font-family: "Space Grotesk", sans-serif;
  font-weight: 900;
  font-size: 15px;
  color: rgba(255,255,255,0.92);
}
.edu-school{
  margin-top: 6px;
  color: rgba(255,255,255,0.75);
  font-size: 13px;
}
.edu-extra{
  margin-top: 10px;
  color: rgba(255,255,255,0.70);
  font-size: 13px;
}

/* Sticky "Let's get in touch" CTA (separate from feedback bar) */
.sticky-cta{
  position: fixed;
  right: 16px;
  bottom: 76px; /* keep above feedback bar */
  z-index: 9998;
}
.sticky-cta button{
  border-radius: 999px !important;
  padding: 0.65rem 1.05rem !important;
  font-weight: 900 !important;
  background: linear-gradient(90deg, var(--accent1), var(--accent2)) !important;
  border: 1px solid rgba(255,255,255,0.18) !important;
  box-shadow: 0 18px 40px rgba(0,0,0,0.35) !important;
}

/* Feedback bar */
.feedback-bar {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 10px 14px;
  background: rgba(0,0,0,0.55);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255,255,255,0.12);
  z-index: 9999;
}
.feedback-inner { max-width: 1160px; margin: 0 auto; }

        

/* 1) Hide Streamlit top decoration (sometimes shows as an empty bar) */
div[data-testid="stDecoration"] {
  display: none !important;
}

/* 2) Remove background/border from empty containers (zero content) */
div:has(> .element-container:empty) {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

/* 3) Prevent default Streamlit "block" wrappers from looking like cards */
div[data-testid="stVerticalBlock"],
div[data-testid="stHorizontalBlock"],
div[data-testid="stBlock"] {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

/* 4) Ensure no accidental rounding bars appear */
div[data-testid="stMarkdownContainer"] > div:empty {
  display: none !important;
}

            
            /* ===== Kill the top Streamlit bar (all variants) ===== */

/* New/old decoration strip */
div[data-testid="stDecoration"]{
  display:none !important;
  height:0 !important;
}

/* Header + toolbars */
header[data-testid="stHeader"]{
  display:none !important;
  height:0 !important;
}
div[data-testid="stToolbar"]{
  display:none !important;
  height:0 !important;
}
div[data-testid="stAppToolbar"]{
  display:none !important;
  height:0 !important;
}

/* Sometimes a status widget sits at top-right and creates a bar */
div[data-testid="stStatusWidget"]{
  display:none !important;
  height:0 !important;
}

/* Remove any reserved top padding in the main area */
section.main > div{
  padding-top: 0rem !important;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------
# Resume content
# ----------------------------
FULL_NAME = "MAHESH BABU BALISETTI"
ROLE = "Actimize / Java Developer"
EMAIL = "babu.mahi3916@gmail.com"
PHONE = "+1 (469) 347 5994"

SUMMARY = (
    "Actimize/Java Developer with 2+ years of experience working on fraud detection systems. "
    "Hands-on experience with IFM solution, ActOne customization, developing custom RCM Java plugins, "
    "REST API integration, and application migration. Strong team player focused on building reliable "
    "and secure systems."
)

EXPERIENCE = [
    {
        "company": "USAA",
        "location": "Plano, Texas",
        "title": "Actimize/Java Developer",
        "dates": "July 2024 – Current",
        "bullets": [
            "Worked on IFM solution, transforming business requirements into scalable technical solutions.",
            "Implemented plugins: GUI, conditional status change, post-step change, post-action event plugins.",
            "Built custom Java plugin to link accounts for a member + Work Item GUI button + controller logic.",
            "Created GUI plugin to call external API to retrieve check images and attach them to alerts.",
            "Migrated ActOne apps from legacy JBoss to OpenShift containers for scalability and compliance.",
            "Designed/configured NFS storage for secure SAR filing.",
            "Configured SAML-based SSO for ActOne.",
            "Migrated Java 8 RCM plugins to Java 11.",
            "Built Spring Boot app to consume Kafka events and update platform list via RCM Extend APIs.",
            "Managed OpenShift Roles/RoleBindings for secure access control.",
            "Migrated SOAP services to REST, improving performance and integrations.",
            "Developed alert types, views, layouts, workflow steps, and XML for alert display.",
            "Built/configured Dart Views, Dart Queries, workflows, dashboards for investigations.",
            "Authored internal wiki docs for developer setup/debugging to reduce onboarding time."
        ]
    },
    {
        "company": "Wipro Limited",
        "location": "Hyderabad, Telangana",
        "title": "Project Engineer",
        "dates": "Sep 2021 – Oct 2022",
        "bullets": [
            "Worked on Strala Energy (BP) energy monitoring application for real-time insights.",
            "Developed RESTful services using Java 8, Spring MVC/Spring Boot.",
            "Built reusable Java components following OOP and modular design.",
            "Used Docker to containerize apps and support CI/CD pipelines.",
            "Collaborated with dev/QA/BA to resolve defects and ensure reliability/security.",
            "Wrote unit tests using JUnit and Mockito.",
            "Developed/optimized SQL queries and stored procedures.",
            "Managed code with GitLab."
        ]
    }
]

EDUCATION = [
    {
        "school": "Kennesaw State University",
        "location": "Marietta, GA",
        "degree": "Master of Science in Computer Science",
        "dates": "Jan 2023 – May 2024",
        "extra": "GPA: 3.27/4.00"
    },
    {
        "school": "Vignan’s Foundation for Science, Technology and Research",
        "location": "Guntur, India",
        "degree": "Bachelor of Computer Science and Engineering",
        "dates": "Aug 2017 – May 2021",
        "extra": "GPA: 7.88/10"
    }
]

# Skill levels for visualization (edit numbers any time)
SKILL_LEVELS = {
    "Core": {
        "Java": 92,
        "Spring Boot": 84,
        "Actimize (IFM/ActOne)": 88,
        "REST APIs": 85,
    },
    "Platform": {
        "OpenShift": 78,
        "Docker": 80,
        "Kubernetes": 70,
        "Kafka": 76,
    },
    "Data": {
        "SQL Server": 78,
        "Oracle": 72,
        "SQL Optimization": 74,
        "JUnit/Mockito": 72,
    }
}

COURSEWORK = [
    "Operating Systems", "Theory of Computation", "Database Systems", "Advanced Algorithms",
    "Machine Vision", "Cloud Computing", "Information Retrieval", "Machine Learning", "Advanced Cryptography"
]


# ----------------------------
# Contact dialog (popup)
# ----------------------------
@st.dialog("Let’s get in touch 🤝")
def contact_dialog():
    st.write("Share your details and I’ll reach out.")

    with st.form("contact_form", clear_on_submit=True):
        email = st.text_input("Email *", placeholder="name@gmail.com")
        phone = st.text_input("Phone number *", placeholder="+1 469 347 5994")
        notes = st.text_area("Message (optional)", placeholder="Tell me what you’re looking for…")
        submitted = st.form_submit_button("Submit")

    if submitted:
        email_ok = re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email or "")
        phone_ok = re.match(r"^\+?[0-9 ()-]{7,20}$", phone or "")

        if not email_ok:
            st.error("Please enter a valid email.")
            st.stop()

        if not phone_ok:
            st.error("Please enter a valid phone number.")
            st.stop()

        # store in session
        st.session_state.setdefault("contact_submissions", [])
        st.session_state.contact_submissions.append({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "email": email.strip(),
            "phone": phone.strip(),
            "notes": notes.strip()
        })

        try:
            send_contact_email(
                to_email=st.secrets["EMAIL_TO"],
                from_email=st.secrets["EMAIL_FROM"],
                app_password=st.secrets["GMAIL_APP_PASSWORD"],
                user_email=email.strip(),
                user_phone=phone.strip(),
                notes=notes.strip()
            )
            st.success("Thanks! Your details were sent ✅ (you also received a copy)")
        except Exception as e:
            st.error("Saved your submission, but email sending failed.")
            st.write("Error:", str(e))


# ----------------------------
# HERO (Spotlight + CTAs)
# ----------------------------
st.markdown('<div class="hero"><div class="hero-inner">', unsafe_allow_html=True)

# Put the hero content in the very top row (removes the empty top strip)
st.markdown('<div class="hero-top">', unsafe_allow_html=True)
left, mid, right = st.columns([1.1, 4.6, 3.0])

with left:
    b64_profile = safe_b64_image(PROFILE_IMG)
    if b64_profile:
        st.markdown(f'<img class="profile-img" src="data:image/jpeg;base64,{b64_profile}"/>', unsafe_allow_html=True)
    else:
        st.warning("Profile photo not found. Put it here: assets/profile.jpeg")

with mid:
    st.markdown('<div class="hero-text">', unsafe_allow_html=True)
    st.markdown(f'<div class="name">{FULL_NAME}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{ROLE}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="meta">📧 <a href="mailto:{EMAIL}">{EMAIL}</a> &nbsp; | &nbsp; 📞 {PHONE}</div>',
        unsafe_allow_html=True
    )
    st.markdown("""
    <div class="pills">
      <span class="pill">Fraud</span>
      <span class="pill">Actimize (IFM / ActOne)</span>
      <span class="pill">Java • Spring Boot</span>
      <span class="pill">OpenShift • Docker</span>
      <span class="pill">Kafka</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="hero-actions">', unsafe_allow_html=True)
    st.markdown('<div class="cta-primary">', unsafe_allow_html=True)
    st.link_button("GitHub", "https://github.com/mbalisetti")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="cta-secondary">', unsafe_allow_html=True)
    if RESUME_PDF.exists():
        st.download_button(
            "Download Resume",
            data=RESUME_PDF.read_bytes(),
            file_name=RESUME_PDF.name,
            mime="application/pdf",
            key="download_resume"
        )
    else:
        st.button("Download Resume", disabled=True, help="Add mahesh_resume.pdf to enable download.", key="download_resume_disabled")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)


# ----------------------------
# Summary (glass card)
# ----------------------------
st.markdown('<div class="section-header">Summary</div>', unsafe_allow_html=True)
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.write(SUMMARY)
st.markdown('</div>', unsafe_allow_html=True)


# ----------------------------
# Skills (visualized)
# ----------------------------
st.markdown('<div class="section-header">Skills</div>', unsafe_allow_html=True)

cols = st.columns(3)
for i, (group, items) in enumerate(SKILL_LEVELS.items()):
    with cols[i]:
        st.markdown('<div class="skill-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="skill-title">{group}</div>', unsafe_allow_html=True)
        for label, pct in items.items():
            pct = max(0, min(100, int(pct)))
            st.markdown(f"""
            <div class="skill-row">
              <div class="skill-label"><span>{label}</span><span>{pct}%</span></div>
              <div class="bar"><div style="--w:{pct}%;"></div></div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ----------------------------
# Professional Experience (timeline + expand for details)
# ----------------------------
st.markdown('<div class="section-header">Professional Experience</div>', unsafe_allow_html=True)

st.markdown('<div class="timeline">', unsafe_allow_html=True)

for idx, exp in enumerate(EXPERIENCE):
    role_line = f"{exp['title']} — {exp['company']}"
    meta_line = f"{exp['location']} • {exp['dates']}"
    st.markdown(f"""
    <div class="t-item">
      <div class="t-dot"></div>
      <div class="t-card">
        <div class="t-top">
          <div class="t-role">{role_line}</div>
          <div class="t-meta">{meta_line}</div>
        </div>
        <div class="t-sub">Key highlights are available below.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander(f"View details: {exp['company']} ({exp['dates']})", expanded=False):
        for b in exp["bullets"]:
            st.write(f"• {b}")

st.markdown('</div>', unsafe_allow_html=True)


# ----------------------------
# Education (cards)
# ----------------------------
st.markdown('<div class="section-header">Education</div>', unsafe_allow_html=True)

edu_cols = st.columns(2)
for i, edu in enumerate(EDUCATION):
    with edu_cols[i % 2]:
        st.markdown(f"""
        <div class="edu-card">
          <div class="edu-degree">{edu["degree"]}</div>
          <div class="edu-school">{edu["school"]} • {edu["location"]}<br/>{edu["dates"]}</div>
          <div class="edu-extra">{edu["extra"]}</div>
        </div>
        """, unsafe_allow_html=True)


# ----------------------------
# Coursework (compact)
# ----------------------------
st.markdown('<div class="section-header">Coursework</div>', unsafe_allow_html=True)
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.write(", ".join(COURSEWORK))
st.markdown('</div>', unsafe_allow_html=True)


# ----------------------------
# Sticky CTA button (opens popup)
# ----------------------------
st.markdown('<div class="sticky-cta">', unsafe_allow_html=True)
if st.button("Let’s build something awesome → Drop me your detials :) ", key="sticky_contact"):
    contact_dialog()
st.markdown('</div>', unsafe_allow_html=True)


# ----------------------------
# Feedback widget at bottom (1–5 with emoji)
# ----------------------------
st.markdown('<div class="feedback-bar"><div class="feedback-inner">', unsafe_allow_html=True)

rating = st.slider(
    "Feedback (1 = Sad, 5 = Happy)",
    min_value=1, max_value=5,
    value=5, step=1,
    key="feedback_rating"
)

emoji_map = {
    1: ("😢", "Sad"),
    2: ("😕", "Not great"),
    3: ("😐", "Okay"),
    4: ("🙂", "Better"),
    5: ("😄", "Happy"),
}
emoji, label = emoji_map[rating]

st.markdown(
    f"""
    <div style="display:flex; align-items:center; gap:10px; margin-top:6px;">
      <div style="font-size:26px;">{emoji}</div>
      <div style="color: rgba(255,255,255,0.85); font-size:14px;">
        You selected <b>{rating}</b> — {label}
      </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("</div></div>", unsafe_allow_html=True)

# spacer so last content isn't hidden behind fixed bars
st.markdown("<div style='height:120px;'></div>", unsafe_allow_html=True)
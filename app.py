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
# Custom CSS (unique look + font)
# ----------------------------
st.markdown("""
<style>
            
.block-container { padding-top: 0rem !important; }
header[data-testid="stHeader"], div[data-testid="stToolbar"] { display:none !important; }

.profile-top { display:flex; justify-content:center; margin-top: 14px; margin-bottom: 14px; }

.profile-img {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid rgba(255,255,255,0.22);
  box-shadow: 0 12px 30px rgba(0,0,0,0.45);
}

.center-text { text-align:center; }
            
/* Section headers (Summary, Experience, etc.) */
.section-header {
    font-family: "Space Grotesk", sans-serif;
    font-size: 28px;          /* ⬅ increase size here */
    font-weight: 700;
    margin-top: 32px;
    margin-bottom: 14px;
    letter-spacing: 0.5px;
    color: rgba(255,255,255,0.95);
}

/* Optional underline effect */
.section-header::after {
    content: "";
    display: block;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #ec4899);
    margin-top: 6px;
    border-radius: 2px;
}
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

.feedback-inner {
  max-width: 1200px;
  margin: 0 auto;
}

            .footer-bar{
  width:100%;
  margin-top: 40px;
  padding: 18px 10px 8px;
  border-top: 1px solid rgba(255,255,255,0.12);
  text-align:center;
  color: rgba(255,255,255,0.70);
  font-size: 14px;
}

.footer-link-btn button{
  background: transparent !important;
  border: none !important;
  color: rgba(199,210,254,0.95) !important;
  font-weight: 700 !important;
  text-decoration: underline !important;
  cursor: pointer !important;
  padding: 0 !important;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------
# Resume content (from your PDF)
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

SKILLS = {
    "Programming": ["Java", "Python", "JavaScript", "Django"],
    "Messaging": ["Kafka"],
    "Containers & Cloud": ["Docker", "OpenShift", "Kubernetes"],
    "Databases": ["SQL Server", "Oracle"],
    "Tools": ["ActOne 6.6", "IFM 10.X", "Git", "Jira"]
}

COURSEWORK = [
    "Operating Systems", "Theory of Computation", "Database Systems", "Advanced Algorithms",
    "Machine Vision", "Cloud Computing", "Information Retrieval", "Machine Learning", "Advanced Cryptography"
]

# ----------------------------
# HERO SECTION (Top picture centered + name left)
# ----------------------------

PROFILE_IMG = Path("assets/profile.jpeg")

def img_to_base64(path: Path) -> str:
    data = path.read_bytes()
    return base64.b64encode(data).decode()

st.markdown('<div class="profile-top">', unsafe_allow_html=True)

if PROFILE_IMG.exists():
    b64 = img_to_base64(PROFILE_IMG)
    st.markdown(
        f'<img class="profile-img" src="data:image/jpeg;base64,{b64}"/>',
        unsafe_allow_html=True
    )
else:
    st.error("Profile photo not found. Put it here: assets/profile.jpeg")

# Details below (left aligned)
st.markdown(f'<div class="name">{FULL_NAME}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="role">{ROLE}</div>', unsafe_allow_html=True)

st.markdown(
    f'<div class="meta">📧 <a href="mailto:{EMAIL}">{EMAIL}</a> &nbsp; | &nbsp; 📞 {PHONE}</div>',
    unsafe_allow_html=True
)

st.markdown("""
<span class="pill">Fraud •</span>
<span class="pill">Actimize (IFM / ActOne) •</span>
<span class="pill">Java • Spring Boot •</span>
<span class="pill">OpenShift • Docker •</span>
<span class="pill">Kafka</span>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# SUMMARY
# ----------------------------
st.markdown('<div class="section-header">Summary</div>', unsafe_allow_html=True)
st.write(SUMMARY)

# ----------------------------
# EXPANDABLE SECTIONS
# ----------------------------
st.markdown('<div class="section-header">Professional Experience</div>', unsafe_allow_html=True)

for exp in EXPERIENCE:
    header = f"{exp['title']} — {exp['company']} ({exp['location']}) | {exp['dates']}"
    with st.expander(header, expanded=False):
        for b in exp["bullets"]:
            st.write(f"• {b}")

st.markdown('<div class="section-header">Education</div>', unsafe_allow_html=True)
for edu in EDUCATION:
    header = f"{edu['degree']} — {edu['school']} ({edu['location']}) | {edu['dates']}"
    with st.expander(header, expanded=False):
        st.write(edu["extra"])

# ----------------------------
# SKILLS + COURSEWORK
# ----------------------------
st.markdown('<div class="section-header">Skills</div>', unsafe_allow_html=True)

skill_cols = st.columns(2)
left = skill_cols[0]
right = skill_cols[1]

with left:
    st.markdown("**Core Skills**")
    for k, v in SKILLS.items():
        st.write(f"**{k}:** {', '.join(v)}")

with right:
    st.markdown("**Coursework**")
    st.write(", ".join(COURSEWORK))


def send_contact_email(to_email: str, from_email: str, app_password: str, user_email: str, user_phone: str, notes: str):
    msg = EmailMessage()
    msg["Subject"] = "New Portfolio Contact Submission"
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Cc"] = user_email

    body = f"""
New contact submitted from your Streamlit portfolio:

User Email: {user_email}
User Phone: {user_phone}
Message: {notes if notes else "(no message)"}
"""
    msg.set_content(body)

    # Gmail SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(from_email, app_password)
        smtp.send_message(msg)


# --- dialog (popup) ---
@st.dialog("Let's get in touch 🤝")
def contact_dialog():
    st.write("Share your details and I’ll reach out.")

    with st.form("contact_form", clear_on_submit=True):
        email = st.text_input("Email *", placeholder="name@gmail.com")
        phone = st.text_input("Phone number *", placeholder="+1 469 347 5994")
        notes = st.text_area("Message (optional)", placeholder="Tell me what you’re looking for…")

        submitted = st.form_submit_button("Submit")

    if submitted:
        # Basic validation
        email_ok = re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email or "")
        phone_ok = re.match(r"^\+?[0-9 ()-]{7,20}$", phone or "")

        if not email_ok:
            st.error("Please enter a valid email.")
            st.stop()

        if not phone_ok:
            st.error("Please enter a valid phone number.")
            st.stop()

        # Store in session (you can also save to file/db)
        if "contact_submissions" not in st.session_state:
            st.session_state.contact_submissions = []

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
            st.success("Thanks! Your details were emailed to Mahesh ✅")
        except Exception as e:
            st.error("Saved your submission, but email sending failed.")
            st.write("Error:", str(e))

# --- Footer ---
st.markdown('<div class="footer-bar">', unsafe_allow_html=True)

# Create a "clickable text" feel using a button with link styling
colA, colB, colC = st.columns([1, 1, 1])
with colB:
    st.markdown('<div class="footer-link-btn">', unsafe_allow_html=True)
    if st.button("Let’s get in touch", key="open_contact"):
        contact_dialog()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# --- Feedback widget at bottom ---
st.markdown('<div class="feedback-bar"><div class="feedback-inner">', unsafe_allow_html=True)

rating = st.slider("Feedback (1 = Sad, 5 = Happy)", min_value=1, max_value=5, value=5, step=1, key="feedback_rating")

# Emoji logic
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

# add extra spacing so last content isn't hidden behind fixed bar
st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)

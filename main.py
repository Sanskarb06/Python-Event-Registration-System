import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import re

# ==================================================
# CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Python Workshop | Registration",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


EVENT_NAME = "Python Workshop"
EVENT_VENUE = "ABC Training Center"
EVENT_DATE = "30-09-2026"
FILE_NAME = Path(__file__).with_name("registrations.txt")


# ==================================================
# PREMIUM BLACK THEME
# ==================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #080a10;
    --card: #111521;
    --border: #292f43;
    --blue: #38bdf8;
    --purple: #8b5cf6;
    --text: #f4f6ff;
    --muted: #a0abc5;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 10% 0%, #15213c 0%, transparent 38%),
        radial-gradient(ellipse at 95% 10%, #281638 0%, transparent 32%),
        var(--bg);
    color: var(--text);
}

[data-testid="stHeader"] {
    background: rgba(8, 10, 16, 0.85);
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c1222, #11101d, #090b12);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    color: #f4f6ff;
}

.hero {
    background:
        radial-gradient(ellipse at 90% 10%, #34205e 0%, transparent 42%),
        linear-gradient(125deg, #151c2d, #111321 65%, #20132e);
    border: 1px solid #343452;
    border-radius: 24px;
    padding: 32px;
    margin-bottom: 24px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, .25);
}

.hero h1 {
    font-size: clamp(32px, 4vw, 49px);
    font-weight: 800;
    line-height: 1.15;
    background: linear-gradient(90deg, #38bdf8, #a78bfa, #f0abfc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero h3 {
    color: #f4f6ff !important;
}

.hero p {
    color: #aab5d0;
    font-size: 17px;
}

.panel {
    background: linear-gradient(145deg, #151a28, #10131e);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, .18);
}

.info-card {
    background: linear-gradient(145deg, #171e30, #111522);
    border: 1px solid #303954;
    border-radius: 16px;
    padding: 20px;
    min-height: 100px;
    transition: .2s;
}

.info-card:hover {
    border-color: #8b78ef;
    transform: translateY(-2px);
}

.info-label {
    color: #9ba9c8;
    font-size: 12px;
    letter-spacing: 1px;
}

.info-value {
    color: #f4f6ff;
    font-size: 17px;
    font-weight: 700;
    margin-top: 8px;
}

h1, h2, h3, h4 {
    color: #f4f6ff !important;
}

p, label, li {
    color: #d2d9ec;
}

[data-testid="stCaptionContainer"] {
    color: var(--muted);
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background: #0c101b !important;
    color: #f4f6ff !important;
    border: 1px solid #353d55 !important;
    border-radius: 11px !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #8b78ef !important;
    box-shadow: 0 0 0 1px #8b78ef !important;
}

[data-baseweb="select"] > div {
    background: #111522 !important;
    border-color: #353d55 !important;
    color: white !important;
}

.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    background: linear-gradient(100deg, #168cff, #7547ed) !important;
    color: white !important;
    border: none !important;
    border-radius: 11px !important;
    min-height: 44px;
    font-weight: 700;
    transition: .2s;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover,
.stDownloadButton > button:hover {
    box-shadow: 0 0 22px rgba(102, 92, 246, .4);
    transform: translateY(-1px);
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #161c2c, #10141f);
    border: 1px solid #303954;
    border-radius: 16px;
    padding: 18px;
}

[data-testid="stMetricLabel"] {
    color: #aab5d0 !important;
}

[data-testid="stMetricValue"] {
    color: #70c9ff !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #303954;
    border-radius: 12px;
    overflow: hidden;
}

[data-testid="stForm"] {
    background: #10141f;
    border: 1px solid #292f43;
    border-radius: 15px;
    padding: 20px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: #10141f;
    border-radius: 12px;
}

.stTabs [aria-selected="true"] {
    color: #70c9ff !important;
}

hr {
    border-color: #2b3247;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# FILE HANDLING
# ==================================================

def load_participants():
    participants = []

    if not FILE_NAME.exists():
        return participants

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.rstrip("\n").split(" | ")

                if len(parts) == 4:
                    participants.append({
                        "Name": parts[0],
                        "Email": parts[1],
                        "Mobile": parts[2],
                        "Registration Time": parts[3]
                    })
    except OSError:
        st.error("Unable to read registrations.txt.")

    return participants


def save_participant(name, email, mobile):
    registration_time = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    try:
        with open(FILE_NAME, "a", encoding="utf-8") as file:
            file.write(
                f"{name} | {email} | {mobile} | "
                f"{registration_time}\n"
            )
        return True

    except OSError:
        st.error("Unable to save registration.")
        return False


# ==================================================
# SIDEBAR NAVIGATION
# ==================================================

with st.sidebar:
    st.markdown(
        "<h1 style='text-align:center;'>🎓</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h2 style='text-align:center;'>Event<br>Registration<br>System</h2>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Register Participant",
            "👥 View Participants",
            "📅 Event Details",
            "ℹ️ About"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 🐍 Learn Python")
    st.caption("Learn today. Build tomorrow.")
    st.markdown("---")
    st.caption("Built with ❤️ using Streamlit")


# ==================================================
# HERO HEADER
# ==================================================

st.markdown(f"""
<div class="hero">
    <h1>Python Workshop</h1>
    <h3>Event Registration System</h3>
    <p>Join our hands-on Python workshop and take your
    programming skills to the next level.</p>
</div>
""", unsafe_allow_html=True)


# ==================================================
# EVENT SUMMARY CARDS
# ==================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="info-card">
        <div class="info-label">📅 EVENT DATE</div>
        <div class="info-value">{EVENT_DATE}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="info-card">
        <div class="info-label">📍 VENUE</div>
        <div class="info-value">{EVENT_VENUE}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="info-card">
        <div class="info-label">🎯 EVENT</div>
        <div class="info-value">{EVENT_NAME}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")


# ==================================================
# REGISTER PARTICIPANT
# ==================================================

if page == "🏠 Register Participant":

    left, right = st.columns([1.35, 1])

    with left:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("🙋 Register Participant")
        st.write("Fill in your details to reserve your place.")

        with st.form("registration_form", clear_on_submit=True):
            name = st.text_input(
                "Participant Name",
                placeholder="Enter your full name"
            )

            email = st.text_input(
                "Email Address",
                placeholder="you@example.com"
            )

            mobile = st.text_input(
                "Mobile Number",
                placeholder="Enter your 10-digit number",
                max_chars=10
            )

            submitted = st.form_submit_button(
                "🚀 Register Now",
                type="primary",
                use_container_width=True
            )

        if submitted:
            name = name.strip()
            email = email.strip().lower()
            mobile = mobile.strip()

            if not name or not email or not mobile:
                st.error("Please fill in all fields.")

            elif not re.fullmatch(r"[A-Za-z0-9 .'-]+", name):
                st.error("Please enter a valid name.")

            elif not re.fullmatch(
                r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                email
            ):
                st.error("Please enter a valid email address.")

            elif not mobile.isdigit() or len(mobile) != 10:
                st.error("Enter a valid 10-digit mobile number.")

            elif any("|" in value or "\n" in value
                     for value in [name, email, mobile]):
                st.error("Please remove separator characters.")

            else:
                participants = load_participants()

                duplicate = any(
                    p["Email"].lower() == email
                    for p in participants
                )

                if duplicate:
                    st.warning(
                        "This email is already registered!"
                    )

                elif save_participant(name, email, mobile):
                    st.success(
                        f"Welcome, {name}! Registration successful."
                    )
                    st.balloons()
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="panel">
            <h2>✨ Why Join?</h2>
            <p>✅ Hands-on Python training</p>
            <p>✅ Practical coding exercises</p>
            <p>✅ Learn from industry experts</p>
            <p>✅ Interactive learning sessions</p>
            <p>✅ Network with fellow learners</p>
            <hr>
            <h3>💡 What You'll Learn</h3>
            <p>Variables, data types, conditions, loops,
            functions and real-world Python applications.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.subheader("📊 Workshop Overview")

    participants = load_participants()

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric("Total Participants", len(participants))

    with m2:
        st.metric("Workshop", EVENT_NAME)

    with m3:
        st.metric("Venue", EVENT_VENUE)


# ==================================================
# VIEW PARTICIPANTS
# ==================================================

elif page == "👥 View Participants":

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("👥 Registered Participants")
    st.write("Search and view all registered participants.")

    participants = load_participants()

    if participants:
        df = pd.DataFrame(participants)

        st.metric("Total Registrations", len(df))

        search = st.text_input(
            "🔍 Search Participants",
            placeholder="Search by name or email..."
        )

        if search:
            mask = (
                df["Name"].str.contains(
                    search, case=False, na=False, regex=False
                )
                | df["Email"].str.contains(
                    search, case=False, na=False, regex=False
                )
            )
            df = df[mask]

        st.dataframe(
            df.reset_index(drop=True),
            use_container_width=True,
            hide_index=True
        )

        csv_data = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download Participants CSV",
            data=csv_data,
            file_name="participants.csv",
            mime="text/csv"
        )

    else:
        st.info(
            "No participants registered yet. Be the first to register!"
        )

    st.markdown('</div>', unsafe_allow_html=True)


# ==================================================
# EVENT DETAILS
# ==================================================

elif page == "📅 Event Details":

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("📅 Event Details")

    st.markdown(f"## 🎓 {EVENT_NAME}")

    st.write(
        "A hands-on workshop designed to introduce participants "
        "to Python programming."
    )

    st.markdown("---")

    st.markdown(f"**📍 Venue:** {EVENT_VENUE}")
    st.markdown(f"**📆 Date:** {EVENT_DATE}")
    st.markdown("**💻 Mode:** Practical learning workshop")
    st.markdown(
        "**📚 Topics:** Python basics, functions, loops and projects"
    )

    st.info(
        "Please confirm the event date and venue with the organizer."
    )

    st.markdown('</div>', unsafe_allow_html=True)


# ==================================================
# ABOUT
# ==================================================

elif page == "ℹ️ About":

    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.subheader("ℹ️ About This Application")

    st.write("""
    The Event Registration System is a web application built
    using Python and Streamlit.

    ### Features
    - Participant registration
    - Email-based duplicate checking
    - Name, email and mobile validation
    - File-based data storage
    - Searchable participant table
    - CSV export
    - Event details and statistics

    ### Technologies Used
    """)

    st.code("Python | Streamlit | Pandas | File Handling")

    st.markdown('</div>', unsafe_allow_html=True)


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.markdown("""
<div style="text-align:center; color:#8b96b0; padding:12px;">
    🎓 Python Workshop Registration System<br>
    <small>Designed with Streamlit • Powered by Python</small>
</div>
""", unsafe_allow_html=True)

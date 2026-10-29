import os
from datetime import datetime

import mysql.connector
import streamlit as st

from ai_explanation import get_ai_advice

st.set_page_config(page_title="AI Career Guide", page_icon="🎯", layout="wide")


# ---------- Database ----------
@st.cache_data(show_spinner=False)
def load_careers():
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "blackroom"),
        database=os.getenv("DB_NAME", "career_guidance"),
    )
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM careers")
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return rows


# ---------- Scoring (same rules as main.py, made case-insensitive) ----------
def txt(value):
    return str(value or "").strip().lower()


def score_careers(careers, info):
    results = []
    user_skills = [s.strip().lower() for s in info["skills"].split(",") if s.strip()]

    for career in careers:
        score = 0
        if info["interest"] and info["interest"].lower() in txt(career["interest"]):
            score += 1
        if info["subject"] and info["subject"].lower() in txt(career["subject"]):
            score += 1
        if info["education"].lower() == txt(career["education_level"]):
            score += 1
        if info["environment"].lower() == txt(career["preferred_working_environment"]):
            score += 1
        if info["percentage"] is not None:
            try:
                if info["percentage"] >= float(career["minimum_percentage"]):
                    score += 1
            except (TypeError, ValueError):
                pass
        for skill in user_skills:
            if skill in txt(career["skills"]):
                score += 1
        results.append((career, score))

    results.sort(key=lambda x: x[1], reverse=True)
    return results


def build_report(info, top3):
    lines = ["===== USER INFORMATION =====", f"Name: {info['name']}",
             f"Education Level: {info['education']}",
             f"Percentage: {info['percentage']}",
             f"Interest: {info['interest']}",
             f"Favorite Subject: {info['subject']}",
             f"Skills: {info['skills']}",
             f"Preferred Working Environment: {info['environment']}",
             "", "==== Top 3 Career Matches ===="]
    for i, (c, score) in enumerate(top3, start=1):
        lines += [
            f"{i}. {c['career']} (Score: {score})",
            f"Description: {c['description']}",
            f"Your Interest: {c['interest']}",
            f"Skills you need to develop: {c['skills']}",
            f"Subjects you need to focus on: {c['subject']}",
            f"Education Level Required: {c['education_level']}",
            f"Education Level after 12th: {c['after_12th_degree']}",
            f"Entrance Exams Required: {c['entrance_exams']}",
            f"Stream Required: {c['stream']}",
            f"Minimum Percentage Required: {c['minimum_percentage']}",
            f"Preferred Working Environment: {c['preferred_working_environment']}",
            "-----------------------------",
        ]
    return "\n".join(lines)


# ---------- Header ----------
st.title("🎯 AI Career Guide")
st.caption("Tell us about yourself and get your top 3 career matches, plus AI advice.")

try:
    careers = load_careers()
except Exception as e:
    st.error(f"Could not connect to the database: {e}")
    st.stop()

# ---------- Input form ----------
with st.form("career_form"):
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Your name")
        education = st.selectbox("Education level", ["10th", "12th", "Graduate", "Other"], index=1)
        percentage = st.number_input(
            "Percentage (used for 10th / 12th)", min_value=0.0, max_value=100.0, value=60.0, step=0.5
        )
        stream = st.selectbox("Stream (12th only)", ["Science", "Commerce", "Arts"])
    with c2:
        interest = st.text_input("Interest", placeholder="e.g. technology, design, helping people")
        subject = st.text_input("Favorite subject", placeholder="e.g. Maths")
        skills = st.text_input("Your skills (comma separated)", placeholder="e.g. coding, communication")
        environment = st.text_input("Preferred working environment", placeholder="e.g. office, remote, field")
    submitted = st.form_submit_button("Find my careers", type="primary", use_container_width=True)

if submitted:
    if not name.strip():
        st.warning("Please enter your name.")
    else:
        info = {
            "name": name.strip().upper(),
            "education": education,
            "percentage": percentage if education in ("10th", "12th") else None,
            "stream": stream if education == "12th" else None,
            "interest": interest.strip(),
            "subject": subject.strip(),
            "skills": skills.strip(),
            "environment": environment.strip(),
        }
        ranked = score_careers(careers, info)
        st.session_state["info"] = info
        st.session_state["top3"] = ranked[:3]
        st.session_state.pop("advice", None)

# ---------- Results ----------
if "top3" in st.session_state:
    info = st.session_state["info"]
    top3 = st.session_state["top3"]

    st.divider()
    st.subheader(f"Top 3 matches for {info['name']}")

    for i, (c, score) in enumerate(top3, start=1):
        with st.expander(f"{i}. {c['career']}  —  Score: {score}", expanded=(i == 1)):
            st.write(c["description"])
            a, b, d = st.columns(3)
            a.metric("Min. percentage", c["minimum_percentage"])
            b.metric("Stream", c["stream"])
            d.metric("Education level", c["education_level"])
            st.markdown(f"**Interest:** {c['interest']}")
            st.markdown(f"**Skills to develop:** {c['skills']}")
            st.markdown(f"**Subjects to focus on:** {c['subject']}")
            st.markdown(f"**Degree after 12th:** {c['after_12th_degree']}")
            st.markdown(f"**Entrance exams:** {c['entrance_exams']}")
            st.markdown(f"**Working environment:** {c['preferred_working_environment']}")

    report = build_report(info, top3)
    col_a, col_b = st.columns(2)
    with col_a:
        st.download_button(
            "⬇️ Download career report", report,
            file_name="career_report.txt", mime="text/plain", use_container_width=True,
        )
    with col_b:
        if st.button("🤖 Get AI advice for my best match", use_container_width=True):
            best = top3[0][0]["career"]
            with st.spinner("Asking the AI..."):
                try:
                    st.session_state["advice"] = get_ai_advice(best)
                except Exception as e:
                    st.session_state["advice"] = None
                    st.error(f"AI advice failed: {e}")

    if st.session_state.get("advice"):
        st.subheader("🤖 AI Career Advice")
        st.info(st.session_state["advice"])

    # keep the original behaviour of saving the report file
    with open("career_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
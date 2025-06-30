
import streamlit as st
import re
import tempfile
import spacy
import textstat
import pdfplumber
import docx

# Ensure spaCy model is loaded
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

st.set_page_config(page_title="AI Resume Sculptor", layout="centered")

# Step 0: Logo/Splash
st.image("https://i.ibb.co/gJ1M5pL/logo-splash.png", use_column_width=True)
st.markdown("<h3 style='text-align: center;'>AI Resume Sculptor</h3>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Step 1: Login UI (simplified)
with st.expander("🔐 Login to continue"):
    login_method = st.radio("Choose login method", ["Email/Password", "Google (Simulated)"], horizontal=True)
    if login_method == "Email/Password":
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            st.success(f"Welcome {email}")
    elif login_method == "Google (Simulated)":
        if st.button("Continue with Google"):
            st.success("Simulated Google Login Successful")

# Step 2–5: Upload Resume & Profile Analysis
uploaded_file = st.file_uploader("📁 Upload Resume", type=["pdf", "docx"], key="resume_uploader")
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        filename = tmp_file.name

    def extract_text(fname):
        if fname.endswith(".pdf"):
            with pdfplumber.open(fname) as pdf:
                return "\n".join([p.extract_text() or "" for p in pdf.pages])
        elif fname.endswith(".docx"):
            return "\n".join([para.text for para in docx.Document(fname).paragraphs])
        return ""

    def extract_email(text):
        match = re.search(r"[\w.-]+@[\w.-]+", text)
        return match.group(0) if match else "Not Found"

    text = extract_text(filename)
    email = extract_email(text)

    st.subheader("📄 Extracted Info")
    st.write("📧 Email:", email)
    st.text_area("📝 Resume Text", text[:3000])

# Step 6–8: ATS Match & Feedback
st.subheader("📊 ATS Match Engine")
jd_skills = {"python", "machine learning", "communication", "sql"}
resume_words = set(re.findall(r'\b\w+\b', text.lower())) if uploaded_file else set()
matched = jd_skills & resume_words
score = round((len(matched)/len(jd_skills)) * 100, 2) if jd_skills else 0
st.write("Matched Skills:", matched)
st.write("Match Score:", f"{score}%")

# Step 9–11: AI Chatbot & Interview
st.subheader("🤖 HR Interview (Mock)")
questions = ["Tell me about yourself", "What is your strength?", "Why should we hire you?"]
for i, q in enumerate(questions):
    st.write(f"**Q{i+1}: {q}**")
    st.text_input("Answer", key=f"ans{i}")

# Step 12–16: Chatbot & Feedback & DB Save (Simulated)
st.subheader("💬 AI Chatbot Kannama")
st.info("Type anything about your doubts, career, jobs etc.")

st.subheader("📝 HR Feedback (Simulated)")
st.text_area("Feedback from Company")

# Step 17–22: Deployment Notice
st.success("✅ All features loaded and ready for deployment!")
st.markdown("🔗 Visit Streamlit Cloud to deploy this app.")

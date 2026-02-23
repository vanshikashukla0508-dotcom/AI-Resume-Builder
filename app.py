import streamlit as st
import openai
from docx import Document
import io

# OpenRouter API setup
openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"

MODEL_NAME = "openai/gpt-3.5-turbo"


# DOCX creation function
def create_docx_resume(resume_text, template):
    doc = Document()

    if template == "Modern":
        doc.add_heading("RESUME", level=0)
    elif template == "Professional":
        doc.add_heading("Professional Resume", level=0)
    else:
        doc.add_heading("Resume", level=0)

    for line in resume_text.split("\n"):
        doc.add_paragraph(line)

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    return buffer


# Streamlit UI
st.title("AI Resume Builder")

name = st.text_input("Full Name")
education = st.text_area("Education")
skills = st.text_area("Skills")
experience = st.text_area("Experience")

template = st.selectbox(
    "Select Template",
    ["Modern", "Professional", "Minimal"]
)


if st.button("Generate Resume"):

    if name and education and skills:

        prompt = f"""
        Create a professional resume for:

        Name: {name}
        Education: {education}
        Skills: {skills}
        Experience: {experience}

        Include summary, skills, education, and experience sections.
        """

        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        resume_output = response['choices'][0]['message']['content']

        st.subheader("Generated Resume")
        st.write(resume_output)

        docx_file = create_docx_resume(resume_output, template)

        st.download_button(
            label="Download Resume (.docx)",
            data=docx_file,
            file_name=f"{name}_Resume.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    else:
        st.error("Please fill required fields")

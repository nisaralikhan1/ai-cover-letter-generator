# 1. Import libraries
import os
import streamlit as st
from dotenv import load_dotenv

# LangChain / Google Gemini libraries
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

# 2. Load environment variables
load_dotenv()

# We use "MY_API_KEY" because that is what you have in your .env file
api_key = os.getenv("API_KEY")

# 3. Initialize the Gemini LLM
# This setup matches Sir Hassaan's style but uses the Google Gemini model
if api_key:
   llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=api_key,
    temperature=0.7,
)
else:
    st.error("❌ API Key not found! Please check your .env file for 'MY_API_KEY'.")
    st.stop()

# 4. The System Message (The "Persona")
# Formatted with <div> tags just like the reference code
system_message = SystemMessage(
    content="""
    <div>
    You are a Professional Career Consultant and Expert Resume Writer.
    Speak with the authority, encouragement, and clarity of a recruitment expert.
    Your goal is to bridge the gap between a candidate's resume and a job's requirements.
    Do not break character under any circumstances.
    </div>

    <div>
    Instructions:
    - Analyze the provided Resume and Job Description.
    - Write a formal, high-impact cover letter (exactly 3 paragraphs).
    - Match specific skills from the resume to the job responsibilities.
    - End with a professional call to action and closing.
    </div>
    """
)

# 5. --- Streamlit UI (The Interface) ---
st.set_page_config(page_title="AI Cover Letter Generator", page_icon="📝")

st.title("📝 AI Cover Letter Generator")
st.markdown("Generate a professional, tailored cover letter in seconds using **Google Gemini AI**.")

# Layout for Inputs
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Job Description")
    job_description = st.text_area(
        "Paste the job requirements here...",
        height=300,
        placeholder="Copy requirements from LinkedIn, Indeed, etc."
    )

with col2:
    st.subheader("📄 Your Resume")
    resume_text = st.text_area(
        "Paste your resume text here...",
        height=300,
        placeholder="Copy and paste your CV content..."
    )

# 6. --- Generation Logic ---
if st.button("🚀 Generate My Cover Letter", type="primary", use_container_width=True):
    if job_description and resume_text:
        with st.spinner("Gemini is analyzing and writing..."):
            # Combine both inputs for the model to see
            user_input = f"JOB DESCRIPTION:\n{job_description}\n\nRESUME:\n{resume_text}"
            
            messages = [
                system_message,
                HumanMessage(content=user_input)
            ]
            
            try:
                # Call the model
                response = llm.invoke(messages)
                
                # Display the Result
                st.success("Cover Letter Generated Successfully!")
                st.divider()
                st.subheader("📝 Your Professional Cover Letter")
                st.write(response.content)
                
                # Download Button
                st.download_button(
                    label="📥 Download as Text File",
                    data=response.content,
                    file_name="Tailored_Cover_Letter.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please provide both the Job Description and your Resume.")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and LangChain for NAVTTC EB.")
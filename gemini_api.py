import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
#load_dotenv()

# Configure API Key
GEMINI_API_KEY = st.secrets["gemini"]["api_key"]

genai.configure(api_key=GEMINI_API_KEY)

def generate_response(prompt):
    """Calls Gemini API to generate a response."""
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text if response else "Sorry, I couldn't generate a response."

def generate_questions(prompt):
    """Calls Gemini API to generate diverse tech questions."""
    model = genai.GenerativeModel("gemini-pro")
    
    try:
        response = model.generate_content(prompt)
        if response and response.text:
            # Ensure we extract only valid questions and ignore unnecessary text
            questions = [q.strip() for q in response.text.split("\n") if q.strip()]
            return questions[:5]  # Ensure exactly 5 questions
        else:
            return ["Error: No valid questions generated."]
    except Exception as e:
        return [f"Error: {str(e)}"]



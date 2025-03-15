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
    model = genai.GenerativeModel(model_name="gemini-pro-1")
    response = model.generate_content(prompt)
    return response.text if response else "Sorry, I couldn't generate a response."

def generate_questions(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(prompt)

        # Ensure response is structured correctly
        if not response or not response.text:
            return ["Error: No response from API"]

        # Split response into list of questions
        questions = response.text.strip().split("\n")
        return questions[:5]  # Ensure only 5 questions

    except Exception as e:
        return [f"Error: {str(e)}"]




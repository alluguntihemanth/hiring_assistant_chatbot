import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure API Key
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GENAI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing! Please add it to your .env file.")

genai.configure(api_key=GENAI_API_KEY)

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



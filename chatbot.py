import streamlit as st
import google.generativeai as genai  # Gemini API
from auth import signup_user, login_user, save_user, get_user_data, delete_user_data
import gemini_api
from database import save_chat_history, get_chat_history, delete_all_user_data, save_user_score
from prompts import get_tech_questions
import time

# Initialize Gemini AI
GEMINI_API_KEY = st.secrets["gemini"]["api_key"]

genai.configure(api_key=GEMINI_API_KEY)

import re

def evaluate_response(candidate_answer):
    """Evaluates the candidate's answer using Gemini AI and returns a numeric score."""
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
    
    # Improved prompt for better response evaluation
    prompt = (
        "Evaluate the following technical answer on accuracy, completeness, and relevance to the topic. "
        "Provide a numeric score between 0 and 100, with 100 being perfect. Format: Score: [number]/100.\n\n"
        f"Answer: {candidate_answer}"
    )
    
    response = model.generate_content(prompt)

    # Extract numerical score using regex
    match = re.search(r"Score:\s*(\d+)", response.text)
    
    if match:
        return min(max(float(match.group(1)), 0), 100)  # Ensure score is within 0-100
    else:
        return 0.0  # Default score if extraction fails

# Page Title
st.title("🧑‍💻 TalentScout Hiring Assistant")
st.write("Helping recruiters assess tech candidates quickly!")

# Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.tech_questions = []
    st.session_state.current_question_index = 0
    st.session_state.scores = []  # Initialize scores list    

# Login or Signup
if not st.session_state.logged_in:
    option = st.selectbox("Login or Signup", ["Login", "Signup"])
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if option == "Signup":
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        experience = st.number_input("Years of Experience", min_value=0, max_value=50, step=1)
        position = st.selectbox("Desired Position", ["Full Stack Developer", "Frontend Developer", "Backend Developer", "ML Engineer", "Gen AI Engineer"])
        location = st.text_input("Current Location")
        tech_stack = st.text_area("Tech Stack (e.g., Python, React, AWS)")

    # GDPR Policy
    st.subheader("🔐 Privacy Policy")
    st.markdown(
        "By using this application, you agree to our **[Privacy Policy](https://docs.google.com/document/d/1_qotecui4tWRO5VqqaMK0af5YKofpzs0shQpq9dsFjg/edit?usp=sharing)**. "
        "You can delete your data at any time."
    )
    agree_gdpr = st.checkbox("I agree to the Privacy Policy", key="gdpr_checkbox")

    if option == "Signup":
        if st.button("Signup") and agree_gdpr:
                user_id = signup_user(email, password)
                if user_id:
                    save_user(user_id, email, name, phone, experience, position, location, tech_stack)
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.session_state.tech_questions = get_tech_questions(tech_stack)[:5]
                    st.success("Signup successful!")
                    st.rerun()
                else:
                    st.error("Error during signup!")
        elif not agree_gdpr:
            st.warning("You must accept the Privacy Policy to continue.")

    elif option == "Login":
        if st.button("Login") and agree_gdpr:
            user_id = login_user(email, password)
            if user_id:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                user_data = get_user_data(user_id)
                st.session_state.tech_questions = get_tech_questions(user_data["tech_stack"])[:5]
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials!")
        elif not agree_gdpr:
            st.warning("You must accept the Privacy Policy to continue.")


# Logged-in State
if st.session_state.logged_in:
    user_data = get_user_data(st.session_state.user_id)
    st.write(f"Welcome, **{user_data['name']}**! Your Tech Stack: {user_data['tech_stack']}")

    # Ask Tech Questions Sequentially
    if st.session_state.current_question_index < len(st.session_state.tech_questions):
        current_question = st.session_state.tech_questions[st.session_state.current_question_index]
        st.write(f"📌 **{current_question}**")

        candidate_answer = st.text_area("Your Answer:", key=f"answer_{st.session_state.current_question_index}")

        if st.button("Submit"):
            score = evaluate_response(candidate_answer)  # Evaluate response with Gemini
            st.session_state.scores.append(score)

            save_chat_history(st.session_state.user_id, current_question, candidate_answer)
            st.session_state.current_question_index += 1
            st.session_state[f"answer_{st.session_state.current_question_index}"] = ""
            st.rerun()
    else:
        average_score = sum(st.session_state.scores) / len(st.session_state.scores)
        st.write(f"✅ Assessment Complete! Your final score: **{average_score:.2f}%**")
        save_user_score(st.session_state.user_id, average_score)

    # User Data Deletion (Button deactivated after first click)
    if "delete_clicked" not in st.session_state:
        st.session_state.delete_clicked = False

    st.subheader("⚠️ Delete Your Data")
    st.write("If you wish to remove all your stored data, click below.")
    delete_button = st.button("Delete My Data", disabled=st.session_state.delete_clicked)

    if delete_button:
        delete_all_user_data(st.session_state.user_id)
        st.session_state.delete_clicked = True
        st.success("Your data has been deleted successfully.")
        time.sleep(2)
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.rerun()
    
    # Logout Button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.tech_questions = []
        st.session_state.current_question_index = 0
        st.rerun()

import streamlit as st
from auth import signup_user, login_user, save_user, get_user_data, delete_user_data
import gemini_api
from database import save_chat_history, get_chat_history, delete_all_user_data
from prompts import get_tech_questions

# Page Title
st.title("🧑‍💻 TalentScout Hiring Assistant")
st.write("Helping recruiters assess tech candidates quickly!")


# Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.tech_questions = []
    st.session_state.current_question_index = 0

# Login or Signup
if not st.session_state.logged_in:
    option = st.selectbox("Login or Signup", ["Login", "Signup"])
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    # GDPR Policy
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.subheader("🔐 Privacy Policy")
        st.markdown(
            "By using this application, you agree to our **[Privacy Policy](https://docs.google.com/document/d/1_qotecui4tWRO5VqqaMK0af5YKofpzs0shQpq9dsFjg/edit?usp=sharing)**. "
            "You can delete your data at any time."
        )
    # Accept GDPR Policy
    agree_gdpr = st.checkbox("I agree to the Privacy Policy", key="gdpr_checkbox")

    if option == "Signup":
        name = st.text_input("Full Name")
        tech_stack = st.text_area("Tech Stack (e.g., Python, React, AWS)")
        if st.button("Signup") and agree_gdpr:
            user_id = signup_user(email, password)
            if user_id:
                save_user(user_id, email, name, tech_stack)
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.tech_questions = get_tech_questions(tech_stack)[:5]
                st.success("Signup successful!")
                st.rerun()
            else:
                st.error("Error during signup!")
        elif not agree_gdpr:
            st.warning("You must accept the Privacy Policy to continue.")
    else:
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

        # Auto-expanding text box (no form border, submits on Enter)
        candidate_answer = st.text_area(
            "Your Answer:",
            key=f"answer_{st.session_state.current_question_index}",
            height=None,  # Expands dynamically
            max_chars=500  # Prevents excessive growth
        )

        # Submit Button
        if st.button("Submit", key=f"submit_{st.session_state.current_question_index}"):
            save_chat_history(st.session_state.user_id, current_question, candidate_answer)
            st.session_state.current_question_index += 1
            st.session_state[f"answer_{st.session_state.current_question_index}"] = ""
            st.rerun()
    else:
        st.write("✅ You've completed the technical assessment. Thank you!")

    # User Data Deletion
    st.subheader("⚠️ Delete Your Data")
    st.write("If you wish to remove all your stored data, click below.")
    if st.button("Delete My Data"):
        delete_all_user_data(st.session_state.user_id)
        st.success("Your data has been deleted successfully.")
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

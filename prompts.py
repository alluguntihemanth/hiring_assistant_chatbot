from gemini_api import generate_questions

def get_tech_questions(tech_stack):
    """Generates technical questions dynamically based on the user's tech stack."""
    prompt = (
        f"Generate exactly 5 diverse technical interview questions related to {tech_stack}. "
        "Ensure they cover different aspects such as programming, algorithms, debugging, best practices, "
        "and real-world applications. Do NOT provide answers, only questions."
    )
    questions = generate_questions(prompt)
    
    # Ensure questions list is valid and correctly formatted
    if not questions or len(questions) < 5:
        return ["Error: Failed to generate relevant questions. Please retry."]
    
    return questions

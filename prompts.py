from gemini_api import generate_questions

def get_tech_questions(tech_stack):
    """Generates technical questions dynamically based on the user's tech stack."""
    prompt = (
        f"Generate exactly 5 diverse technical interview questions related to {tech_stack}. "
        "Ensure they cover different aspects such as programming, algorithms, debugging, best practices, "
        "and real-world applications. Do NOT provide answers, only questions."
    )
    
    questions = generate_questions(prompt)

    if not isinstance(questions, list) or len(questions) < 5:
        return ["Error: Unable to generate enough questions. Try again later."]

    return questions


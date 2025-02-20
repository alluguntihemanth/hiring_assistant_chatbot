from firebase_admin import firestore

db = firestore.client()

def save_chat_history(user_id, question, response):
    chat_ref = db.collection("users").document(user_id).collection("chats")
    chat_ref.add({"question": question, "response": response})

def get_chat_history(user_id):
    chats = db.collection("users").document(user_id).collection("chats").stream()
    return [{"question": chat.get("question"), "response": chat.get("response")} for chat in chats]

def delete_all_user_data(user_id):
    """Deletes all user data including chats and account details"""
    user_ref = db.collection("users").document(user_id)
    chats_ref = user_ref.collection("chats").stream()

    # Delete chat history
    for chat in chats_ref:
        chat.reference.delete()

    # Delete user data
    user_ref.delete()

def save_user_score(user_id, score):
    db.collection("users").document(user_id).update({"final_score": score})
